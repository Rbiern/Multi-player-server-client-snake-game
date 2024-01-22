import socket
import threading
import pygame
import re
import rsa

server_addr = "localhost"
server_port = 5555

width = 500
rows = 20
msgList = ["Congratulations!", "It Works!", "Ready?"]

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP
try:
    client_socket.connect((server_addr, server_port))
except socket.error as e:
    print("Could not connect to server.")
    exit(1)

window = pygame.display.set_mode((width, width))

rgb_colorss = {
    "(255, 0, 0)" : (255, 0, 0),
    "(0, 255, 0)" : (0, 255, 0),
    "(0, 0, 255)" : (0, 0, 255),
    "(255, 255, 0)" : (255, 255, 0),
    "(255, 165, 0)" : (255, 165, 0),
}


def drawGrid(window):
    sizeBtwn = width // rows
    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(window, (255, 255, 255), (x, 0), (x, width))
        pygame.draw.line(window, (255, 255, 255), (0, y), (width, y))


def drawNewFrame(window, serverMsg, flag):
    if flag:
        return
    window.fill((0, 0, 0))
    drawGrid(window)
    serverMsg = serverMsg.split("|")

    #draw the green foods cubes
    list2 = re.findall("[0-9]+", serverMsg[1])
    col_green = []
    row_green = []
    for i, value in enumerate(list2):
        if i % 2 == 0:
            row_green.append(int(value))
        else:
            col_green.append(int(value))

    for i in range(len(col_green)):
        pygame.draw.rect(window, (10, 255, 10), (25* row_green[i], 25 * col_green[i], 25 - 1, 25 - 1))

    # draw the snakes and get thier colours
    list1 = serverMsg[0].split("**")
    list3 = serverMsg[2].split("**")
    j = 0
    cords = []
    for i in list1:
        cords.append(re.findall("[0-9]+", list1[j]))
        j += 1

    idx = 0
    for l in cords:
        list1 = cords[idx]
        cube_color = rgb_colorss[list3[idx]]
        idx += 1
        col_snake = []
        row_snake = []
        for i, value in enumerate(list1):
            if i % 2 == 0:
                row_snake.append(int(value))
            else:
                col_snake.append(int(value))
        eyes = True
        for i in range(len(col_snake)):
            pygame.draw.rect(window, cube_color, (25* row_snake[i], 25 * col_snake[i], 25 - 1, 25 - 1))
            if eyes:
                dis = width // rows
                centre = dis // 2
                radius = 3
                circleMiddle = (row_snake[i] * dis + centre - radius, col_snake[i] * dis + 8)
                circleMiddle2 = (row_snake[i] * dis + dis - radius * 2, col_snake[i] * dis + 8)
                pygame.draw.circle(window, (0, 0, 0), circleMiddle, radius)
                pygame.draw.circle(window, (0, 0, 0), circleMiddle2, radius)
                eyes = False

    pygame.display.update()


def inputs(client_socket, ServerKey):
    flag = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        # check if event is a key pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                client_socket.send((rsa.encrypt("up".encode(), ServerKey)))
            elif event.key == pygame.K_a:
                client_socket.send((rsa.encrypt("left".encode(), ServerKey)))
            elif event.key == pygame.K_s:
                client_socket.send((rsa.encrypt("down".encode(), ServerKey)))
            elif event.key == pygame.K_d:
                client_socket.send((rsa.encrypt("right".encode(), ServerKey)))
            elif event.key == pygame.K_e:
                client_socket.send((rsa.encrypt("get".encode(), ServerKey)))
            elif event.key == pygame.K_r:
                client_socket.send((rsa.encrypt("reset".encode(), ServerKey)))
            elif event.key == pygame.K_z:
                client_socket.send((rsa.encrypt(msgList[0].encode(), ServerKey)))
            elif event.key == pygame.K_x:
                client_socket.send((rsa.encrypt(msgList[1].encode(), ServerKey)))
            elif event.key == pygame.K_c:
                client_socket.send((rsa.encrypt(msgList[2].encode(), ServerKey)))
            elif event.key == pygame.K_q:
                client_socket.send((rsa.encrypt("quit".encode(), ServerKey)))
                flag = True

            return flag


def getMsg():
    dupMsgCheck = ""
    while True:
        try:
            serverMsg = client_socket.recv(2048).decode()
            if "User" in serverMsg:
                print(serverMsg)
                continue
            if dupMsgCheck == serverMsg :
                drawNewFrame(window, serverMsg, True)
            else:
                drawNewFrame(window, serverMsg, False)
            dupMsgCheck = serverMsg

        except:
            print("socket of thread will terminate")
            break


def main():
    ServerKey = rsa.key.PublicKey.load_pkcs1(client_socket.recv(1024), format='DER')
    print(f"Client connected to server at {server_addr}:{server_port}")
    serverOutput = threading.Thread(target=getMsg)
    serverOutput.start()
    client_socket.send((rsa.encrypt("get".encode(), ServerKey)))

    clock = pygame.time.Clock()
    runtime = True

    while runtime:
        pygame.time.delay(100)
        clock.tick(60)
        flag = inputs(client_socket, ServerKey)
        if flag:
            runtime = False
        else:
            client_socket.send((rsa.encrypt("get".encode(), ServerKey)))

    print("Client Closing..........")
    pygame.quit()
    client_socket.close()


if __name__ == "__main__":
    main()