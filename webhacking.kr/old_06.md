## old_06

![vmware_KfIUm4nKPt](https://user-images.githubusercontent.com/79683414/144009261-80316306-86b3-4731-84f1-04f1149f0b23.png)

<br>

?!

일단 뭔가 엄청나다. Source-view 를 확인해주자.



_view-source_

```php+HTML
<?php
include "../../config.php";
if($_GET['view_source']) view_source();
if(!$_COOKIE['user']){
  $val_id="guest";
  $val_pw="123qwe";
  for($i=0;$i<20;$i++){
    $val_id=base64_encode($val_id);
    $val_pw=base64_encode($val_pw);
  }
  $val_id=str_replace("1","!",$val_id);
  $val_id=str_replace("2","@",$val_id);
  $val_id=str_replace("3","$",$val_id);
  $val_id=str_replace("4","^",$val_id);
  $val_id=str_replace("5","&",$val_id);
  $val_id=str_replace("6","*",$val_id);
  $val_id=str_replace("7","(",$val_id);
  $val_id=str_replace("8",")",$val_id);

  $val_pw=str_replace("1","!",$val_pw);
  $val_pw=str_replace("2","@",$val_pw);
  $val_pw=str_replace("3","$",$val_pw);
  $val_pw=str_replace("4","^",$val_pw);
  $val_pw=str_replace("5","&",$val_pw);
  $val_pw=str_replace("6","*",$val_pw);
  $val_pw=str_replace("7","(",$val_pw);
  $val_pw=str_replace("8",")",$val_pw);

  Setcookie("user",$val_id,time()+86400,"/challenge/web-06/");
  Setcookie("password",$val_pw,time()+86400,"/challenge/web-06/");
  echo("<meta http-equiv=refresh content=0>");
  exit;
}
?>

<?php
$decode_id=$_COOKIE['user'];
$decode_pw=$_COOKIE['password'];

$decode_id=str_replace("!","1",$decode_id);
$decode_id=str_replace("@","2",$decode_id);
$decode_id=str_replace("$","3",$decode_id);
$decode_id=str_replace("^","4",$decode_id);
$decode_id=str_replace("&","5",$decode_id);
$decode_id=str_replace("*","6",$decode_id);
$decode_id=str_replace("(","7",$decode_id);
$decode_id=str_replace(")","8",$decode_id);

$decode_pw=str_replace("!","1",$decode_pw);
$decode_pw=str_replace("@","2",$decode_pw);
$decode_pw=str_replace("$","3",$decode_pw);
$decode_pw=str_replace("^","4",$decode_pw);
$decode_pw=str_replace("&","5",$decode_pw);
$decode_pw=str_replace("*","6",$decode_pw);
$decode_pw=str_replace("(","7",$decode_pw);
$decode_pw=str_replace(")","8",$decode_pw);

for($i=0;$i<20;$i++){
  $decode_id=base64_decode($decode_id);
  $decode_pw=base64_decode($decode_pw);
}

echo("<hr><a href=./?view_source=1 style=color:yellow;>view-source</a><br><br>");
echo("ID : $decode_id<br>PW : $decode_pw<hr>");

if($decode_id=="admin" && $decode_pw=="nimda"){
  solve(6);
}
```

<br>

위를 정리해보면

Cookie-user 값이 세팅되지 않았을 때, id/pw 를 guest/123qwe 로 세팅하고

base64_encode 를 20 회 수행한 후

str_replace 로 특정 문자를 변환한다.

<br>

그리고 Cookie-user,password 를 str_replace 로 다시 변환 하고

base64_decode 를 20 회 수행한다.

이때 값이 admin/nimda 이면 solve 되는 듯 하다.

> __base64란?__
>
> 바이너리를 "ascii 코드로 이루어진 64진법"으로 변환하는 것. 64 진법은 6bit 로 나타내기 때문에 패딩("==")이 필요함.
>
> 영문자(52) + 숫자(10) + 공백 + "/" = 64

<br><br>

생각보다 간단하군. 파이썬을 이용하자.

<br><br>

```python
import base64

username = "admin".encode("ascii")
password = "nimda".encode("ascii")


def enc_replace(txt):
    txt.replace("1", "!")
    txt.replace("2", "@")
    txt.replace("3", "$")
    txt.replace("4", "^")
    txt.replace("5", "&")
    txt.replace("6", "*")
    txt.replace("7", "(")
    txt.replace("8", ")")
    return txt


def dec_replace(txt):
    txt.replace("!", "1")
    txt.replace("@", "2")
    txt.replace("$", "3")
    txt.replace("^", "4")
    txt.replace("&", "5")
    txt.replace("*", "6")
    txt.replace("(", "7")
    txt.replace(")", "8")
    return txt


for _ in range(20):
    username = base64.b64encode(username)
    password = base64.b64encode(password)

username = dec_replace(username.decode())
password = dec_replace(password.decode())

print("[Encrypt]")
print("username: ", username)
print("password: ", password)

username = enc_replace(username)
password = enc_replace(password)

for _ in range(20):
    username = base64.b64decode(username)
    password = base64.b64decode(password)

print("[Decrypt]")
print("username: ", username.decode())
print("password: ", password.decode())

```

![pycharm64_rAcLgSLmV4](https://user-images.githubusercontent.com/79683414/144010709-8b95fe75-296e-4abf-8dd5-6d2acd549273.png)

<br>

결과값을 burp suite 를 이용해 보냈다.