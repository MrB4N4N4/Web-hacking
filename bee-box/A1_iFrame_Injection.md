## iFrame Injection

iframe은 html 문서 안에 또 하나의 html 문서를 출력한다. 예를 들면 구글 홈페이지에 네이버 홈페이지 frame 을 띄울 수 있는 것이다. iframe의 크기를 0으로 하면 보이지 않는 iframe 을 삽입 할 수 있다.

</br>

## iframei.php

![chrome_G8gKT0nJW4](https://user-images.githubusercontent.com/79683414/133544870-f1955fe9-8635-4a8f-a30a-f69a06978742.png)

URL을 보니 GET 방식이다.

robots.txt 를 출럭하는 페이지이다.

<br/>

<br/>

<br/>

<br/>

### low

```php
<iframe frameborder="0" src="<?php echo xss($_GET["ParamUrl"])?>" height="<?php echo xss($_GET["ParamHeight"])?>" width="<?php echo xss($_GET["ParamWidth"])?>"></iframe>
```

코드를 보니 `ParamUrl` 은 주소를 받아오고 `ParamHeight` 와 `ParamWidth`는 크기를 지정한다.

xss() 는 low에서 아무런 동작을 하지 않는다. `src` 속성에는 URL 이 입력되므로

/bWAPP/robots.txt 파일을 불러온다는  것을 알 수 있다. 따라서 `ParamUrl` 변수에 원하는 값을 넣어 iframe 을 삽입할 수 있다.

<br/>

<br/>

<br/>

<br/>

ifram에 다른 웹의 주소를 삽입해 봤는데 'connection refused'가 떠서

/bWAPP 에 bad.html을 만들어서 테스트 했다.

아래와 같이 `ParamUrl`을  bad.html로 바꿔서 악성 iframe 을 띄울 수도 있고

![chrome_fcm9gTYp21](https://user-images.githubusercontent.com/79683414/133552113-b1efb738-7ae6-41d0-b80d-5396c7b488f2.png)

<br/>

<br/>

<br/>

<br/>

"robots.txt " 뒤에 아래의 payload를 이용해서 임의의 iframe 을 삽입할 수 있다.

![chrome_wvfEK4i4FM](https://user-images.githubusercontent.com/79683414/133551452-df2476d4-f7ed-4ec8-8ae5-00ba67171c93.png)

<br/>

<br/>

![explorer_VBcj6WE3No](https://user-images.githubusercontent.com/79683414/133551623-eef8751a-eafa-4989-a7ce-360dc0a60a22.png)

<br/><br/><br/><br/>

## medium

