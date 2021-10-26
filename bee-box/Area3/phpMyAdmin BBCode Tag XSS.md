## phpMyAdmin BBCode Tag XSS

![vmware_1QleYrhHOP](https://user-images.githubusercontent.com/79683414/138812258-06533466-42ed-4678-a10f-d70a3978daeb.png)

phpMyAdmin 은 MySQL을 웹 상에서 관리하기 위한 도구이다.

phpMyAdmin 의 버전 때문에 error.php 에서 BBCode 태그 입증에 실패했다고 하고

Hint 로 "CVE-2010-4480" 이 주어졌다.

BBCode 는 Html 의 기능을 일부 옮겨놓은 경량 마크업이라고 보면 된다.

BBCode 에서는 `<>` 대신 `[]` 를 이용한다.

<br>

[CVE-2010-4480]

![chrome_cyWLBuEPCz](https://user-images.githubusercontent.com/79683414/138814917-c06dd9a5-a5da-4a3d-a1c2-2c0047d9b576.png)

<br>

error.php 페이지에 [a@url@page]{text}[/a] 형태로 리다이렉트가 가능하다고 한다.

`[a]` 는 Html 의 `<a>` 와 같이 anchor 의 동작을 하는 것 같은데

BBCode tag reference 를 찾아봐도 `[a]`는 존재하지 않았다. `@` 도 마찬가지...

<br>

POC(Proof Of Concept)를 보면

<br>

![chrome_q1BZKvHumN](https://user-images.githubusercontent.com/79683414/138815765-6553b0c5-3669-466f-a591-8fc8d4df4c39.png)

<br>

error 파라매터에 Redirect 될 링크를 삽입하고 있다는 것을 알 수 있다.

<br>

__error=[a@https://www.google.com@]Let's google![/a]__

<br>

![vmware_F1W3sQ3fcN](https://user-images.githubusercontent.com/79683414/138816249-e047c143-d884-46b6-84fe-000df7471a63.png)

<br>

성공적으로 링크가 생성되고 Google 페이지로 Redirect 된다.

Error 페이지 이므로, 그럴듯한 오류내용과 링크를 위조(Falsification) 하면

사용자를 악성페이지로 유도할 수 있다.

아래는 POC 코드를 그대로 입력했을 때 이다.

![vmware_VA8mGBBAKH](https://user-images.githubusercontent.com/79683414/138816538-0c6d90a9-d6c3-4714-92d7-8416988f95ed.png)

<br>

위 취약점은 phpMyAdmin 3.3.8.1/3.3.9.0 버전에서 발생하므로 버전 업데이트를 하여

공격을 막을 수 있다.