#!/usr/bin/env python3

import posixpath
import re
import requests
from bs4 import BeautifulSoup
import argparse
from colorama import Fore, Back



def banner():
    print(Fore.LIGHTCYAN_EX + """
                      _ _     _ ______             
           _         | | |   | (____  \       _    
      ____| |_   ____| | |   | |____)  ) ___ | |_  
     / ___)  _) / ___) | |   | |  __  ( / _ \|  _) 
    ( (___| |__| |   | | |___| | |__)  ) |_| | |__ 
     \____)\___)_|   |_|\______|______/ \___/ \___) v1.0                              
    """ + Fore.RESET)

def getUrl(targetUrl):
    r = requests.get(targetUrl)
    return r


def getLoot(targetUrl):
    soup = BeautifulSoup(targetUrl.text, 'html.parser')

    #Loot Response Headers
    lstHeaders = []
    if "Server" in targetUrl.headers:
        lstHeaders.append("Server: " + targetUrl.headers["Server"])
        #print("Server:", targetUrl.headers["Server"])
    if "X-Powered-By" in targetUrl.headers:
        lstHeaders.append("X-Powered-By: " + targetUrl.headers["X-Powered-By"])
        #print(targetUrl.headers)
    if "X-AspNet-Version" in targetUrl.headers:
        lstHeaders.append("X-AspNet-Version: " + targetUrl.headers["X-AspNet-Version"])

    if not lstHeaders:
        print(Fore.RED + "\n[!] NO RESPONSE HEADERS FOUND" + Fore.RESET)
    else:
        print(Fore.GREEN + "\n[+] RESPONSE HEADERS FOUND:" + Fore.RESET) 
        for i in lstHeaders:
            print("",i)


    #Loot HTML Comments
    lstComments = []
    comments= re.findall('<!--(.*)-->', str(targetUrl.text))
    for c in comments:
        lstComments.append(c)

    stComments = set(lstComments)

    if not stComments:
        print(Fore.RED + "\n[!] NO COMMENTS FOUND" + Fore.RESET)
    else:
        print(Fore.GREEN + "\n[+] COMMENTS FOUND:" + Fore.RESET) 
        for i in stComments:
            print("",i)


    #Loot URLs
    lstUrls = []
    for tag_a in soup.find_all("a", href=True):
        cleanUrls = tag_a['href']
        if "http" in cleanUrls:
            lstUrls.append(cleanUrls)

    stUrls = set(lstUrls)

    if not stUrls:
        print(Fore.RED + "\n[!] NO URLS FOUND" + Fore.RESET)
    else:
        print(Fore.GREEN + "\n[+] URLS FOUND:" + Fore.RESET)
        for i in stUrls:
            print("",i)


    #Loot Dirs
    lstDirs = []
    for dirs in soup.find_all('a', href=True):
        dirpath = posixpath.dirname(dirs['href'])
        if dirpath.count("/") >= 2 and "http" not in dirpath:
            lstDirs.append(dirpath)

    stDirs = set(lstDirs)

    if not stDirs:
        print(Fore.RED + "\n[!] NO DIRS FOUND" + Fore.RESET)
    else:
        print(Fore.GREEN + "\n[+] DIRS FOUND:" + Fore.RESET)
        for i in stDirs:
            print("",i.strip())
            

    #Loot Contacts
    lstEmails = []
    emails = soup.find_all('a', href=True)
    for email in emails:
        if "mailto:" in email['href']:
            lstEmails.append(email.text)

    stEmails = set(lstEmails)

    if not stEmails:
        print(Fore.RED + "\n[!] NO EMAILS FOUND" + Fore.RESET)
    else:
        print(Fore.GREEN + "\n[+] EMAILS FOUND:" + Fore.RESET)
        for i in stEmails:
            print("",i)



if __name__ == "__main__":
    # PARSE ARGS
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", required=True, type=str, help="Set target to scan")


    args = parser.parse_args()

    targetUrl = args.target


    # Variables
    target = getUrl(targetUrl)

    # Start
    banner()
    print(Back.BLACK + Fore.RED + "[+] TARGET TO SCAN:" + Fore.RESET + Back.RESET, targetUrl)
    getLoot(target)
 
    