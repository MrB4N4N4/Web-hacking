## old_08

```php+HTML
<?php
$agent=trim(getenv("HTTP_USER_AGENT"));
$ip=$_SERVER['REMOTE_ADDR'];
if(preg_match("/from/i",$agent)){
  echo("<br>Access Denied!<br><br>");
  echo(htmlspecialchars($agent));
  exit();
}
$db = dbconnect();
$count_ck = mysqli_fetch_array(mysqli_query($db,"select count(id) from chall8"));
if($count_ck[0] >= 70){ mysqli_query($db,"delete from chall8"); }

$result = mysqli_query($db,"select id from chall8 where agent='".addslashes($_SERVER['HTTP_USER_AGENT'])."'");
$ck = mysqli_fetch_array($result);

if($ck){
  echo "hi <b>".htmlentities($ck[0])."</b><p>";
  if($ck[0]=="admin"){
    mysqli_query($db,"delete from chall8");
    solve(8);
  }
}

if(!$ck){
  $q=mysqli_query($db,"insert into chall8(agent,ip,id) values('{$agent}','{$ip}','guest')") or die("query error");
  echo("<br><br>done!  ({$count_ck[0]}/70)");
}
?>
```

<br>

위의 코드의 핵심을 요약하면 아래와 같다.

1. User-Agent 값을 가져와 공백을 제거한 후 $agent 에 저장.
2. $agent 에 "from" 문자열이 있는지 검사
3. $agent 가 존재하는지 DB에 쿼리 실행. addslash()로 `', ", \, NULL`  필터링
4. 존재하지 않으면 Insert 문 실행.

3번의 결과가 "admin" 이면 해결된다.

<br>

처음에는 UNION 을 이용해 인젝션을 시도했다. User-Agent 값을 조작해야 하므로 Burp suite 를 이용했다.

<br>

__%aa' union select 0x61646d696e #__

<br>

`%aa`'  는 addslash 를 우회하는 용도이다. `%aa'`은 addslash 로 인해  `%aa\'` 가 되고

멀티바이트 환경(2바이트로 문자 표현)에서 위의 값이 인코딩 될 때 `%aa%5c'`

%aa 와 %5c("\\") 가 1개의 문자로 변환된다.

0x616... 은 "admin" 이다.

<br>

하지만 결과는 "query error". 다른 방법을 찾아야 한다.

두 번째 쿼리에는 addslash 가 없다.

..

..

!!!

<br>

![vmware_T2r62NmMIH](https://user-images.githubusercontent.com/79683414/144740246-10cebdb4-984c-496a-8747-40143e1c04df.png)

위와 같이 입력하게 되면

__insert into chall8(agent,ip,id) values('banana', '1', 'admin'), ('guest', 'ip', 'guest')__

agent 값이 `banana` 이고 id 값이 `admin` 인 튜플을 삽입할 수 있다.

<br>

![vmware_DtfkJrioze](https://user-images.githubusercontent.com/79683414/144740396-80db26c9-e943-4eea-b63a-a9f820476e26.png)

<br>

이제 User-Agent 에 "banana" 값을 전달해주면 해결이다.

