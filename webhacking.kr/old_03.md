## old_03

![vmware_uUztj1O4d9](https://user-images.githubusercontent.com/79683414/142836028-d3ef1575-79f0-45c1-9223-43752e9555a4.png)



![vmware_SbUJGtREbC](https://user-images.githubusercontent.com/79683414/142836057-0c4a4726-d446-48f5-8c54-eb438194e033.png)

<br>

음...색칠한 칸에 따라 _answer 값이 세팅 되어 전송되는듯 한데... 일단 로직을 풀어보자.

<br>

![vmware_uhLk1jpCe9](https://user-images.githubusercontent.com/79683414/143677446-d1240777-fc22-4f91-b006-b42812f53315.png)

<br>

![vmware_GoTZSHuy4J](https://user-images.githubusercontent.com/79683414/143677454-e7932afb-2032-464b-8e7b-b34a65421d17.png)

<br>

? 풀렸다. input 으로 POST 로 보내는 데이터는 위와 같이 answer, id 이다.

id 에 ` ' or 1=1 # ` 를 시도했지만 실패, answer 에 해봤더니

<br>

![vmware_p7r8VxfjEV](https://user-images.githubusercontent.com/79683414/143677491-1dee103d-11e8-4455-9d71-de2d18b7ce24.png)

![vmware_IrjUzvWQpv](https://user-images.githubusercontent.com/79683414/143677528-ae5f493d-2ef5-473e-816e-848d89ef7b89.png)

<br>

해결!!
