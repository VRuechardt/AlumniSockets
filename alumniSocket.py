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
            c.execute("SELECT id FROM users WHERE email = ?", (result[0][0],))
            r = c.fetchone()
            client.update({'id': r[0]})
            conn.close()
        else:
            server.send_message(client,"error width autentication")
            conn.close()
    elif message['task'] == 'msg':
        broadcastMessage(client['id'],message['id'] ,message['message'])

def broadcastMessage(userID, conversationID, message):
    conn = sqlite3.connect("../alumniBackend/alumni.db")
    c = conn.cursor()
    c.execute("SELECT userID FROM conversationparticipants WHERE conversationID = ?", (conversationID,))
    #c.execute("INSERT INTO ")
    conversationMembers = [v[0] for v in enumerate(c.fetchall())]
    print conversationMembers
    #nicht 2
    #if userID in conversationMembers:
    for i in server.clients:
        if i['id'] in conversationMembers and i['id'] is not userID:
            server.send_message(i,message)

server = WebsocketServer(9001)
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
server.run_forever()
