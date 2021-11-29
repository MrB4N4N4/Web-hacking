## old_05

![vmware_wCUlAVa0N8](https://user-images.githubusercontent.com/79683414/143832373-ef82444a-2ef3-42c1-8af1-5a7a8b4bbc38.png)

<br>

login/join 버튼이 있다.

login 클릭 시 /mem/login.php 으로 이동하고 join 클릭 시 "access denied" alert 이 뜬다.

느낌상 join 으로 계정을 생성해서 login 하는 문제인듯 하다.

<br>

페이지를 탐색해본 결과 모든 input 에 sql 인젝션을 시도해봤지만 막혀있었고

/mem/ 에서 Directory Browsing 이 존재했다.

/mem/join.php 에 접근하면 처음과 같이 "access denied" alert 이 발생하는데 난독화된 스크립트 코드를 볼 수 있다.

<br><br>

![vmware_rCYze6yEgj](https://user-images.githubusercontent.com/79683414/143833648-aec74044-8117-4acf-8001-d4c4ba04f8e6.png)

<br>

이를 beautiful 하게 바꿔주었다.

Online JavaScript Beautifier - https://beautifier.io/

<br>

```javascript
l = 'a';
ll = 'b';
lll = 'c';
llll = 'd';
lllll = 'e';
llllll = 'f';
lllllll = 'g';
llllllll = 'h';
lllllllll = 'i';
llllllllll = 'j';
lllllllllll = 'k';
llllllllllll = 'l';
lllllllllllll = 'm';
llllllllllllll = 'n';
lllllllllllllll = 'o';
llllllllllllllll = 'p';
lllllllllllllllll = 'q';
llllllllllllllllll = 'r';
lllllllllllllllllll = 's';
llllllllllllllllllll = 't';
lllllllllllllllllllll = 'u';
llllllllllllllllllllll = 'v';
lllllllllllllllllllllll = 'w';
llllllllllllllllllllllll = 'x';
lllllllllllllllllllllllll = 'y';
llllllllllllllllllllllllll = 'z';
I = '1';
II = '2';
III = '3';
IIII = '4';
IIIII = '5';
IIIIII = '6';
IIIIIII = '7';
IIIIIIII = '8';
IIIIIIIII = '9';
IIIIIIIIII = '0';
li = '.';
ii = '<';
iii = '>';
lIllIllIllIllIllIllIllIllIllIl = lllllllllllllll + llllllllllll + llll + llllllllllllllllllllllllll + lllllllllllllll + lllllllllllll + ll + lllllllll + lllll;
lIIIIIIIIIIIIIIIIIIl = llll + lllllllllllllll + lll + lllllllllllllllllllll + lllllllllllll + lllll + llllllllllllll + llllllllllllllllllll + li + lll + lllllllllllllll + lllllllllllllll + lllllllllll + lllllllll + lllll;
if (eval(lIIIIIIIIIIIIIIIIIIl).indexOf(lIllIllIllIllIllIllIllIllIllIl) == -1) {
    alert('bye');
    throw "stop";
}
if (eval(llll + lllllllllllllll + lll + lllllllllllllllllllll + lllllllllllll + lllll + llllllllllllll + llllllllllllllllllll + li + 'U' + 'R' + 'L').indexOf(lllllllllllll + lllllllllllllll + llll + lllll + '=' + I) == -1) {
    alert('access_denied');
    throw "stop";
} else {
    document.write('<font size=2 color=white>Join</font><p>');
    document.write('.<p>.<p>.<p>.<p>.<p>');
    document.write('<form method=post action=' + llllllllll + lllllllllllllll + lllllllll + llllllllllllll + li + llllllllllllllll + llllllll + llllllllllllllll +
        '>');
    document.write('<table border=1><tr><td><font color=gray>id</font></td><td><input type=text name=' + lllllllll + llll + ' maxlength=20></td></tr>');
    document.write('<tr><td><font color=gray>pass</font></td><td><input type=text name=' + llllllllllllllll + lllllllllllllllllllllll + '></td></tr>');
    document.write('<tr align=center><td colspan=2><input type=submit></td></tr></form></table>');
}
```

<br>

브라우저의 콘솔을 이용해 분석해보았다.

<br>

![vmware_IMrCzBMdaO](https://user-images.githubusercontent.com/79683414/143834206-fac7151d-46fd-455c-ae7a-078442234ada.png)

<br>

첫번째 조건문은 쿠키값을 얻어와서 "oldzombie" 문자열을 검색하는 동작을 한다.

처음에는 Burp Suite 로 쿠키값을 추가해 주었는데 작동하지 않아서 브라우저에서 직접 추가했다.

<br>

![vmware_vvbV2lwNUZ](https://user-images.githubusercontent.com/79683414/143834479-5845adaa-100e-478a-a675-a7c1e1d22376.png)

<br>

두번째 조건문은 document.URL 로 url 을 받아온다.

![vmware_AGvGdk9oTS](https://user-images.githubusercontent.com/79683414/143834813-a1fc99e3-9fca-4192-bbf3-cfe8c5a4b877.png)

<br>

url의 끝에 `?mode=1` 을 추가하면 아래와 같이 Join 페이지에 접속이 가능하다.

<br>

![vmware_nAaqeLCjKX](https://user-images.githubusercontent.com/79683414/143835048-fcd6302f-d440-4bf3-a104-fca664836d47.png)

<br>

여기서도 SQL 인젝션을 시도했지만 실패.

admin 계정을 생성하여 로그인을 해줘야 한다.

하지만 admin 계정을 생성하려고 하면 아래와 같이 이미 존재하는 계정이라고 뜬다.

<br>

![vmware_HeLkxbMnCS](https://user-images.githubusercontent.com/79683414/143835205-a846bb17-f3d7-4466-83dd-dc0afd043101.png)

<br>

burpesuite 로 공백문자를 채워보자. 반복적인 시도를 위해 Repeater를 사용했다.

스페이스인 %20을 시도했는데 실패, %00(NULL)을 추가했더니 성공하였다.



<br>

![vmware_3PrVX03xf6](https://user-images.githubusercontent.com/79683414/143835767-96f30dec-5896-442b-b28c-9fc094a155eb.png)

![vmware_JjEHQimj74](https://user-images.githubusercontent.com/79683414/143836188-8f9a2fb8-c05a-471a-b3da-0893795d8f10.png)

<br>

로그인 할 때도 Burp suite 를 이용해 'admin%00'를 입력해 주면 해결.