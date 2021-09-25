## Server-Side Includes Injection

SSI는 HTML 페이지의 동적인 부분을 간단하게 처리하기 위한 기능이다.

예를 들면 방문자 이름, 방문자 수, 날짜 등을 표시할 때 위 기능을 이용하기도 한다.

SSI를 사용하려면 "SSI 지시어"를 이용해야 하는데,

이 지시어를 처리하기 위한 '.shtml' 확장자 파일을 생성한다.

SSI 지시어는 다음과 같다.

```bash
<!--#element attribute=value-->
```

ex)  <!--#echo var="DATE_LOCAL"-->

<br/>

<br/>

<br/>

![chrome_OvMbOtXp20](https://user-images.githubusercontent.com/79683414/134750698-6b8f686e-bdf4-409e-b9f1-a448292cd159.png)




## low

![chrome_RZZ1HC97Ne](https://user-images.githubusercontent.com/79683414/134751333-25a729cc-7db1-4ac4-9dd3-7fc52455c408.png)

'.shtml' 확장자 파일을 확인할 수 있다.

SSI 기능이 잘 동작하는지, 지시어를 입력해보자.

<br/>

<br/>

<br/>

SSI : `<!--#echo var="DATE_LOCAL"-->`

![chrome_hzIZhFMbtN](https://user-images.githubusercontent.com/79683414/134751460-58148c4e-cd72-4581-96d1-ce8763f13967.png)
![chrome_bs7pj8lv10](https://user-images.githubusercontent.com/79683414/134751468-cbd9a288-8e4b-4378-8f91-aab1ba702c1f.png)

<br/>

<br/>

<br/>

SSI 기능이 제대로 동작하고 있다.

'exec'를 이용하면 원하는 명령을 입력할 수 있다.

```bash
<!--#exec cmd="ls"-->
<!--#exec cmd="whoami"-->
...
```

![chrome_wZVolFT5MY](https://user-images.githubusercontent.com/79683414/134751699-e7caa795-28ab-4719-9fdd-3803f38fa8fe.png)
![chrome_i8ZX6iUBmN](https://user-images.githubusercontent.com/79683414/134751703-b249d531-66fc-487d-8b41-28d51eb0c651.png)

<br/>

<br/>

<br/>

SSI Injection 도 앞의 OS Command Injection 이나 PHP Injection 과 마찬가지로,

리버스 쉘을 이용해 쉘 획득이 가능하고 'htmlspecialchars()' 로 막을 수 있다.