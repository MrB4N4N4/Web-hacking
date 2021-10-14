## XSS-Reflected(GET/POST)

![vmware_Q2xxycwagt](https://user-images.githubusercontent.com/79683414/137242590-cca1bd58-9283-4760-96ac-b90fd6928fbc.png)

GET 과 POST 문제는 Request method 가 다를 뿐, 풀이 방식에 차이가 없어 같이 작성했다.

이전 인젝션 문제들 처럼, First namd/Last name 입력란이 있다.

XSS-Reflected 이므로 Input 에 스크립트를 인젝션 할 수 있을 것 같다.

<br><br>

## low

인젝션이 가능한지 체크해보기 위해 아래와 같이 입력했다.

"<script>alert("Succeed");</script>"

<br>

![vmware_Z6vAitLK1H](https://user-images.githubusercontent.com/79683414/137243146-4a54c141-2d55-4906-aee5-36e96c08103c.png)
![vmware_37qQlK9mPI](https://user-images.githubusercontent.com/79683414/137243188-41cfe318-bfb7-4e3b-bce2-10e80ab61349.png)

<br>

결과는 성공. 이전 XSS-Stored 문제처럼 악성 사이트로 접속을 유도할 수 있고 세션/쿠키 등의 탈취도 가능하다.

<br><br>

## medium

low 와 같은 입력을 시도했지만 실패했다. 지금 까지 공부한 인젝션 방어 기법을 생각해 보면 어떠한 필터링이 작용하고 있는듯 하다.

cookie 값을 출력하도록 입력해보자.

"<script>alert(document.cookie);</script>"

<br>

![vmware_o2gcp8Mte3](https://user-images.githubusercontent.com/79683414/137243933-e30cf0c7-168d-4314-9d0f-e3c4117dbf73.png)
![vmware_yxt9JzzV2V](https://user-images.githubusercontent.com/79683414/137243937-3f526270-c01e-4739-8529-f6d8f4a3a2b4.png)

<br><br>

cookie 출력은 성공했다. 그렇다면 위의 두 스크립트의 차이첨은 뭘까.

필터링이 전자의 것에만 작욯했다는 뜻인데 두 스크립트

"<script>alert("Succeed");</script>"

"<script>alert(document.cookie);</script>"

가장 눈에 띄는 차이점은 `"` 이다. String.fromCharCode() 는 정수를 문자로 바꿔주는 JS의 함수이다.

이를 이용해 필터링을 우회해보자.

"<script>alert(String.fromCharCode(83,117,99,99,101,101,100,33));</script>"

<br>

![vmware_cfKY6Y6KT9](https://user-images.githubusercontent.com/79683414/137244598-f17c2621-61bb-4194-9d9a-3bed789c2f80.png)
![vmware_sDGODalpW8](https://user-images.githubusercontent.com/79683414/137244606-102c2548-819b-4178-aa3c-320bddd793c0.png)

<br><br>



지금 까지 공부한 내용에 의하면,

Html, xml, SQL 등등 인젝션 공격 기법들은 대부분 필터링을 제대로 적용하면 방어할 수 있다. Bee-Box의 High 단계에도 대부분 htmlspecialchars,  mysqli_real_escape_string 과 같은 필터링 함수가 적용되어있다.

인젝션 공격이 가능한 곳은 __사용자의 Input__ 이다. 고급진 단어로 "공격 벡터"라고 부르기도 하는데 Input을 중점으로 필터링이 제대로 구현되어 있는지 테스트하면 된다.

