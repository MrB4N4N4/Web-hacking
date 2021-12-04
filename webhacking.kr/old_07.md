## old_07

![vmware_gk8mvelHTh](https://user-images.githubusercontent.com/79683414/144386112-8ab29d2d-fe38-4c5e-b95b-0261dd9090c7.png)

```php+HTML
<?php
$go=$_GET['val'];
if(!$go) { echo("<meta http-equiv=refresh content=0;url=index.php?val=1>"); }
echo("<html><head><title>admin page</title></head><body bgcolor='black'><font size=2 color=gray><b><h3>Admin page</h3></b><p>");
if(preg_match("/2|-|\+|from|_|=|\\s|\*|\//i",$go)) exit("Access Denied!");
$db = dbconnect();
$rand=rand(1,5);
if($rand==1){
  $result=mysqli_query($db,"select lv from chall7 where lv=($go)") or die("nice try!");
}
if($rand==2){
  $result=mysqli_query($db,"select lv from chall7 where lv=(($go))") or die("nice try!");
}
if($rand==3){
  $result=mysqli_query($db,"select lv from chall7 where lv=((($go)))") or die("nice try!");
}
if($rand==4){
  $result=mysqli_query($db,"select lv from chall7 where lv=(((($go))))") or die("nice try!");
}
if($rand==5){
  $result=mysqli_query($db,"select lv from chall7 where lv=((((($go)))))") or die("nice try!");
}
$data=mysqli_fetch_array($result);
if(!$data[0]) { echo("query error"); exit(); }
if($data[0]==1){
  echo("<input type=button style=border:0;bgcolor='gray' value='auth' onclick=\"alert('Access_Denied!')\"><p>");
}
elseif($data[0]==2){
  echo("<input type=button style=border:0;bgcolor='gray' value='auth' onclick=\"alert('Hello admin')\"><p>");
  solve(7);
}
?>
```

<br>

코드를 해석해보면 GET으로 val 변수의 값을 받아와서 sql 쿼리를 날리는 동작을 한다.

쿼리의 결과값이 2 일 때 문제가 풀리는 듯 하다.

<br>
rand(1,5) 에 따라 쿼리의 `()` 부분이 달라지는데, 확률은 1/5 이니 몇번 시도하면 뚤릴 것이다.

<br>

쿼리에 Regular Expressiong 으로 필터링 하는 함수  preg_match 가 사용되는데

예시로 `" or 1=1 # ` 을 입력해봤다.

<br>

_https://regexr.com/_

![chrome_JiwFZaKC27](https://user-images.githubusercontent.com/79683414/144386675-b2892aa4-cac4-4ab4-9df0-b25b158861a2.png)

정규표현식을 테스트할 수 있는 페이지 인데,

위와 같이 마우스를 on 하면 설명도 나와서 매우 편리하다.

`2, -, +, from, _, *, /, 공백문자` 를 피터링한다.

<br>

공백문자 필터링은 `()` 로 우회할 수 있다.

결과 값을 2로 만들기 위한 쿼리문을 생각해보면 아래와 같다.

0)union(select(char(50)))#

<br>

쿼리를 날려봤는데 Bad Request 가 자꾸 떠서 "#" 와 마지막의 ")" 를 빼주었다.(rand=1 일 때 쿼리를 기준으로)

<br>

완성된 쿼리는 다음과 같을 것이다.

`select lv from chall7 where lv=( __0)union(select(chr(50))__  )

<br>

3번 째 시도에 풀렸다.

![vmware_TDOwrXgAB1](https://user-images.githubusercontent.com/79683414/144704656-a17d0977-be4a-4557-b559-3fecb5ba1a64.png)

<br><br>

