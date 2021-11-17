## XSS-Reflected(JSON)

![vmware_u5QMKeHIZd](https://user-images.githubusercontent.com/79683414/137247857-c20a01aa-9465-4902-b485-cb388e81d979.png)

영화의 이름을 검색해서 DB에 존재하는지 여부를 출력해주는 웹이다. 

__JSON__은 xml 과 같이 속성과 값의 쌍으로 이루어져 있으며 해쉬 구조를 갖는다.

xml은 태그로 속성값을 나타내지만 JSON 은 문자열로 나타내며 예제는 아래와 같다.

```json
{
  "squadName": "Super hero squad",
  "homeTown": "Metro City",
  "formed": 2016,
  "secretBase": "Super tower",
  "active": true,
  "members": [
    {
      "name": "Molecule Man",
      "age": 29,
      "secretIdentity": "Dan Jukes",
      "powers": [
        "Radiation resistance",
        "Turning tiny",
        "Radiation blast"
      ]
    },
    {
      "name": "Madame Uppercut",
      "age": 39,
      "secretIdentity": "Jane Wilson",
      "powers": [
        "Million tonne punch",
        "Damage resistance",
        "Superhuman reflexes"
      ]
    },
    {
      "name": "Eternal Flame",
      "age": 1000000,
      "secretIdentity": "Unknown",
      "powers": [
        "Immortality",
        "Heat Immunity",
        "Inferno",
        "Teleportation",
        "Interdimensional travel"
      ]
    }
  ]
}
```



<br><br>

## low

인젝션이 가능한지 테스트하기 위해

"<script>alert(1);</script>"

를 입력해주었더니 무언가 복잡한게 뜬다.

![vmware_QKdsrstm3N](https://user-images.githubusercontent.com/79683414/137248587-9429d23d-427c-4a4e-993c-35e9b429e40b.png)

<br><br>

지금 까지 배운 입력으로는 공격을 성공할 수 없었고 JSON문제는 처음 접하는 것이므로 PHP 소스를 확인해보기로 했다. 아래는 오류로 출력된 문자열의 코드이다.

```php+HTML
<?php
    // Generates the output depending on the movie title received from the client
    if(in_array(strtoupper($title), $movies))
        $string = '{"movies":[{"response":"Yes! We have that movie..."}]}';
    else
        $string = '{"movies":[{"response":"' . $title . '??? Sorry, we don&#039;t have that movie :("}]}';
?>

<script>
    var JSONResponseString = '<?php echo $string ?>';
    // var JSONResponse = eval ("(" + JSONResponseString + ")");
    var JSONResponse = JSON.parse(JSONResponseString);
    document.getElementById("result").innerHTML=JSONResponse.movies[0].response;
</script>
```

<br><br>

`var JSONResponseString = '<?php echo $string ?>'` 를 통해

PHP 에 선언한 "$string"값을 script에 불러오고 

<br>

`var JSONResponse = JSON.parse(JSONResponseString);`

JSON.parse 는 JSON String 을 해당하는 객체로 변환해주는 함수이다.

![chrome_y1Cx213r35](https://user-images.githubusercontent.com/79683414/137253582-1a2b1318-4fa1-41ef-94e3-a641bd3208b6.png)

> __JSON.parse__ https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON/parse

<br><br>

아래는 alert 코드를 삽입했을 때의 상태이다.

<br>

```php
$string = '{"movies":[{"response":"' . "<script>alert(1);</script>". '??? Sorry, we don&#039;t have that movie :("}]}';
```

<br>

php, js 와 같은 서버사이드 스크립트들은 클라이언트에 Response 하기 전에 실행된다는 것을 염두해 두고

에러가 발생한 부분을 다시 살펴보자.

![vmware_AVmAxdI7gs](https://user-images.githubusercontent.com/79683414/138199286-34c85f78-a423-4756-b6d1-69acc7e8e617.png)

![Code_72T9spndEa](https://user-images.githubusercontent.com/79683414/138026378-9eeec5b1-d376-46c3-b1c4-eae7f5fb7a96.png)

<br><br>

삽입한 script 문 뒷 부분부터 출력된 것을 알 수 있다.

출력 결과와 alert문이 실행되지 않은 것으로 볼 때,

alert 문 까지 js 로 취급되고 이후의 것은 html 로 취급된 것 같다.

alert 문이 실행되지 않은 이유는 script 태그가 중복되어서 인듯 하다.

![chrome_CjhRQAiTvT](https://user-images.githubusercontent.com/79683414/138200668-03dd53de-2f5f-454c-9490-8c8d6090e7b4.png)

<br><br>

테스트 결과 Script error 로 alert 문이 실행되지 않고 에러가 발생한 부분이 html 로 취급되어 웹에 출력되고 있다. 테스트 환경에서 'alert(1)' 이 출력된 것은 Bee-Box와 버전 차이로 인한 결과인 것 같다.

<br><br>

그렇다면, 사용자 입력값으로 `</script>`를 추가해주면 스크립트 인젝션 공격을 수행할 수 있을 것이다.

<br><br>

![chrome_A5nVYsK8KR](https://user-images.githubusercontent.com/79683414/138201030-b00581e7-9827-4637-bb7b-303b909c28ad.png)

<br><br>

`</script><script>alert('succeed');</script>`

<br>

![vmware_ostkIYMo1k](https://user-images.githubusercontent.com/79683414/138201237-816f1bba-1ce5-4c32-a8b1-bae766cff347.png)
![vmware_p4YmQ0Whgx](https://user-images.githubusercontent.com/79683414/138201284-4d5c0c89-0089-42dc-9e91-b019aaf3a228.png)
