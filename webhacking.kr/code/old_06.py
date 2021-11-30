import base64

username = "admin".encode("ascii")
password = "nimda".encode("ascii")


def enc_replace(txt):
    txt.replace("1", "!")
    txt.replace("2", "@")
    txt.replace("3", "$")
    txt.replace("4", "^")
    txt.replace("5", "&")
    txt.replace("6", "*")
    txt.replace("7", "(")
    txt.replace("8", ")")
    return txt


def dec_replace(txt):
    txt.replace("!", "1")
    txt.replace("@", "2")
    txt.replace("$", "3")
    txt.replace("^", "4")
    txt.replace("&", "5")
    txt.replace("*", "6")
    txt.replace("(", "7")
    txt.replace(")", "8")
    return txt


for _ in range(20):
    username = base64.b64encode(username)
    password = base64.b64encode(password)

username = dec_replace(username.decode())
password = dec_replace(password.decode())

print("[Encrypt]")
print("username: ", username)
print("password: ", password)

username = enc_replace(username)
password = enc_replace(password)

for _ in range(20):
    username = base64.b64decode(username)
    password = base64.b64decode(password)

print("[Decrypt]")
print("username: ", username.decode())
print("password: ", password.decode())
