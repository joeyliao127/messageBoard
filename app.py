from flask import *
import mysql.connector
import json
import datetime
app = Flask(
    __name__,
    static_folder="public",
    static_url_path="/"
)
app.secret_key = "0xffffffff"
    
def connectionFactory(DB, host="127.0.0.1", port=3306, user="root", password="root"):
    def connectionDecorator(operationFn):
        def connectDB(*args, **queryStr):
            print("建立db_connection...")
            db_connection = {
                "host": host,
                "port": port,
                "user": "root", # 替換為你的 MySQL 使用者名稱
                "password": "root", # 替換為你的 MySQL 密碼
                "database": DB
            }
            try:
                with mysql.connector.connect(**db_connection) as connection:
                    print("Connected to database!")
                    try:
                        with connection.cursor() as cursor:
                            resutl = operationFn(cursor, **queryStr)
                            connection.commit()                      
                            return resutl     
                    except Exception as ex:
                            print("建立cursor失敗")
                            print(f"錯誤訊息:{ex}")
            except Exception as ex:
                print("連線失敗:")
                print(f"來自DB的錯誤訊息：{ex}")
        return connectDB
    return connectionDecorator



#請依照以下格式使用createMember()
#createMember(table=, name= ,username= ,password= )
#呼叫函式範例：createMember(table="member", name= 'Joey', username='joey', password='joey123')
@connectionFactory(DB="website")
def createMember(cursor, **queryStr):
    queryString = f"INSERT INTO {queryStr['table']} (name, username, password) VALUES ('{queryStr['name']}', '{queryStr['username']}', '{queryStr['password']}')"
    try:
        cursor.execute(queryString)
        return True
    except Exception as ex:
        print("新增失敗...")
        print(f"來自DB的錯誤訊息：{ex}")
        return False
# createMember(table = "member",name="aaa", username="aaa", password="aaa")

#請依照以下格式使用createMsg()
#createMsg(table=, name=, id=, content=)
@connectionFactory(DB="website")
def queryMsg(cursor, **queryStr):
    query = f"INSERT INTO message(member_id, content) VALUES({queryStr['id']},'{queryStr['content']}')"
    print(f"--------傳送到createMsg的query為-----------\n{query}")
    try:
        cursor.execute(query)
    except Exception as ex:
        print(f"message新增失敗，錯誤訊息：{ex}")
    

#請依照以下格式使用find()：
#1. find(queryStr= )
#2. queryStr需為完整的句子，如SELECT * FROM member where name = 'Joey'
#呼叫函式範例：find(queryStr="SELECT * FROM member where name = 'Joey'")

@connectionFactory(DB="website")
def find(cursor, **qureyStr):
    try:
        cursor.execute(qureyStr["qureyStr"])
        result = cursor.fetchall()
        print(f"查詢後的查詢結果為：{result}")
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
@connectionFactory(DB="website")
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
@connectionFactory(DB="website")
def delete(cursor, **qureyStr):
    try:
        print(f"刪除的query為： {qureyStr}")
        cursor.execute(qureyStr["qureyStr"])
    except Exception as ex:
        print(ex)

# delete(qureyStr="DELETE FROM member where name = 'AAA'")

def verify(username: str, password: str):
    queryStr = f"SELECT id,name, username FROM member where username = '{username}' and password = '{password}' "
    result = find(qureyStr=queryStr)
    print(f"verify中，從find取得的result = {result}")
    if(result):
        return result
    else:
        return None

def getComment(count: int):
    qureyStr = f"SELECT member.id, member.name, member.time, message.content FROM member JOIN message ON member.id = message.member_id ORDER BY member.time DESC  LIMIT 5 OFFSET {count};"
    queryResult =  find(qureyStr= qureyStr)
    result = []
    print(f"------------------getComment裡面未處理的result---------------\n{queryResult}")
    for data in queryResult:
        date = data[2].date()
        date = date.isoformat()
        result.append({
            "id": data[0],
            "name": data[1],
            "date": date,
            "comment": data[3]
        })
    return result

@app.route("/")
def index():
    session["status"] = False
    return render_template("index.html")

@app.route("/signin", methods=["POST"])
def signin():
    verified = verify(request.form["username"], request.form["password"])
    print(f'sign裡面的verified():{verified}')
    if(verified):
        session["status"] = True
        session["id"] = verified[0][0]
        session["name"] = verified[0][1]
        session["username"] = verified[0][2]
        
        return redirect("member")
    else:
        return redirect(url_for("error", message = "帳號或密碼錯誤"))

@app.route("/signout")
def signout():
    session["status"] = False
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
    result = find(qureyStr=queryStr)
    print(f"檢查註冊的使用者，是否有返回帳號：{result}")
    if(result):
        return redirect(url_for("error", message="帳號已經被註冊"))
    else:
        createMember(table="member", name=name, username=username, password=password)
        return redirect("/")

@app.route("/init")
def init():
    res = {
        "userInfo":{
            "id": session["id"],
            "name": session["name"]
        }
    }
    result = getComment(0)
    print(f"------------------init裡面接收到的result---------------\n{result}")
    res["msg"] = result
    print(res)
    res = json.dumps(res)
    return res


@app.route("/loadMore/<count>")
def loadMore(count):
    result = getComment(count=count)
    result = json.dumps(result)
    return result
    
@app.route("/jsonPage")
def jsonPage():
    qureyStr = "SELECT member.id, member.name, member.time, message.content FROM member JOIN message ON member.id = message.member_id ORDER BY member.time DESC LIMIT 5 OFFSET 0;"
    resutl =  find(qureyStr= qureyStr)
    res = {
        "userInfo":{
            "id": session["id"],
            "name": session["name"]
        },
        "msg":[]
    }
    for data in resutl:
        date = data[2].date()
        date = date.isoformat()
        res["msg"].append({
            "id": data[0],
            "name": data[1],
            "date": date,
            "comment": data[3]
        })
    print(res)
    res = json.dumps(res)
    return res

@app.route("/createMsg", methods=["POST"])
def createMsg():
   content = request.form["comment"]
   queryMsg(id=session["id"], content=content)
   return redirect("member")
app.run(port=3000, debug=True, use_reloader=True)


