import argparse
import requests
import re
from pyfiglet import Figlet
from concurrent.futures import ThreadPoolExecutor
import threading
import time

f = Figlet(font='roman')
print(f.renderText('\nDrupal\nKiller'))


def versionfind(changelog_text):
    pattern = r'Drupal (\d+\.\d+), (\d{4}-\d{2}-\d{2})'
    matches = re.findall(pattern, changelog_text)
    
    if matches:
        version, date = matches[0]
        print("\n[+] Possible Drupal version : "+version)
    else:
        print("\n[-] Version Not Found")


def adminfind():
    with open('paths.txt', 'r') as file:
        adminurl = [line.strip() for line in file]
    for path in adminurl:
        response = requests.get(url+path)
        if response.status_code == 200:
            if path == "/CHANGELOG.txt":                
                print("\n[+] CHANGELOG.txt ",url+path)
                versionfind(response.text)
            elif path == "/admin/login":
                print("\n[+] Default Admin Panel ",url+path)
            elif path == "/user/login":
                print("\n[+] Default Login Panel ",url+path)
            elif path == "/web.config":
                print("[+] Web.config ",url+path)
            elif path == "/LICENSE.txt":
                print("[+] LICENSE.txt ",url+path)
            elif path == "/xmlrpc.php":
                print("[+] xmlrpc.php ",url+path)
            elif path == "/update.php":
                print("[+] update.php ",url+path)

def modulesenum():
    plugins_base_url = ["/sites/all/modules/","/sites/default/modules/","/modules/contrib/","/modules/"]
    
    with open("plugins.txt","r") as f:
        modurl = [line.strip() for line in f]
    
    def check_module(mod, modpath):
        response = requests.get(url + mod + modpath)
        """for i in range(1, 4):
            print("taranıyor" + "." * i, end='\r')
            time.sleep(1) """
        #print("Scanning Modules...")
        if response.status_code == 200:
            print("[+] ", url + mod + modpath)
    
    with ThreadPoolExecutor(max_workers=int(thread)) as executor:
        for mod in plugins_base_url:
            for modpath in modurl:
                executor.submit(check_module, mod, modpath)
def main():
    adminfind()
    modulesenum()

if __name__ == "__main__":
    argp = argparse.ArgumentParser()
    argp.add_argument("-u", "--url", required=True, help="Enter Url")
    argp.add_argument("-t", "--thread", required=True, help="Enter MAX thread")
    args = vars(argp.parse_args())
    
    url = args["url"]
    thread = args["thread"]
    
    main()

