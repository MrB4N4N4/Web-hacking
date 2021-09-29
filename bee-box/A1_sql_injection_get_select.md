## SQL Injection(GET/Select)

![chrome_vdaaRznMEb](https://user-images.githubusercontent.com/79683414/135188493-f4b39626-71e0-4272-a921-26f875c3128b.png)

<br><br>

SQL Injection(GET/Search)에 이어 (GET/Select)형태의 SQL Injection 을 수행해보자.

기본적인 개념은 Search 와 동일하다.

위 두 형태의 차이점은 Search 는 문자열 입력이 들어가고 Select 는 정수형 입력이 들어간다는 것이다.

<br><br>

## low

Select 공격시 URL 의 movie 변수에 인젝션을 수행하면 되는데 페이로드는 다음과 같다.

` 0 union select 1,2,3,4,5,6,7`

<br>

??? Search 에서는 `'` 으로 Injection 했는데 왜 Select 에서는 안쓰지 ???

정수형 입력이라는 것을 염두해 두면 간단히 이해할 수 있다. 각 문제에 해당하는 Query를 보자.

<br>

_Search_

SELECT ??? FROM movies WHERE title='<user_input>'

<br>

_Select_

SELECT ??? FROM movies WHERE id=<user_input>

<br><br>

이제 정수형 입력에서 `'`은 필요 없다는 것이 확실하게 이해됬다.

따라서, 공격 방법은 Search에서 했던 것과 동일하되, `'` 만 빼주면 된다.

![chrome_AIfu8R5cx4](https://user-images.githubusercontent.com/79683414/135192139-b1be173f-1e04-4cb7-9109-64b08a08c329.png)

## medium/high

medium 단계에는 Select의 mysql_real_escape_string() 이 적용되어있고

high는 새로운 내용이었다. high 단계에서는 "header(Location:sqli_2-ps.php)"가 적용되어있는데 해당 코드를 살펴보자.

