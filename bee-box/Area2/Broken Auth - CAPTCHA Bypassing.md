## Broken Auth - CAPTCHA Bypassing

![vmware_wPoQF6yhf9](https://user-images.githubusercontent.com/79683414/136682947-9e97c832-b8c7-4b00-a604-27d216e9a556.png)

Broken Auth는, 인증 및 세션 관리 결함을 이용해 사용자 권한 획득이 가능한 취약점으로 OWASP Top10 A2(취약한 인증과 세션 관리)에 해당하는 내용이다. 해당 문제를 살펴보니 Credential + CAPTCHA 로 이루어져 있다. 이번 문제는 "Reload" 나 "Login" 버튼을 누를 경우에만 CAPTCHA 값이 갱신되는 취약점으로 low, medium, high 전부 공격이 가능하다.

<br><br>

공격 방식은 Burp suite 를 이용한 Brute force 으로 CAPTCHA 값이 변하지 않는 점을 이용해 Login 과 Password 에 무차별 대입 공격을 하는 것이다. 우선 잘못된 ID, PW 를 입력했을 때의 문자열"Invalid credentials~~~"을 복사해두자.

![vmware_aUodpJDd26](https://user-images.githubusercontent.com/79683414/136684489-132690b9-0d69-4169-81a9-a47c320e4e81.png)

<br><br>

Burp suite 를 켜서 패킷을 intercept 한 후 Intruder 로 보냈다. Intruder는 패킷에 페이로드를 지정해서 원하는 데이터를 대입할 수 있어 Brute force 공격을 할 때 매우 유용한 기능이다.

![vmware_kmxe7vsnK8](https://user-images.githubusercontent.com/79683414/136685278-e39b4c6b-a740-4ee5-9de2-2832c699a7f9.png)

<br>

<br>

Positions 탭에서 Attack type 은 Cluster bomb 로 설정, payload는 login 과 password로 지정해줬다.

![vmware_JPqfwCpmab](https://user-images.githubusercontent.com/79683414/136685375-f61ad151-4840-4859-872b-dcea3debfd02.png)

<br>

<br>

payloads 탭에서 각각의 페이로드에 대입할 값들을 Add 한다. 실제 Brute force의 경우 Dictionary 파일을 사용한다.

![vmware_kjOCW3dh02](https://user-images.githubusercontent.com/79683414/136685400-68904c77-cad5-4a2a-b3d7-39b547e4a360.png)

<br><br>

Options 탭에서

공격에 성공했을 경우를 구분하기 위해, 실패했을 때의 문자열을 Add해 주다. 패킷에 문자열이 지정해둔 문자열이 포함되어 있으면 알려주는 기능이다.

![vmware_jpzQkqJRGx](https://user-images.githubusercontent.com/79683414/136685432-e5d55218-e92b-4486-8b76-9ca187c5aee7.png)

<br><Br>

![vmware_srRf1x8TGX](https://user-images.githubusercontent.com/79683414/136685633-c620aead-1bb3-4224-8c44-719affe4fa5e.png)

"✅" 는 "Invalid cre~~~" 문자열을 포함하고 있다는 뜻이다.

따라서 bee/bug 가 로그인을 위한 crededtial 이다.

<br><Br>

이번 문제는 CAPTCHA 값이 "Reload", "Login" 을 버튼을 클릭했을 때만 갱신되어 발생한 취약점이었다. 갱신 타이밍을 바꾸거나 CAPTCHA를 이미지로 바꿔야 될듯 하다.

<br><br>

Brute Force 는 단순 대입이었기 때문에, 지금까지 배운 다른 공격들 보다는 재미가 없었다....