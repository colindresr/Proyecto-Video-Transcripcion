import json
from http.cookiejar import MozillaCookieJar

def guardar_cookies():
    with open("cookies.json", "r", encoding="utf-8") as f:
        cookies = json.load(f)

    jar = MozillaCookieJar("cookies.txt")
    for c in cookies:
        jar.set_cookie(create_cookie(c))
    jar.save()

def create_cookie(c):
    from http.cookiejar import Cookie
    return Cookie(
        version=0,
        name=c["name"],
        value=c["value"],
        port=None,
        port_specified=False,
        domain=c["domain"],
        domain_specified=True,
        domain_initial_dot=c["domain"].startswith("."),
        path=c["path"],
        path_specified=True,
        secure=c.get("secure", False),
        expires=c.get("expirationDate", None),
        discard=False,
        comment=None,
        comment_url=None,
        rest={"HttpOnly": c.get("httpOnly", False)},
        rfc2109=False
    )

if __name__ == "__main__":
    guardar_cookies()
