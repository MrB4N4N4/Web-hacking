## Broken Auth-Insecure Login Forms

![chrome_8NEsVGwJ5O](https://user-images.githubusercontent.com/79683414/136742423-f87a39c4-a8c0-4b60-bfbe-354e7843f168.png)

이번 문제는 HTML 과 JS는 브라우저의 관리자 도구를 통해 그대로 노출된다는 사실을 알려준다. 따라서 노출되면 안되는 코드는 php를 이용하거나 HTML, JS 이외의 것을 이용해야 할 것 같다.

<br><br>

## low

관리자 도구(F12)로 코드를 살펴보면 HTML의 코드로 login 과 password 가 그대로 노출되어 있다.

![chrome_iRQ0mNBr73](https://user-images.githubusercontent.com/79683414/136742942-2ceab9e3-4805-45a0-87d3-0628158bf5ca.png)

<br><BR>

## medium

![chrome_W1O4EE4riI](https://user-images.githubusercontent.com/79683414/136745905-8288daef-02f8-4b2a-9cf7-b6ab11a0f353.png)

<br>

![chrome_7jJs3KtHqD](C:\Users\MrBanana\Documents\ShareX\Screenshots\2021-10\chrome_7jJs3KtHqD.png)

medium 에서는 Name 에 "brucebanner"가 세팅되어있다. 

low 단계처럼 Name 은 노출되어 있지만 Passphrase 는 그렇지 않다.

위의 HTML 코드를 통해 몇 가지 추측해보면,

getElementById("passphrase") 또는 documnent.forms.passphrase 등의 형태로 변수가 전달될 것이고 unlock_secret()  함수가 실행될 것이다.

"Ctrl+F" 로 unlock_secret 을 찾아보자.

<br><BR>

![chrome_cYRDCzvkTm](https://user-images.githubusercontent.com/79683414/136747146-0edf10a9-fd2f-45b8-b3e6-07d4035b2204.png)

JS 코드로 그대로 노출되어 있다;; 복사해서 콘솔에 입력해보자.

<br><BR>

![chrome_2eR9mmc4PO](https://user-images.githubusercontent.com/79683414/136747414-f89495da-2391-48c8-841c-03b4b5990d1f.png)

secret을 SO Easy 하게 GET 했다.

high 단계에는 위의 두 단계처럼 민감한 정보가 노출되어 있지 않았다. 브루트 포싱 말고는 방법이 없어보인다.....

<br><br>

웹 취약점을 분석할 때,

input/from 형태를 먼저 확인하고 "Ctrl+F" 검색기능도 잘 활용하면 분석시간을 단축시킬 수 있을 것 같다.