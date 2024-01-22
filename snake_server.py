import threading
import numpy as np
import socket
from _thread import *
import rsa
from snake import SnakeGame
import uuid
import time

# server = "10.11.250.207"
server = "localhost"
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

counter = 0
rows = 20
global runFlag
funFlag = True

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

game = SnakeGame(rows)
game_state = ""
last_move_timestamp = time.time()
interval = 0.2
moves_queue = set()

(pubkey, privkey) = rsa.newkeys(1024)
a = pubkey.save_pkcs1(format='DER')
b = rsa.key.PublicKey.load_pkcs1(a, format='DER')


def game_thread():
    global game, moves_queue, game_state
    while True:
        last_move_timestamp = time.time()
        game.move(moves_queue)
        moves_queue = set()
        game_state = game.get_state()
        while time.time() - last_move_timestamp < interval:
            time.sleep(0.1)


rgb_colors = {
    "red" : (255, 0, 0),
    "green" : (0, 255, 0),
    "blue" : (0, 0, 255),
    "yellow" : (255, 255, 0),
    "orange" : (255, 165, 0),
}
rgb_colors_list = list(rgb_colors.values())


def sendToAll(msg, id):
    for client in clients:
        string = "User: " + str(id) + "  " + str(msg)
        client.send(string.encode())


def main(conn, addr) :
    global counter, game
    unique_id = str(uuid.uuid4())
    color = rgb_colors_list[np.random.randint(0, len(rgb_colors_list))]
    game.add_player(unique_id, color = color)
    rgb_colors_list.remove(color)
    conn.send(a)

    if len(clients) == 1:
        start_new_thread(game_thread, ())

    while True:
        d = conn.recv(2048)
        conn.send(game_state.encode())
        try:
            data = rsa.decrypt(d, privkey).decode()
        except:
            data = d.decode()
            pass

        move = None
        if not data:
            print("no data received from client")
            break
        elif data == "get":
            print("received get")
            pass
        elif data == "quit":
            print("received quit")
            game.remove_player(unique_id)
            break
        elif data == "reset":
            game.reset_player(unique_id)
        elif data in ["up", "down", "left", "right"]:
            move = data
            moves_queue.add((unique_id, move))
        else :
            send = threading.Thread(target=sendToAll, args=(data, unique_id))
            send.start()

    clients.remove(conn)
    conn.close()
    if not clients:
        print("interrupt received: shutting down\nserver shut down")
        s.close()


if __name__ == "__main__":
    clients = []
    runFlag = True
    while runFlag:
        try:
            conn, addr = s.accept()
            print("Connected to:", addr)
            clients.append(conn)
            clientConnection = threading.Thread(target=main, args=(conn, addr))
            clientConnection.start()
        except:
            break