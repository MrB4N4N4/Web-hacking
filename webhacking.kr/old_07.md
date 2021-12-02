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

여기서 Regular Expressiong 으로 필터링 하는 함수  preg_match 가 사용되는데

예시로 `" or 1=1 # ` 을 입력해봤다.

<br>

_https://regexr.com/_

![chrome_JiwFZaKC27](https://user-images.githubusercontent.com/79683414/144386675-b2892aa4-cac4-4ab4-9df0-b25b158861a2.png)

정규표현식을 연습할 수 있든 페이지 인데,

위와 같이 마우스를 on 하면 설명도 나와서 매우 편리하다.

<br><br>

