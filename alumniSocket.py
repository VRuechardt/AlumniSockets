from websocket_server import WebsocketServer
import sqlite3
import json
def new_client(client, server):
    print("New client connected and was given id %d" % client['id'])
    server.send_message_to_all("Hey all, a new client has joined us")

def client_left(client, server):
    print("Client(%d) disconnected" % client['id'])

def message_received(client, server, message):
    message = json.loads(message)
    print("Client(%d) said: %s" % (client['id'], message['task']))
    if message['task'] == 'auth':
        conn = sqlite3.connect("../alumniBackend/alumni.db")
        c = conn.cursor()
        c.execute("SELECT email FROM users WHERE logincode = ?", (message['code'], ))
        result = c.fetchall()
        if len(result) is 1:
            client.update({'email': result[0][0]})
        else:
            server.send_message(client,"error width autentication")
    if message['task'] == 'msg':
        for i in server.clients:
            if i['email'] == message['email']:
                print('sending to: ', i['email'])
                server.send_message(i ,message['message'])

server = WebsocketServer(9001)
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
server.run_forever()
