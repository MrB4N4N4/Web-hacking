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

`SELECT ???? FROM movies? WHERE titel='<user_input>';`

<br>

<br>

따라서 Input 에 `' or 1=1` 을 입력하면 해당 테이블의 모든 튜플이 출력될 것이다.

하지만 해당 테이블에는 추가적으로 노출되는 정보가 없어서 적절하지 않다.

<br>

<br>

'or'을 이용한 공격은 "해당"테이블(movies?)의 모든 튜플을 출력하지만,

UNION을 이용하면 " __원하는 테이블__ "의 정보를 출력할 수 있다.

<br>