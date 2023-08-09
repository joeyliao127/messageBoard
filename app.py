from flask import *
import mysql.connector
app = Flask(
    __name__,
    static_folder="public",
    static_url_path="/"
)
app.secret_key = "0xffffffff"


db_connection = {
            "host": "127.0.0.1",
            "port": 3306,
            "user": "root", # 替換為你的 MySQL 使用者名稱
            "password": "root", # 替換為你的 MySQL 密碼
            "database": "website" # 替換為你要連線的資料庫名稱
        }


def connectSQL(query):
    try:
        with mysql.connector.connect(**db_connection) as connection:
            if connection.is_connected():
                print("Connected to the database!")
                cursor = connection.cursor()
                sql_query = "SELECT * FROM member"	
                cursor.execute(sql_query)	
                result = cursor.fetchall() # 或使用 fetchone() 獲取一行	
                print(result)
                # 關閉 cursor 和連線
                cursor.close()
                connection.close()
                print("Connection closed.")

    except Exception as ex:
        print("Connection failed")
        print(ex)

def create(**data):

    pass
def verify(username, password):
    try:
        with mysql.connector.connect(**db_connection) as connection:
            if connection.is_connected():
                print("Connected to the database!")
                cursor = connection.cursor()
                sql_query = f"SELECT username, password FROM website.member where username='{username}' and password='{password}'"	
                cursor.execute(sql_query)
                result = cursor.fetchall() # 或使用 fetchone() 獲取一行	
                print(f"result={result}\n name={result[0][0]}\nusername={result[0][1]}")
                cursor.close()
                connection.close()
                print("Connection closed.")
                return result
                # 關閉 cursor 和連線
                
    except Exception as ex:
        print("Connection failed")
        print(ex)



def update(**data):
    pass
def delete(**query):
    pass

@app.route("/")
def index():
    session["status"] = False
    return render_template("index.html")

@app.route("/signin", methods=["POST"])
def signin():
    verified = verify(request.form["username"], request.form["password"])
    if(verified):
        session["status"] = True
        session["name"] = verified[0][0]
        session["username"] = verified[0][1]
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
    
    return redirect("/")

@app.route("/sql")
def sql():
    return redirect("error.html")
app.run(port=3000, debug=True, use_reloader=True)

