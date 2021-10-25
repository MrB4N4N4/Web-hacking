## XSS-Reflected(HREF)

![vmware_YkgwV9Vpvm](https://user-images.githubusercontent.com/79683414/138577183-8d852b21-63f1-4cf3-9e71-0afd65425f7e.png)
![vmware_Bz7THodtUv](https://user-images.githubusercontent.com/79683414/138577187-d0cd1d9d-5110-481a-8f01-411a955b56dc.png)



XSS-Reflected 문제중 HREF 속성을 이용한 문제이다.

첫 페이지의 입력란에 이름을 입력하게 되어있고 Continue 버튼을 누르면

영화목록과 투표를 하는 기능이 구현된 페이지가 뜬다.

HREF 속성을 이용하는 문제이므로 "Vote" 링크와 관련되어 있을 것 같다.

우선, 문제를 풀기 전 알아두어야 할 개념들이 있다.

<br><br>

## HREF ?

HREF은 Html 태그의 속성 값 중의 하나로 URL을 명시할 때 쓰인다.

이번 문제에서 사용된 `<a>` 태그를 예로 들면 아래와 같다.

__`<a href="www.google.com">Vote</a>`__

`<a>` 태그는 다른 문서로 이동할 때 사용하는 태그이다. JS 로는

__location.href="www.google.com"__과 같은 동작을 한다.

<br><br>

## HTML DOM?

DOM (Document Object Model)은 웹 페이지에 대한 프로그래밍 인터페이스로, Html의 요소들로 이루어진 트리 이다.

웹 페이지는 Html > DOM > Rendering 의 과정을 걸쳐서 표시가 되는데

DOM 은 HTML 태그들이 노드 트리 방식으로 표현된다. 이 DOM 을 이용해 콘텐츠, 구조, 스타일 등을 조작할 수 있는, JS 로 접근이 가능한 API 가 제공된다.

지금까지 사용하고 있었던 "document.alert" 등이 DOM 의 API 이다.

HTML 태그가 DOM 으로 변환될 때, "브라우저"가 <u>유효하지 않은 코드들을 올바르게 수정</u>한다.

<br><br>

## low

처음엔 입력란에 스크립트 공격이 가능한지, 필터링이 구현되어 있는지 테스트하기 위해 alert 문을 시도했다.

![vmware_WIXynNl9iZ](https://user-images.githubusercontent.com/79683414/138577246-8f0e5c90-9887-48b4-9092-2a604f1cac80.png)
![vmware_fKoRmbSELA](https://user-images.githubusercontent.com/79683414/138577247-dcbdb0d7-5ec5-45bd-9eaf-31c4c8524cbe.png)

<br><br>

???

<br>

입력한 내용이 페이지에 반영되었다. 일단 브라우저의 관리자 도구를 이용해 소스를 살펴보자. 

![vmware_S5PBF1YUnK](https://user-images.githubusercontent.com/79683414/138624204-848bbf0b-504a-417b-8c65-5375efac07c2.png)

<br>

입력했던 스크립트가 기묘한 형태로 들어가있다. 여기서 드는 의문점은

- name=<script"> 부분.
- `</script>` 닫는 태그가 사라짐.
- 웹 페이지에 alert 부분부터 Vote 까지 표시됨.

<br><br>

Html 이 DOM 으로 변환되기 전 상태를 생각해보면 아래와 같다.

![Code_jOxbfvIIDv1](https://user-images.githubusercontent.com/79683414/138630349-0873f1cf-6832-4ca2-ae36-75f7f49dd61b.png)

![chrome_yOkZFoHHg1](https://user-images.githubusercontent.com/79683414/138630428-a7de9ab4-b7f4-4712-8831-a6d3066acbc9.png)

<br><br>

직접 테스트 해본 결과도 문제와 동일하게 출력하고 있다. 결과를 통해 유추해보면

`<a>` 태그의 닫히는 지점이 `script>` 이고 이후의 문자는 스크립트로 인식되지 않고

"Hello world"처럼 단순 문자열로 출력되고 있다는 것을 알 수 있다. 

즉, `<a>` 태그가 닫혀버려서 alert 부터 출력되고 닫는 html 태그는 웹 페이지에 표시되지 않아서 위와 같은 결과가 되었다. 정리하면 아래와 같다.

![Code_jOxbfvIIDv](https://user-images.githubusercontent.com/79683414/138631648-c183dd6d-c0ac-497e-a1f5-01f729b6619d.png)

<br><br>

조금 더 간단히 하면, 아래와 같은 상황이다.

![chrome_gX12wntuEc](https://user-images.githubusercontent.com/79683414/138631823-88a54f74-870f-41c3-90dd-9f445df5ee4a.png)

<br><br>

원리를 알았으니 이제 페이로드를 수정하면 된다.

여기서 이용할 것은 DOM Event 의 `onmouseover` 속성이다.

DOM Event 속성은 Html event 에 반응하기 위해 JS 를 실행할 수 있다.

<br>

<br>

__0 onmouseover=alert("success") a__

<br>

![Code_jGFWp6hJNg](https://user-images.githubusercontent.com/79683414/138634331-50df1edc-be51-4213-8427-2b6d8d3eed1b.png)

<br><br>

위와 같이 입력한 후 Continue 를 누르면 Vote 링크에 마우스를 올리기만 해도 Success 가 표시 될 것이다.

![vmware_lW5Fuo4nh6](https://user-images.githubusercontent.com/79683414/138634528-6c954d27-62a9-4b3d-b63b-a110142d6bd1.png)

<br>

위에서 DOM을 설명할 때 JS 로 DOM에 접근할 수 있다고 언급하였는데,

아래와 같이 DOM 에 직접 접근하여 페이지를 이동할 수도 있다.

<br>

__0 onmouseover=alert(document.location="https://www.google.com") a__
