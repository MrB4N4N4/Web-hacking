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

