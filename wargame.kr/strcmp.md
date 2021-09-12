## strcmp_view-source

```php+HTML
<?php
    require("../lib.php"); // for auth_code function

    $password = sha1(md5(rand().file_get_contents("/var/lib/dummy_file")).rand());

    if (isset($_GET['view-source'])) {
        show_source(__FILE__);
        exit();
    }else if(isset($_POST['password'])){
        sleep(1); // do not brute force!
        if (strcmp($_POST['password'], $password) == 0) {
            echo "Congratulations! Flag is <b>" . auth_code("strcmp") ."</b>";
            exit();
        } else {
            echo "Wrong password..";
        }
    }

?>
<br />
<br />
<form method="POST">
    password : <input type="text" name="password" /> <input type="submit" value="chk">
</form>
<br />
<a href="?view-source">view-source</a>
```

password 는 rand(),  dummy_file, 해쉬함수를 이용하여 구성되어있다. rand()가 10자리 난수를 반환하고 

sleep() 때문에 브루트 포싱도 힘들 것 같다.

## strcmp

strcmp(string `$string1`, string `$string2`): int

str1이 str2보다 작으면 음수,  크면 양수, 같으면 0 을 반환하는 함수이다. 

php 4, 5, 7, 8 버전에서 문자열과 배열을 비교하면 NULL을 반환한다.

> __Reference__ - https://www.php.net/manual/en/function.strcmp.php



## exploit

문제를 풀기 위해 아래의 3가지 아이디어를 이용했다.

- php 의 특정 버전에서 `NULL` 을 return 하는 경우가 있다.
- "NULL== 0" 의 결과는 참이다.
- `<input>`from의 `name=password` 를 `name=password[]` 로 바꾸면 배열로 넘어간다.





1번째 항목은 위의 Reference 를 참고하자.





2번째 항목을 확인해보자.

![DODCcC6g3z](https://user-images.githubusercontent.com/79683414/132970864-569c8a6d-8da0-4a2c-b81e-4076f0814d67.png)





"NULL==0" 의 결과는 `True` 지만, 아래의 상황도 유의하자.

![oexG6r4130](https://user-images.githubusercontent.com/79683414/132970925-a8fb739b-8e96-44d4-82b2-52a807e3c402.png)







3번째 항목 name 속성의 `password`  를 `password[]` 로 변경했다.

![chrome_5Nb33FaF0R](https://user-images.githubusercontent.com/79683414/132970974-4e98a0ed-7066-4500-a773-f0a91070125b.png)





`POST` 방식이므로 htmlrequest 패킷의 body에 "password=input" 형태로 들어갈 것이다.

![BurpSuiteCommunity_HFyPEvhENW](https://user-images.githubusercontent.com/79683414/132971033-25b98474-4cb9-4bf1-9194-8b2fe9946baa.png)

사실 이 부분이 아직은 이해가 안된다. 소스코드에서 $_POST['password'] 로 값을 받고 있으므로 `password[]` 가 타입이 맞지 않아 전달이 안될 것이라 생각했다. php 의 어떤 동작방식에 이름만 같으면 객체 타입에 상관 없이 전달이 되는 듯 하다. 

