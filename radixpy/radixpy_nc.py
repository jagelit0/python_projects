#!/usr/bin/env python3
import requests, argparse, mmh3, codecs, re, json, urllib.parse
from bs4 import BeautifulSoup

def banner():
    print("""
                _ _      ____        
  _ __ __ _  __| (_)_  _|  _ \ _   _ 
 |  __/ _  |/ _  | \ \/ / |_) | | | |
 | | | (_| | (_| | |>  <|  __/| |_| |
 |_|  \__,_|\__,_|_/_/\_\_|    \__, |
                               |___/  v1.0    
    """)


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
        print("[+] TARGET TO SCAN:", targetHost)

        if args.favicon_url:
            favHas(targetFavicon)

        if args.target:
            allSubdomains(target, targetHost, outFile)
    except:
        print("[!] Something went wrong!")


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
    print("[+] Favicon Hash:",favHash)
  

# All Subdomain
def crtSh(targetHost):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0"}
    subLst = []
    crtQuery = requests.get("https://crt.sh/?q="+targetHost+"&output=json", headers=headers)
    crtResp = crtQuery.text
    subDict = json.loads(crtResp)
    for i in subDict:
        subLst = i['name_value'].split("\n")

    stSubs = set(subLst)

    for i in stSubs:
        print("[crtsh]",i) 

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
        print("[webarchive]",i)

    if not stWebArch:
        print("[!] Subdomains not found in webArchive")
    else:
        return stWebArch

# Dnsdumpster
def DnsDumpster(targetHost):
	url = "https://dnsdumpster.com/"
	headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0", "Referer": "https://dnsdumpster.com"}

	r = requests.get(url, headers=headers)

	soup = BeautifulSoup(r.text.strip(), "html.parser")

	tag = soup.find("input", {"name":"csrfmiddlewaretoken"})
	csrftoken = tag['value']
	headers = {
		"Referer":"https://dnsdumpster.com",
		"Cookie": "csrftoken={0};".format(csrftoken)
	}

	data = {"csrfmiddlewaretoken": csrftoken, "targetip": targetHost, "user": "free"}
	r = requests.post("https://dnsdumpster.com", headers=headers, data=data)
	ssoup = BeautifulSoup(r.text, "html.parser")


	tmpLst = []
	for tr in ssoup.find_all('table'):
		for td in tr.find_all('td'):
				tmpLst.append(td.text.strip().split("\n"))

	dnsLst = []
	pattern = "[0-9a-zA-Z\-]*." + targetHost
	for i in tmpLst:
		x = re.findall(pattern, str(i))
		if i == x:
			dnsLst.append(str(x))

    # ARREGLAR
	stDns = set(dnsLst)
    
	for i in stDns:
		print("[dnsdumspter]",i)

	if not stDns:
		print("[!] Subdomains not found in Dnsdumpster")
	else:
		return stDns

# All Subdomains
def allSubdomains(urlTarget, targetHost, outFile):
    urlTarget = ""
    allSubs = []

    # Crt.sh
    allCrts = crtSh(targetHost)
    for subA in allCrts:
        allSubs.append(subA)

    # Web Archive
    allWebArchive = webArchive(targetHost)
    for subB in allWebArchive:
        allSubs.append(subB)

    allDnsDumpster = DnsDumpster(targetHost)
    for subC in allDnsDumpster:
        allSubs.append(subC)

    stSubs = set(allSubs)

    if outFile:
        with open(str(outFile), "w") as f:
            for i in stSubs:
                f.write(i+"\n")
        print("Output saved in", outFile)
    return stSubs


if __name__ == "__main__":
    main() 