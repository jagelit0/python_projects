#!/usr/bin/env python3
import requests, argparse, mmh3, codecs
import urllib.parse
import json
from colorama import Fore, Back

def banner():
    print(Fore.LIGHTBLACK_EX + """
                _ _      ____        
  _ __ __ _  __| (_)_  _|  _ \ _   _ 
 |  __/ _  |/ _  | \ \/ / |_) | | | |
 | | | (_| | (_| | |>  <|  __/| |_| |
 |_|  \__,_|\__,_|_/_/\_\_|    \__, |
                               |___/  v1.0    
    """ + Fore.RESET)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", type=str, help="Set target to scan")
    parser.add_argument("-f", "--favicon-url", type=str, help="Specify the favicon url")
    parser.add_argument("-o", "--output", type=str, help="Save output to a file")
    args = parser.parse_args()


    try:
        # Format args
        targetUrl = args.target
        targetFavicon = args.favicon_url
        outFile = args.output
        target = getUrl(targetUrl)
        targetHost = '.'.join(urllib.parse.urlparse(targetUrl).netloc.split('.')[-2:])

        banner()
        print(Back.BLACK + Fore.RED + "[+] TARGET TO SCAN:" + Fore.RESET + Back.RESET, targetHost)

        if args.favicon_url:
            favHas(targetFavicon)

        if args.target:
            allSubdomains(target, targetHost, outFile)
    except:
        print(Fore.RED + "[!] Something went wrong!" + Fore.RESET)


# Get url
def getUrl(urlTarget):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0"}
    r = requests.get(urlTarget, headers=headers)
    return r


# Favicon Hash
def favHas(urlTargetFav):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0"}
    r = requests.get(urlTargetFav, headers=headers)
    favicon = codecs.encode(r.content, "base64")
    favHash = mmh3.hash(favicon)
    print(Fore.GREEN + "[+] Favicon Hash:" + Fore.RESET,favHash)
  

# All Subdomain
def crtSh(targetHost):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0"}
    subLst = []
    crtQuery = requests.get("https://crt.sh/?q="+targetHost+"&output=json", headers=headers)
    crtResp = crtQuery.text
    subDict = json.loads(crtResp)
    for i in subDict:
        if (i['common_name'] not in subLst):
            subLst.append(i['common_name'])

    stSubs = set(subLst)
    for i in stSubs:
        print(Fore.GREEN + "[crtsh]" + Fore.RESET,i) 

    if not stSubs:
        print("[!] Subdomains not found in crt.sh")
    else:
        return stSubs

    
# Web Archive
def webArchive(targetHost):
    webLst = []
    webQuery = requests.get("https://web.archive.org/cdx/search/cdx?url=*."+targetHost+"&output=txt&fl=original")
    webResp = webQuery.text.splitlines()
    for host in webResp:
        targetHost = urllib.parse.urlparse(host).netloc
        webLst.append(targetHost)
    
    stWebArch = set(webLst)
    for i in stWebArch:
        print(Fore.GREEN + "[webarchive]" + Fore.RESET,i)

    if not stWebArch:
        print("[!] Subdomains not found in webArchive")
    else:
        return stWebArch

   
# All Subdomains
def allSubdomains(urlTarget, targetHost, outFile):
    urlTarget = ""
    allSubs = []

    # Crt.sh
    allCrts = crtSh(targetHost)
    for subC in allCrts:
        allSubs.append(subC)

    # Web Archive
    allWebArchive = webArchive(targetHost)
    for subA in allWebArchive:
        allSubs.append(subA)

    stSubs = set(allSubs)

    if outFile:
        with open(str(outFile), "w") as f:
            for i in stSubs:
                f.write(i+"\n")
        print(Fore.YELLOW + "Output saved in" + Fore.RESET, outFile)
    return stSubs


if __name__ == "__main__":
    main() 