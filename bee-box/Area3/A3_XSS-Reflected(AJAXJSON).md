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

## medium, high

```php+HTML
        if($_COOKIE["security_level"] == "1")
        {

            // Generates the JSON output
            header("Content-Type: text/json; charset=utf-8");

        }
```

medium 과 high 단계에는 `Content-Type` 을 명시하고 있다.

header("Content-Type: text/json; charset=utf-8");

`Content-Type` 는 리소스(보내는 자원)의 형식을 명시하는 Http Header 이다.

`Content-Type: text/json`  으로 명시하여 스크립트를 주입하여도 문자열로 취급된다.

<br><br>

![vmware_WkfG7xfReh](https://user-images.githubusercontent.com/79683414/138540456-3e71cd9c-44d0-4e73-a310-fab66365363c.png)

<br><br>

## Thoughts

지금 까지 웹 공격을 막는 수단으로 htmlspecialchars, mysql_real_string, addslash 와 같은 필터링 함수를 접해왔다. 위의 함수들로 인젝션 공격을 막을 수 있었다.

하지만 이번 문제에서는 `Content-Type` 헤더를 이용했다. 헤더를 이용한 문제는 이번에 처음 접했는데, 전달되는 데이터 타입 명시를 통해 공격을 차단했다.

이전에 학습한 SQL PDO 와 같은 맥락으로, 사용자 입력값을 문자열로 처리해버린다는 공통점이 있어서 재밌었다.

필터링과 Http Header 를 적절히 이용하면 웹 인젝션 공격으로 부터 좀 더 안전할 것 같다.
