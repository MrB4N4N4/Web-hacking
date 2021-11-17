## XML/XPath Injection(Login Form)

![vmware_XOd6H4cDTi](https://user-images.githubusercontent.com/79683414/136135201-cc9e221f-c1bc-45e5-bdec-f26f0fa2e7d1.png)



![vmware_7VwGMEMLSc](https://user-images.githubusercontent.com/79683414/136135309-07e273fe-eabb-4ea8-a82a-a7d54001a6cd.png)

XML Injection 문제도 SQL 과 같이,  `'` 를 입력했을 때의 오류메세지를 통해 공격이 가능한지 판단 할 수 있다.

id 에 `'` 를 입력했을 때 위와 같이 XPath 관련 에러가 발생한다.

<br><br>

## XML, XPATH?

```xml
<?xml version="1.0" encoding="UTF-8"?>
<heroes>
	<hero>
		<id>1</id>
		<login>neo</login>
		<password>trinity</password>
		<secret>Oh why didn't I took that BLACK pill?</secret>
		<movie>The Matrix</movie>
		<genre>action sci-fi</genre>
	</hero>
	<hero>
		<id>2</id>
		<login>alice</login>
		<password>loveZombies</password>
		<secret>There's a cure!</secret>
		<movie>Resident Evil</movie>
		<genre>action horror sci-fi</genre>
	</hero>
	<hero>
		<id>3</id>
		<login>thor</login>
        		.
        		.
        		.
```

XML 은 데이터를 트리 구조의 노드로 표현한 것이다. XML 태그를 따라가다 보면 그 안에 값이 있다. XML의 데이터를 이용하기 위해 XPATH 를 이용하는데 XML용 쿼리라고 보면 된다.

xmli_1.php 를 보면 XPATH 를 어떻게 이용하는지 알 수 있다.

<br>

```php
$xml = simplexml_load_file("passwords/heros.xml");

$result = $xml->xpath("/heroes/hero[login='" . $login . "' and password='" . $password . "']")
```

<br><br>

xml파일을 불러와서 xpath()로 데이터를 추출하고 있다. 위의 xpath 를 해석해보자면 다음과 같다.

<br>

heroes 의 자식노드 중 " [ ] "내부의 조건이 맞는 hero 를 반환한다.

<br><br>

[XPATH 의 명령어]

| `/`      | 모든 노드 조회                 |
| -------- | ------------------------------ |
| `//`     | 현재 노드로부터 모든 노드 조회 |
| `*`      | 모든 노드 조회                 |
| `.`      | 현재 노드                      |
| `..`     | 현재 상위 노드                 |
| `parent` | 현재 노드의 부모 노드          |
| `child`  | 현재 노드의 자식 노드          |
| `[]`     | 조건문                         |
| `node()` | 현재 노드로부터 모든 노드 조회 |



<br><br>

## low

```php
login='" . $login . "' and password='" . $password . "'
```

xmli_1.php 에 사용된 xpath 조건문 이다. xml의 주석은 `<!-- -->`와 같은 형태이므로 sql 인젝션에서 처럼 사용할수는 없을 것 갔다. $login 과 $password 에 사용자 입력을 대입해 보면서 우회할 방법을 생각해보자.

<br>

login : __'or 1=1 or'__, password = 1

login=' __'or 1=1 or'__ ' and password='1'

<br>

<br>

![vmware_Lyw1uu7O77](https://user-images.githubusercontent.com/79683414/136308269-4ee65647-72cf-4e36-a72f-53a72e748442.png)

or 보다 and 의 우선순위가 높기 때문에 위의 결과는 항상 True 가 될 것이다. 그 결과로 Neo 로 로그인을 성공했다. 이를 이용해 Blind SQL Injection에서 했던 것처럼 데이터를 추측해보자.

<br><br>

parent 노드의 이름은 heroes 이므로

__login : neo' and string-length(name(parent::*))=6 or '____

__passsword : 1__

<br>

위와 같이 입력하면 결과는 True 가 된다.

![Typora_fFzLsamkBq](https://user-images.githubusercontent.com/79683414/136309736-ea57a19b-5b84-4fa5-8fed-f8b7d3eccf52.png)

![vmware_Lyw1uu7O77](https://user-images.githubusercontent.com/79683414/136308269-4ee65647-72cf-4e36-a72f-53a72e748442.png)

<br><BR>

SQL 처럼 substring() 도 사용할 수 있다.

__neo' and substring(name(parent::*), 1, 1)='h' or '__

<BR><BR>

## medium, high

이 두 단계에서 xml injection 공격을 막기 위해  str_replace() 를 사용하고 있다.

```php
    $input = str_replace("(", "", $data);
    $input = str_replace(")", "", $input);
    $input = str_replace("=", "", $input);
    $input = str_replace("'", "", $input);
    $input = str_replace("[", "", $input);
    $input = str_replace("]", "", $input);
    $input = str_replace(":", "", $input);
    $input = str_replace(",", "", $input);
    $input = str_replace("*", "", $input);
    $input = str_replace("/", "", $input);
    $input = str_replace(" ", "", $input);
```

<br><br>

SQL injection 처럼 별도의 함수로 구현되어있지는 않는 듯 하다.

