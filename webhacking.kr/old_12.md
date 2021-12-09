## old_12



![vmware_LMlgxFW14h](https://user-images.githubusercontent.com/79683414/145342430-b25db5b5-8cdf-40a2-b308-4bea184b6c02.png)

<br>

javascript challenge 라고 표시되고 별다른 특이사항은 없다.

저 괴랄한 스크립트 코드를 제외하면...

<br>

알아보니 AAEncodeing 이라는 기법으로 인코딩된 스크립트였다. 디코딩 결과는 아래와 같다.

```javascript
var enco='';
var enco2=126;
var enco3=33;
var ck=document.URL.substr(document.URL.indexOf('='));
for(i=1;i<122;i++){
  enco=enco+String.fromCharCode(i,0);
}
function enco_(x){
  return enco.charCodeAt(x);
}
if(ck=="="+String.fromCharCode(enco_(240))+String.fromCharCode(enco_(220))+String.fromCharCode(enco_(232))+String.fromCharCode(enco_(192))+String.fromCharCode(enco_(226))+String.fromCharCode(enco_(200))+String.fromCharCode(enco_(204))+String.fromCharCode(enco_(222-2))+String.fromCharCode(enco_(198))+"~~~~~~"+String.fromCharCode(enco2)+String.fromCharCode(enco3)){
  location.href="./"+ck.replace("=","")+".php";
}
```

<br>

위를 웹 콘솔에 입력하여 분석해보았다.

![vmware_PGi4RBOyJX](https://user-images.githubusercontent.com/79683414/145343495-6b29671d-7a68-42c7-a461-33d77abf14c9.png)

어떤 조건이 만족되면 `youaregod~~~~~~~!.php` 파일을 불러오는 것 같다.

위 파일을 요청하면 해결된다....