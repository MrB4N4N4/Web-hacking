## old_10

![vmware_5CxkrUFk6L](https://user-images.githubusercontent.com/79683414/145141714-b03abf3c-09f8-4566-ba32-7fe468f6e89b.png)

```html
<a id="hackme" style="position:relative;left:0;top:0" onclick="this.style.left=parseInt(this.style.left,10)+1+'px';if(this.style.left=='1600px')this.href='?go='+this.style.left" onmouseover="this.innerHTML='yOu'" onmouseout="this.innerHTML='O'">O</a>
```

<br>

문제 상황을 분석해보면,

1. "O" 를 클릭하면 오른쪽으로 1px 씩 이동한다. ( relative left + 1)
2. "O" 가 1600px 에 위치할 때 `?go=1600px` 값이 세팅된다.

<br>

문제의 의도는 O 를 1600번 클릭하여 Goal 에 도달하도록 만든 것 같다.

그럼 1599 로 설정하고 한번 클릭해주면 해결이 될 듯 하다.

![vmware_zsmwitxYhD](https://user-images.githubusercontent.com/79683414/145144756-a92b2507-3fe6-4660-98ca-1de58b6c64b2.png)

![vmware_jlEyFZGiIm](https://user-images.githubusercontent.com/79683414/145144825-98a90d7f-b367-4b7d-a9a4-26209434fdfd.png)

<br>

위 상태에서 클릭하면 바로 해결된다.

또, Burp suite 를 이용하는 방법이 있다. ` go=1600px ` 상태로 만들면 된다.

![vmware_L8arjFI7gb](https://user-images.githubusercontent.com/79683414/145145222-7b6cae3d-9529-4b70-85e1-11e662f78c32.png)

<br>

하지만 여기서 주의 사항이 있다.

클릭을 1599회 한 상태에서 1600px 를 보내는 상황을 만들어야 하기 때문에

Referer 을 수정해주어야 한다.

![BScEmGkGZk](https://user-images.githubusercontent.com/79683414/145145494-e89346cd-7924-47c4-8029-8ccacaeffe16.png)

<br>

그 후 Forward 하면 바로 해결된다.