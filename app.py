from flask import *
import mysql.connector
import json
# import datetime
app = Flask(
    __name__,
    static_folder="public",
    static_url_path="/"
)
app.secret_key = "0xffffffff"


db_connection = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "root",
    "database": "website"
}

try:
    # 建立與資料庫的連線
    connection = mysql.connector.connect(**db_connection) 
    if connection.is_connected():
        print("Connected to the database!")

except Exception as ex:
    print("Connection failed")
    print(ex)

cursor = connection.cursor(dictionary=True)

def createMember(name, username, password):
    queryString = f"INSERT INTO member (name, username, password) VALUES ('{name}', '{username}', '{password}')"
    try:
        cursor.execute(queryString)
        connection.commit()
        return True
    except Exception as ex:
        print("新增失敗...")
        print(f"來自DB的錯誤訊息：{ex}")
        return False
    
def find(qureyStr: str):
    try:
        cursor.execute(qureyStr)
        result = cursor.fetchall()
        print(f"------------查詢後的查詢結果為---------------：\n{result}")
        res = []
        for item in result:
            res.append(item)
        return res

    except Exception as ex:
        print("查詢失敗...")
        print(f"來自DB的錯誤訊息：{ex}")
        return False
# find(qureyStr="select * from member")


#請依照以下格式使用update()：
#1. update(queryStr= )
#2. update需為完整的句子，如 UPDATE member SET username='Wilson' WHERE id = 5
#呼叫函式範例：delete(queryStr="UPDATE member SET username='Wilson' WHERE id = 5")
def update(cursor, **queryStr):
    try:
        cursor.execute(queryStr["queryStr"])
        return True
    except Exception as ex:
        print("更新失敗...")
        print(f"來自DB的錯誤訊息為：{ex}")
        return False
    
# update(queryStr="UPDATE member SET username='Wilson' where id = 5")

#請依照以下格式使用delete
#1. delete(queryStr= )
#2. queryStr需為完整的句子，如 DELETE FROM member WHERE name = 'Joey'
#呼叫函式範例：delete(queryStr="DELETE FROM member where name = 'Joey'")
def delMsg(qureyStr):
    print(f"刪除的query為： {qureyStr}")
    try:   
        cursor.execute(qureyStr)
    except Exception as ex:
        print(ex)

# delete(qureyStr="DELETE FROM member where name = 'AAA'")

def verify(username: str, password: str):
    queryStr = f"SELECT id,name, username FROM member where username = '{username}' and password = '{password}' "
    
    result = find(queryStr)
    # print(f"-------------------verify中，從find取得的result-------------------\n{result}")
    if(result):
        return result
    else:
        return None

def getComment(count: int):
    qureyStr = f"SELECT member.id, member.name, member.time, message.content, message.id as msg_id FROM member JOIN message ON member.id = message.member_id ORDER BY message.id DESC LIMIT 5 OFFSET {count};"
    queryResult = find(qureyStr= qureyStr)
    result = []
    print(f"------------------getComment裡面未處理的result---------------\n{queryResult}")
    for data in queryResult:
        #data格式為：{'id': 2, 'name': 'Joey', 'time': datetime.datetime(2022, 6, 18, 0, 0), 'content': 'Hi here is Joey'}
        date = data["time"].date()        
        date = date.isoformat()
        result.append({
            "id": data["id"],
            "name": data["name"],
            "date": date,
            "comment": data["content"],
            "msg_id": data["msg_id"]
        })
    res = {
        "userInfo":{
            "id": session["id"],
            "name": session["name"]
        }
    }
    res["msg"] = result
    print("-----------------getComment JSON dumps之前的res-------------------", res)
    res = json.dumps(res)
    print("-----------------getComment JSON dumps之後的res-------------------", res)
    return res

def insertMsg(id, content):
    query = f"INSERT INTO message(member_id, content) VALUES({id},'{content}')"
    print(f"--------傳送到createMsg的query為-----------\n{query}")
    try:
        cursor.execute(query)
        connection.commit()
    except Exception as ex:
        print(f"message新增失敗，錯誤訊息：{ex}")


@app.route("/")
def index():
    session["status"] = False
    return render_template("index.html")

@app.route("/signin", methods=["POST"])
def signin():
    verified = verify(request.form["username"], request.form["password"])
    print(f'sign裡面的verified():{verified}')
    if(verified):
        data = verified[0]
        session["status"] = True
        session["id"] = data["id"]
        session["name"] = data["name"]
        session["username"] = data["username"]
        return redirect("member")
    else:
        return redirect(url_for("error", message = "帳號或密碼輸入錯誤"))

@app.route("/signout")
def signout():
    session["status"] = False
    session["id"]=""
    session["name"] = ""
    session["username"] = ""
    return redirect("/")

@app.route("/error")
def error():
    message = request.args.get("message")
    return render_template("error.html", message = message)

@app.route("/member")
def member():
    if(session["status"]):
        return render_template("member.html", name = session["name"])
    else:
        return redirect("/")
    
@app.route("/signup", methods=["POST"])
def signup():
    name = request.form["name"]
    username = request.form["username"]
    password = request.form["password"]
    queryStr = f"SELECT name FROM member WHERE name = '{username}'"
    result = find(queryStr)
    print(f"檢查註冊的使用者，是否有返回帳號：{result}")
    if(result):
        return redirect(url_for("error", message="帳號已經被註冊"))
    else:
        createMember(name, username, password)
        return redirect("/")

@app.route("/init")
def init():
    result = getComment(0)
    print(f"------------------init裡面接收到的result---------------\n{result}")
    return result


@app.route("/loadMore/<count>")
def loadMore(count):
    result = getComment(count=count)
    print(f"loadMore回傳的API---------------------------------------------\n{result}")
    return result

@app.route("/createMessage", methods=["POST"])
def createMessage():
   content = request.form["comment"]
   insertMsg(id=session["id"], content=content)
   return redirect("member")

@app.route("/getUserInfo")
def getUserInfo():
    res = {
        "id": session["id"]
    }
    res = json.dumps(res)
    return res

@app.route("/deleteMessage/", methods=["POST"])
def delMsg():
    data = request.json
    verify_id = data["user_id"]
    msg_id = data["msg_id"]
    print(f"data = {data}\nverify = {verify}\nmsg_id={msg_id}")
    if(int(verify_id) == session["id"]):
        print("驗證通過，執行刪除Fn")
        qureyStr = f"DELETE FROM message where id = {msg_id}"
        try:
            cursor.execute(qureyStr)
            connection.commit()
        except Exception as ex:
            print(f"刪除失敗，來自DB的錯誤訊息：{ex}")
    else:
        print("驗證失敗....")
    return "ok"

app.run(port=3000, debug=True, use_reloader=True)


