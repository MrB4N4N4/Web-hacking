## HTML injection



웹 어플리케이션의 필터링 기능이 미흡할 시 공격자가 악의적인 데이터를 주입하여 발생되는 취약점.

`Reflected` 는 악성 스크립트를 주입한 동시에 결과가 반영된다. **반사된 것 처럼**

`Stored` 는 악성 스크립트를 서버에 **저장** 후 다른 사용자(피해자)가 접근 시 공격이 수행된다.

## Reflected(GET)



### __low__

아무런 필터링이 없어 악성 스크립트 주입이 가능하다.

![vj3QxtkP18](https://user-images.githubusercontent.com/79683414/132443902-48467661-941e-4052-b470-ce644770c19a.png)

![RQKUpqk1Ag](https://user-images.githubusercontent.com/79683414/132444632-31557f14-6496-4fa3-bc26-179e413fac4f.png)

_____

### __medium__

low 와 같은 페이로드를 입력했을 때의 결과이다.

![RVOCWOAjSK](https://user-images.githubusercontent.com/79683414/132601777-571bb19a-8a19-474f-96df-3d58555a76cf.png)

입력한 내용이 그대로 출력된다. 어떤 식의 필터링이 작용한 듯 한데 소스코드를 살펴보자.



___/var/www/bWAPP/htmli_get.php___

```php
<?php
    
include("security.php");
include("security_level_check.php");
include("functions_external.php");
include("selections.php");

function htmli($data)
{
         
    switch($_COOKIE["security_level"])
    {
        
        case "0" : 
            
            $data = no_check($data);            
            break;
        
        case "1" :
            
            $data = xss_check_1($data);
            break;
        
        case "2" :            
                       
            $data = xss_check_3($data);            
            break;
        
        default : 
            
            $data = no_check($data);            
            break;   

    }       

    return $data;

}
```

security level > low : 0, medium : 1, high : 2 임을 알 수 있다. `xss_check_1` 과 `xss_check_3` 이 각각 medium 과 high 에 적용되어 있다.



___funtions_external.php_ - xss_check_1__

```php
function xss_check_1($data)
{
    
    // Converts only "<" and ">" to HTLM entities    
    $input = str_replace("<", "&lt;", $data);
    $input = str_replace(">", "&gt;", $input);
    
    // Failure is an option
    // Bypasses double encoding attacks   
    // <script>alert(0)</script>
    // %3Cscript%3Ealert%280%29%3C%2Fscript%3E
    // %253Cscript%253Ealert%25280%2529%253C%252Fscript%253E
    $input = urldecode($input);
    
    return $input;
    
}
```

str_replace 를 이용해 "<", ">" 를 필터링 한 후 `urldecode()` 를 실행한다.

따라서 "< ", ">" 만 encoding 해주면 될 듯 하다.

![HuPGsFXBCQ](https://user-images.githubusercontent.com/79683414/132602990-1914adb3-b05e-49cb-a6fb-48fc4535924d.png)





__Input : %3Cscript%3Ealert("Hacked!!")%3C/script%3E__



![RsVXRRxjwD](https://user-images.githubusercontent.com/79683414/132603215-be7d17eb-078c-4693-9d84-07ab6dbfdade.png)

![RQKUpqk1Ag](https://user-images.githubusercontent.com/79683414/132444632-31557f14-6496-4fa3-bc26-179e413fac4f.png)





> **URL encode**
>
> URL은 ASCII 문자로만 이루어져 있는데, 안전하지 않은 문자를 포함하는 경우가 있다. 이를 위해 URL encode 를 사용하여 유효하지 않은 문자를 `%[hex][hex]` 형식으로 변환한다.

___



### __high__

___funtions_external.php_ - xss_check_3__

```php
function xss_check_3($data, $encoding = "UTF-8")
{

    // htmlspecialchars - converts special characters to HTML entities    
    // '&' (ampersand) becomes '&amp;' 
    // '"' (double quote) becomes '&quot;' when ENT_NOQUOTES is not set
    // "'" (single quote) becomes '&#039;' (or &apos;) only when ENT_QUOTES is set
    // '<' (less than) becomes '&lt;'
    // '>' (greater than) becomes '&gt;'  
    
    return htmlspecialchars($data, ENT_QUOTES, $encoding);
       
}
```



`htmlspecialchars` 함수는 주석의 문자들을 Html entity 로 변환 시켜 준다. 



> __Html entity__
>
>  https://www.w3schools.com/php/func_string_htmlspecialchars.asp





![RmQqIoq0Aw](https://user-images.githubusercontent.com/79683414/132607960-ece4a1c5-ddf1-4915-bc7f-77e1ba8366dc.png)

![BRPnG6R82o](https://user-images.githubusercontent.com/79683414/132607964-1871d49e-5078-4cbe-b61b-2bd16836f6b0.png)



위 함수를 사용하면 결과적으로,

 `<, >, &, ", ' `의 문자들이 브라우저에 그대로 출력된다.



공격을 하기 위해선 `<script>` 와 같은 태그를 "return" 할 수 있어야 하는데 `htmlspecialchars` 로 인해 스크립트 주입이 불가능 하다.
