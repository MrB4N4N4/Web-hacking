import urllib.request

# 쿼리문 수행
def inject(query):
    url = "https://webhacking.kr/challenge/web-03/index.php"
    req = urllib.request.Request(url)
    res = urllib.request.urlopen(req)
    read = str(res.read().decode("utf-8")).split()
    time = list(map(lambda x: int(x), read[2].split(":")))
    return (60 * time[1]) + time[2]


MAX = pow(2, 25)

while MAX:
    MAX =- 1
    str(bin(MAX))[2:]