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

이렇게만 하면 재미없으니 BeEF 를 이용해 XSS 공격의 위험성을 경험해보자. 

<br><br>

우선 Apache Document Root 인 /var/www/html 에 index.html 을 다음과 같이 교체한 후

(hook.js 는 BeEF의 후킹 파일이다.)

![vmware_iZwGTndLvZ](https://user-images.githubusercontent.com/79683414/137107886-00d03129-41df-4d63-8e8f-5d8dee45acc4.png)

Apache 를 재시작 했다.

```bash
sudo service apache2 restart
```

<br><br>

공격자의 웹에 접속하면 자동으로 BeEF의 hook 이 실행된다. 이로 인해 해당 웹에 접속하기만 해도 제어권이 빼앗겨버린다. ㄷㄷ;;

<br>

이제 bWAPP 에 악성 스크립트를 주입할 차례이다. 아래의 스크립트는 자동으로 공격자의 웹 서비스에 접속하도록 한다.

![vmware_GsAmVwqWEa](https://user-images.githubusercontent.com/79683414/137109562-0b3bbad5-69d1-4005-b9f9-9c1bbfafb3f7.png)

<br><br>

위에서 언급했듯, 이제 이 스크립트에 접근할 때 마다 악성 스크립트가 실행된다.

이제 BeEF 를 켜주자.

```bash
beef-xss
```

<br>

그 후 다른 호스트에서 bee-box를 접속해서 XSS blog 페이지로 이동해보자.

![Typora_wqyJvEAbs8](https://user-images.githubusercontent.com/79683414/137110796-4b207047-7130-42e6-9a3b-eed39a64e481.png)

![vmware_vf9KgsUK9A](https://user-images.githubusercontent.com/79683414/137111426-b03f592c-0a46-4b07-95ee-134511c94575.png)

<br>

<br>
미리 설정해둔 hook.js 가 성공적으로 실행되었고 BeEF 웹에 희생자 호스트가 후킹되었다고 표시된다. 후킹에 성공하면 아래와 같이 다양한 공격 커맨드를 실행시킬 수 있는데 Social Engineering 기법으로 위조된 페이지로 접속을 시켜보자.

![vmware_XBbDgd5dTR](https://user-images.githubusercontent.com/79683414/137112181-ccd2d416-9dfc-4b16-8a2a-393847298100.png)

![vmware_hvc20z3FMb](https://user-images.githubusercontent.com/79683414/137112236-0904c448-204e-43b0-8361-c656e6dd3de6.png)

<br><br>

Excute 클릭 시 호스트의 화면에 위조된 페이지가 뜬다 ㄷㄷ;;;

![chrome_TNmDjcGKF4](https://user-images.githubusercontent.com/79683414/137112339-2e9ed175-52a8-4d4d-8b73-27db0bfae1fb.png)
