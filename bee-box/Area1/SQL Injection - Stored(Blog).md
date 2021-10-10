## SQL Injection - Stored(Blog)

![chrome_wuOnomlgrf](https://user-images.githubusercontent.com/79683414/135780326-f2844cbc-31d4-43f5-a705-955b89bd7d5c.png)

<br>

최상단에는 Entry 를 입력하게 되어있고 Owner, Date, Entry 를 데이터베이스에 저장하여 표 형식으로 출력하고 있다. 확인해 보니 Entry 입력란에 Html injection 이 가능했고 SQL injection 도 가능했다. #2 의 Enrty는 이전에 실습했던 Html_injection(post) 이다.

![chrome_GKH0nGpCjG](https://user-images.githubusercontent.com/79683414/135780655-73ba4bf8-7138-49d4-9601-3b66209d7580.png)

<br><br>

## low

![chrome_LVwtuBdj99](https://user-images.githubusercontent.com/79683414/135780754-40fe4f68-8e3d-4ae0-a4a3-5e0f3106e682.png)

SQL injection 이 가능한지 확인하기 위해 `'` 를 입력했는데, `'bee')'` 근처에서 문법 오류가 발생했다는 오류 메세지가 출력된다. 여기서 사용된 SQL Query를 추측해 보자면 DB에 데이터를 추가하는 구조이므로,

<br>

INSERT INTO ????(???) VALUES (...., '<user_input>', 'bee');

<br>

위와 같을 것이다. 좀 더 확실히 하기 위해 `'user` 를 입력했다.

![chrome_vR0XTiFvpG](https://user-images.githubusercontent.com/79683414/135781231-c2d483f9-1448-459b-a773-a3c9a58082f5.png)

<br><br>

다수의 정보를 한번에 노출시킬 수 있는 SELECT 문과 다르게 INSERT 문은 1행만 가능하다는 것, 이 문제에서는 하나의 Column 만 가능하다는 것을 염두해 두고 Injection을 수행해보자.

<br>

INSERT ??? INTO VALUSE(..., '<user_input>', 'bee') 이므로 `(select ~~~)`로 원하는 정보를 출력할 수 있을 것이다.

<br>

', (SELECT password from bWAPP.users where id=1 limit 0,1))#

![chrome_QzzlaDRBCL](https://user-images.githubusercontent.com/79683414/135782403-0af7e55b-1cbd-4f3e-bb38-e0e241e65218.png)

<br><br>

이전 문제들을 통해 테이블에 관한 정보를 알고 있었기에 위와 같은 Injection 이 가능했지만, 위와 같은 노가다성? Injection 문제는 `sqlmap` 을 활용하는 것이 편하다.



```bash
sqlmap -u "<URL>" --cookie="<cookie>" --data "<parameter>" --[dbs|table|columns] --dump
```

<br>

![vmware_MvT1FQgNNw](https://user-images.githubusercontent.com/79683414/135783743-93a74d48-3540-4178-9323-167924774743.png)
![vmware_Xkg5YZ80Z5](https://user-images.githubusercontent.com/79683414/135783746-9e1a6874-d1f4-4737-b78b-6297a135a82f.png)

`sqlmap` 은 편하다. 그 대가는...

<br><br>

![chrome_jp8nlnqU5k](https://user-images.githubusercontent.com/79683414/135783814-572ab949-a5bb-4e71-8480-6838801ae4d7.png)

테스트 query 들이 모두 저장되서 혹시 모르니 한번 정리했다....

