## XSS-Stored(Blog)

![vmware_p4qp6kzyuH](https://user-images.githubusercontent.com/79683414/137084132-90e89102-5479-48da-bf32-66b60bb5eb94.png)

이전 Stored 문제들과 동일하게, User Input 을 받아서 데이터베이스에 저장하여 List를 출력하는 형태이다. 악성 스크립트를 주입하는 XSS 실습을 해보자.

<br><BR>

## XXS?

Cross-site Scripting은 악성 스크립트를 주입하여 악의적인 사이트로 이동하게 하거나 악성코드를 다운받게 하는 등의 행위로, 방식에 따라 Reflected, Stored, DOM Based 등으로 분류한다. 서버사이드 스크립트는 서버에서 직접 실행된다. 따라서 XSS 취약점은 서버에 전달되는 모든 변수 값에서 발생할 수 있다. 아래와 같은 간단한 JS 코드로 취약점이 발생하는지 확인할 수 있다.

```javasc
<script>alert("Succeed");</script>
```

<br><br>

## low

__Stored XSS__는 '대상 서비스 데이터베이스'에 악성 스크립트를 저장하여

사용자가 해당 스크립트에 접근할 때 마다 실행되기 때문에 불특정 다수를 대상으로 공격이 가능하다.

우선 XSS 이 가능한지 스크립트를 주입해보자.

![vmware_Jbb0yfa9XQ](https://user-images.githubusercontent.com/79683414/137086792-03ef06e5-981f-4b11-96e2-08b68818fd1d.png)

<br><br>

![vmware_2R3H8Jqn5w](https://user-images.githubusercontent.com/79683414/137086948-a5c3e4c9-f1c6-487d-bb76-90b819885b08.png)

스크립트가 성공적으로 실행된다. 스크립트는 bWAPP 데이터베이스에 저장되기 때문에 해당 스크립트에 접근 할 때 마다 위와 같은 alert이 발생한다. 다른 페이지에서 해당 스크립트에 접근해도 마찬가지이다.

<br><br>

