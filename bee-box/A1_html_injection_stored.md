## Html injection - Stored

악성 스크립트를 서버에 저장하여 의도되지 않은 행위를 하는 것

![vmware_Vknn2XOaon](https://user-images.githubusercontent.com/79683414/132933770-e5828365-ccfe-4c08-b81b-2827d42c3586.png)

## htmli_stored.php

```php
function htmli($data)
{

    include("connect_i.php");

    switch($_COOKIE["security_level"])
    {

        case "0" :

            $data = sqli_check_3($link, $data);
            break;

        case "1" :

            $data = sqli_check_3($link, $data);
            // $data = xss_check_4($data);
            break;

        case "2" :

            $data = sqli_check_3($link, $data);
            // $data = xss_check_3($data);
            break;

        default :

            $data = sqli_check_3($link, $data);
            break;

    }

    return $data;

}
```

