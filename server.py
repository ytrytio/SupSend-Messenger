import socket
import json
from time import time
import pymysql
from config import host, port, user, password, db

######################### МОЕ БЛЯТЬ, НЕ ТРОГАТЬ

class SupServer():
    # serverPort = 8080
    # serverSocket = socket(AF_INET, SOCK_STREAM)
    # serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    # serverSocket.bind(('', serverPort))
    # serverSocket.listen(2)
    def __init__(self):
        serverPort = 8080
        serverSocket = socket(AF_INET, SOCK_STREAM)
    
    
    def start_server(serverPort, serverSocket, self):
        serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        serverSocket.bind(('', serverPort))
        
    def generate_http_response(content, status_code=200, content_type="text/html"):
        response = f"HTTP/1.1 {status_code} OK\r\n"
        response += f"Content-Type: {content_type}\r\n"
        response += f"Content-Length: {len(content)}\r\n"
        response += "Connection: close\r\n"
        response += "\r\n"
        response += content
        return response


###########################

database = []
try:
    def connect():
        connection = pymysql.connect(
            host="127.0.0.1",
            port=3307,
            user=user,
            password=password,
            db=db,
            cursorclass=pymysql.cursors.DictCursor
        )
except OperationalError as e:
    print("Error connecting to database.")def error_allocate(self, error):
    print("[DEBUG] ")
    print("Reconnect...") 
    connect()

def handle_client(conn, addr):
    print(f"Connected by {addr}")
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            request = json.loads(data.decode('utf-8'))
            response = route_request(request)
            conn.sendall(json.dumps(response).encode('utf-8'))
    except Exception as e:
        print(f"Error handling client {addr}: {e}")
    finally:
        conn.close()


def route_request(request):
    route = request['route']
    method = request['method']
    match req:
        case '/':
            pass
        case '/status':
            pass
        case '/send':
            if method != 'POST': return
        case '/messages':
            pass
        case '/registration':
            if method != 'POST': return
        case '/login':
            if method != 'POST': return

    
    
def main():
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Simple Socket Server</title>
    </head>
    <body>
        <h1>Hello, User!</h1>
        <a href="/send">Send</a>
        <a href="/messages?after=0">Messages</a>
        <a href="/status">Status</a>
    </body>
    </html>
    """
    

def status():
    count_users = 1

    with connection.cursor() as sql:
        sql.execute("SELECT * FROM `users`")
        rows = sql.fetchall()

        for row in rows:
            print(row)
            count_users += 1

    return {
        'status': True,
        'name': 'Messenger',
        'time': time(),
        'count_user': count_users
    }

def groups():
    pass


def send_message():
    data = request.json
    print(data)

    name = data['name']
    text = data['text']

    if not isinstance(data, dict):
        return abort(400)
    if 'name' not in data or 'text' not in data:
        return abort(400)


    message = {
        'name': name,
        'text': text,
        'time': time()
    }

    database.append(message)
    return {'ok': True}

def get_message():
    try:
        after = float(request.args['after'])
    except Exception as ex:
        print(ex)
        return abort(400)
    
    messages = []

    for message in database:
        if message['time'] > after:
            messages.append(message)

    return {'messages': messages[:50]}


def registration():
    data = request.json

    if not isinstance(data, dict):
        return abort(400)
    if 'nickname' not in data or 'password' not in data:
        return abort(400)

    nickname = data['nickname']
    user_password = data['password']

    with connection.cursor() as sql:
        sql.execute("SELECT username FROM `users` WHERE username = %s", nickname)
        result = sql.fetchall()
        
        if len(result) == 0:
            sql.execute("INSERT INTO `users` VALUES('{0}', '{nickname}', '{user_password}')")
            connection.commit()
            return {'ok': True}
        else:
            return abort(400)

def login():
    data = request.json

    if not isinstance(data, dict):
        return abort(400)

    if 'nickname' not in data or 'password' not in data:
        return abort(400)

    user_nickname = data['nickname']
    user_password = data['password']

    with connection.cursor() as sql:
        sql.execute("SELECT * FROM `users` WHERE username = %s", user_nickname)
        result = sql.fetchall()
        
        if len(result) == 0:
            print(f"Could not find user with nickname {user_nickname}!")
            return abort(400)
        
        sql.execute("SELECT username FROM `users` WHERE username = %s", user_nickname)
        nick = sql.fetchone()

        sql.execute("SELECT password FROM `users` WHERE username = %s", user_nickname)
        pasw = sql.fetchone()
    
    if nick['username'] == user_nickname and pasw['password'] == user_password:
        print(f"Logged in as {user_nickname}!")
        return {'ok': True}
    else:
        print("Error!")
        return abort(400)




if __name__ == '__main__':
    
    HOST = '127.0.0.1'
    PORT = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            handle_client(conn, addr)