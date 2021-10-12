## Session Mgmt - Session ID in URL

![vmware_koK7Chqkon](https://user-images.githubusercontent.com/79683414/136905420-8b88e3b8-7fef-4012-be9b-15d260a0ba85.png)

제목 그대로 세션 ID 가 URL 에 그대로 노출되어 있다. Burp Suite를 이용해 세션을 획득해보자.

<br>

## Cookie?

쿠키는 클라이언트(사용자) 로컬에 저장되는 데이터, 브라우저가  자동으로 Header에 넣어서 서버에 전송함. 사용자 개별의 데이터를 저장하는 용도.

ex) 자동 로그인, 쇼핑몰의 장바구니, "오늘 더 이상 이 창을 보지 않음" ...

<br><br>

## Session?

세션은 쿠키 기반이지만 사용자 정보 데이터(Session ID)를 "서버"에 저장. 클라이언트를 구분하기 위한 용도. 즉, 다른 사용자의 세션 ID 값을 이용해 "서버"에게 다른 사용자인 척 접근을 할 수 있다. (단 세션은 유효 시간이 있으므로 세션이 유효할 때만 가능)

<br><BR>

## low

우선 URL 에 노출된 Session ID 값을 복사하자.

![RIgRVBhTjn](https://user-images.githubusercontent.com/79683414/136911662-5fc9ec40-45ff-4587-8ecf-44acd5f22e78.png)

<br><br>

Burp Suite 로 새로운 브라우저를 실행하고 복사해 두었던 Session ID 값을 로그인 Request에 입력해준 후  "smgmt_sessionid_url.php"에 POST 요청을 보냈다.

![vmware_DYx4JDhZAE](https://user-images.githubusercontent.com/79683414/136912783-f1c8686a-8840-4db5-a2e8-86a6889007f2.png)

<br><br>

forward 후 session id 값을 한번 더 입력했다.

![vmware_vxEPtqiAch](https://user-images.githubusercontent.com/79683414/136913049-51e088f7-9fc6-4816-bf9c-e59795438966.png)

<br><br>

![vmware_UtLprBlLe9](https://user-images.githubusercontent.com/79683414/136913339-1d229991-c909-44ba-b140-9c58360fa322.png)

해당 세션으로 성공적으로 접속했다. 