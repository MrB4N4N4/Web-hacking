## DB is really good

![](https://user-images.githubusercontent.com/79683414/133197533-0781e5e9-88a5-4958-893a-12dc57752232.png)

```
what kind of this database?
you have to find correlation between user name adn database.
```

<br/><br/><br/><br/>

이번엔 소스가 따로 제공되지 않았다.  여러가지 값을 테스트 했다.

- admin, root, ADMIN, .., /

<br/> <br/> <br/> <br/>



![chrome_Pqks3MmTXR](https://user-images.githubusercontent.com/79683414/133199970-fd66f64f-7eb9-4ae3-92de-e8253db6bd45.png)

![chrome_sjligDFjpv](https://user-images.githubusercontent.com/79683414/133200223-fce2b86e-7718-4490-bcbc-3cf9dc55d670.png)



![chrome_K0X7V0qwZh](https://user-images.githubusercontent.com/79683414/133200506-42e73e18-501d-413e-bdf4-1d124e6c0e0c.png)

![chrome_X2RcfUr6UR](https://user-images.githubusercontent.com/79683414/133200728-7a9559aa-beca-4c06-bb3c-aab4bede614f.png)

<br/> <br/> <br/> <br/>

__"/"를 입력했을 때 Fatal error 발생__

![SLNR6RbMRE](https://user-images.githubusercontent.com/79683414/133201208-3d327835-a5dc-4e74-8cf0-8db60f720b5f.png)

오류 내용을 살펴보면 db 파일 open 을 실패 한 듯 하다. 

 보아하니 USER 에 입력 한 값(input)이 `/db/wkrm_<input>.db` 형태로 DB를 open 한다.

그렇다면 처음에 막힌 admin의 DB명은  wkrm_admin.db 일 것이다.

<br/> <br/> <br/> <br/>

디렉토리 리스팅을 해보자. 선배들의 흔적을 볼 수 있다...

![chrome_JlR9EJZBs3](https://user-images.githubusercontent.com/79683414/133208186-3a37e565-edd8-4710-ba22-9c0e06cd956e.png)

<br/> <br/> <br/> <br/>

wkrm_admin.db 을 받아서 (검색하거나 URL에 입력) `notepad++`의 `hex-editor`로 열어봤다.

최하단에 flag의 정보가 있었다.

![notepad++_pFx2BM4ngi](https://user-images.githubusercontent.com/79683414/133209550-fdc1715b-99c5-4081-85be-25cf924843eb.png)

<br/> <br/> <br/> <br/>

한글로 "와우인증키숳".php 라고 되어있다. URL에 입력했더니 FLAG를 획득 할 수 있었다.
