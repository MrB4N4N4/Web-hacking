## md5 password_view-source

```php+HTML
<?php
 if (isset($_GET['view-source'])) {
  show_source(__FILE__);
  exit();
 }

 if(isset($_POST['ps'])){
  sleep(1);
  mysql_connect("localhost","md5_password","md5_password_pz");
  mysql_select_db("md5_password");
  mysql_query("set names utf8");
  /*
  
  create table admin_password(
   password char(64) unique
  );
  
  */

  include "../lib.php"; // include for auth_code function.
  $key=auth_code("md5 password");
  $ps = mysql_real_escape_string($_POST['ps']);
  $row=@mysql_fetch_array(mysql_query("select * from admin_password where password='".md5($ps,true)."'"));
  if(isset($row[0])){
   echo "hello admin!"."<br />";
   echo "Password : ".$key;
  }else{
   echo "wrong..";
  }
 }
?>
<style>
 input[type=text] {width:200px;}
</style>
<br />
<br />
<form method="post" action="./index.php">
password : <input type="text" name="ps" /><input type="submit" value="login" />
</form>
<div><a href='?view-source'>get source</a></div>
```

소스를 보니 sql injection 문제인듯 하다. `query` 부분을 보니 사용자의 입력값을 `mysql_real_escape_string()` 으로 필터링 후 md5()에 의해 변환된다.

- mysql_real_escape_string() 은 `\x00, \xn, \xr, \, ', ", \x1a` 를 필터링한다.
- md5(str, True) 는 md5의 raw 결과 값(binary)을 반환한다. ascii 로 출력됨.







__md5 예제__

![chrome_CKNii6GH58](https://user-images.githubusercontent.com/79683414/133011531-770025f1-c71f-4523-b621-f23e7480625a.png)

> __Reference__
>
> mysql_real_escape_string() - https://www.php.net/manual/en/function.mysql-real-escape-string.php
>
> md5() - https://www.php.net/manual/en/function.mysql-real-escape-string.php







password엔 __md5 결과값이 injection 문자열인 값__을 입력해야 하므로 사실상 필터링은 신경쓰지 않아도 된다. 즉, ascii 의 형태로 query 에 전달되므로 password 를 md5 한 결과 값이 `' or 1=1#`과 같은 형태, hex 값으로 변환하면 "27206f7220313d3123" 와 같을 것이다.

하지만, 위 조건에 부합하는 password 값을 발견하기 어려울 것이다. 좀 더 간결한 input 이 필요하다.





## False sql injection

간결한 input을 찾던 중 우연히`False sql injection` 자료를 읽게되었다. 아직 sql injection 의 지식이 콩만한 상태라 mysql 에서는 __False 값(0)을 넣어서 injection 이 가능하다__는 사실을 처음 알게 되었다. 

> False sql injection - https://blog.pages.kr/1237







_query: select * from admin_password where password=''_

__Key point__: 문자열이 저장되는 속성(id, passswd 같은)에 "0" 을 입력하면 테이블의 모든 내용이 출력된다. mysql 에서 0 = false, 나머지는 true 이다. 

어떤 원리로 '0'이 이런 동작을 하는지는 아직 잘 이해가 안된다. ~~형변환 오류?...~~

mysql은 내부적으로 문자열을 정수로 변환한다고 하는데... 혹시??







여러 input들을 테스트해보기 위해 mysql 에 적당한 테이블을 생성했다.







_user table_

![WindowsTerminal_um3Yr6nJHM](https://user-images.githubusercontent.com/79683414/133015153-ce4eae31-be83-4b4a-836f-c585d678daf4.png)



---



우선 기존의, 익숙한, True sql injection 을 입력했다.

_input : ' or 1=1 #_

![WindowsTerminal_cXI7bk8918](https://user-images.githubusercontent.com/79683414/133020801-61b4e43d-1b7b-4626-9c06-00abe78adf3e.png)

![WindowsTerminal_OofOInYcut](https://user-images.githubusercontent.com/79683414/133022279-b74da136-2184-4169-b34b-7ea951dff360.png)

Injection의 결과 값을 확인해봤다. DUAL(가상 테이블)을 이용한 방법도 있어서 참신했다.







위와 같이 결과 값이 True 가 될법한 input 을 확인해보자.

_input : 'or', '||'_

![WindowsTerminal_FVZC529rfR](https://user-images.githubusercontent.com/79683414/133023904-bb6becd4-2ac8-495a-bb36-d94790622773.png)



---

다음은 False injection 이다.

_input : 0_

![WindowsTerminal_9xh9WuZ9Ov](https://user-images.githubusercontent.com/79683414/133021018-64c9654b-477e-4260-be56-5b00f2a52610.png)







Wow... 







input 의 결과 값이 "0"인 경우도  injection 가능하다는 사실이 증명되었다.

_input : '=', 1234'='1234, 1234'='abcd_

![WindowsTerminal_ul3daYZ0KR](https://user-images.githubusercontent.com/79683414/133024174-bc160538-163f-444e-930c-99f0b56099ae.png)



## exploit

사용할 input 은 ` '=', 'or', '||' ` 이다. 비교적 간결하고 input의 양쪽에 어떤 값이 오더라도 결과값이 `Boolean`이 되기 때문이다.

![pycharm64_f62qr8Dta6](https://user-images.githubusercontent.com/79683414/133024434-b5e0cdbf-139a-4d08-b643-41bb80f51584.png)







input 값을 찾기 위해, 애용하는 파이썬을 사용했다. 코드는 다음과 같다

![pycharm64_27f8zIwatD](https://user-images.githubusercontent.com/79683414/133024767-d78268e7-7276-4a1c-992a-e0be56833bc3.png)
![pycharm64_aYWVN7TjjH](https://user-images.githubusercontent.com/79683414/133024771-20b2fd4c-53f7-4729-a7c3-4f04921e215f.png)



차례대로 테스트 하다 보면 모든 값이 성공하지는 않는다. 사용한 코드에서

'md5'의 결과 값이

0x273d27...

0x0273d27a...

두 경우 모두 ` '=' (0x273d27) ` 을 찾았다고 판단하기 때문이다.

