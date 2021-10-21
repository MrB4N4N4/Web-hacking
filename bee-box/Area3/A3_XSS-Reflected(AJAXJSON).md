## A3_XSS-Reflected(AJAX/JSON)

![vmware_O0qBhoeMgn](https://user-images.githubusercontent.com/79683414/138206639-72290ce2-0188-49a5-b067-a2f096d4edf3.png)

<br>

AJAX 는 부분만 동적 처리가 가능한 비동기적 기술이다.

"Search for a movie: " 에 값을 입력하면 전체 페이지가 Reload 되지 않고 즉각적으로 결과를 출력해준다.

<br><br>

## low



인젝션 공격을 수행하기 위해 URL 과 title 에 테스트를 해봤지만 성공하지 못했다.

정보를 좀 더 알아내기 위해 Burp Suite 로 패킷을 분석해봤는데 문제의 페이지는

"bWAPP/xss_ajax_2-1.php"이지만,

"GET Request" 를 "xss_ajax_2-2.php" 로 보내고 있었다....

![vmware_GFLkyhvGPX](https://user-images.githubusercontent.com/79683414/138208573-397bc337-bfbd-42d2-8c6d-47c2861d7aa4.png)

<br><br>

URL을 2-2로 바꿔주고 title 파라매터에 인젝션을 수행했더니 성공했다.

<br>

## medium

