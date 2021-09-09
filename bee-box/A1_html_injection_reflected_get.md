## HTML injection



웹 어플리케이션에 필터링 기능이 미흡할 시 공격자가 악의적인 데이터를 주입하여 발생되는 취약점.

`Reflected` 는 악성 스크립트를 주입한 동시에 결과가 반영된다. _반사된 것 처럼_

`Stored` 는 악성 스크립트를 서버에 _저장_ 후 다른 사용자(피해자)가 접근 시 공격이 수행된다.

## Reflected(GET)



#### **low**

아무런 필터링이 없어 악성 스크립트 주입이 가능하다.

![vj3QxtkP18](https://user-images.githubusercontent.com/79683414/132443902-48467661-941e-4052-b470-ce644770c19a.png)

![RQKUpqk1Ag](https://user-images.githubusercontent.com/79683414/132444632-31557f14-6496-4fa3-bc26-179e413fac4f.png)



#### **medium**

low 와 같은 페이로드를 입력했을 때의 결과이다.

![RVOCWOAjSK](https://user-images.githubusercontent.com/79683414/132601777-571bb19a-8a19-474f-96df-3d58555a76cf.png)

입력한 내용이 그대로 출력된다. 어떤 식의 필터링이 작용한 듯 한데 소스코드를 살펴보자.

