## md5 compare_view-source

[Stack](#stack-program)

```php+HTML
<?php
    if (isset($_GET['view-source'])) {
         show_source(__FILE__);
         exit();
    }

    if (isset($_GET['v1']) && isset($_GET['v2'])) {
        sleep(3); // anti brute force

        $chk = true;
        $v1 = $_GET['v1'];
        $v2 = $_GET['v2'];

        if (!ctype_alpha($v1)) {$chk = false;}
        if (!is_numeric($v2) ) {$chk = false;}
        if (md5($v1) != md5($v2)) {$chk = false;}

        if ($chk){
            include("../lib.php");
            echo "Congratulations! FLAG is : ".auth_code("md5_compare");
        } else {
            echo "Wrong...";
        }
    }
?>
<br />
<form method="GET">
    VALUE 1 : <input type="text" name="v1" /><br />
    VALUE 2 : <input type="text" name="v2" /><br />
    <input type="submit" value="chk" />
</form>
<br />
<a href="?view-source">view-source</a>
```



<br/>

<br/>

<br/>

<br/>

### Stack Program

