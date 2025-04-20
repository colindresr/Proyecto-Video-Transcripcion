import json

with open("cookies.json", "r") as f:
    cookies = json.load(f)

with open("cookies.txt", "w") as f:
    for cookie in cookies:
        f.write(
            f"{cookie['domain']}\t"
            f"{str(cookie.get('hostOnly', False)).upper()}\t"
            f"{cookie['path']}\t"
            f"{str(cookie.get('secure', False)).upper()}\t"
            f"{int(cookie['expirationDate'])}\t"
            f"{cookie['name']}\t"
            f"{cookie['value']}\n"
        )
