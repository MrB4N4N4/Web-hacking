## old_04

![vmware_sIGCLx52yY](https://user-images.githubusercontent.com/79683414/143746415-d62dccc6-6ee8-4e0d-acc1-669be082cd86.png)
![vmware_kEJHeCx46m](https://user-images.githubusercontent.com/79683414/143746440-768b215b-7fac-44a8-a6c3-de6fea4dd6e4.png)

<br>

어떤 해시값이 주어지고 Password(key) 를 제출하는 형태의 문제이다.

코드를 살펴보니 `chall4` 세션 변수와 제출한 Password 의 값이 일치해야 된다.

`chall4` 세션 변수는 "sha1" 해쉬 함수로 암호화 된다.

해쉬함수는 단방향적 특징 때문에 복호화가 불가능하다.

파이썬으로 코드를 이용하여 해.결

<br>

```python
from hashlib import sha1

result = {}

for i in range(10000000, 100000000):
    key = str(i) + "salt_for_you"
    rand = key
    print("[+]Hashing key: ", key)
    for _ in range(500):
        rand = str(sha1(rand.encode("utf-8")).hexdigest())
    result[rand] = key
    print(result)
```

 ![pycharm64_Vy33RdkWWe](https://user-images.githubusercontent.com/79683414/143816035-e51ae631-ac85-4a92-b885-b4f422f66b53.png)

너무 오래 걸린다... 멀티프로세스를 이용하자.

> 파이썬에서 멀티쓰레드
>
> 파이썬은 자원을 보호하기 위해 GIL 정책을 사용한다. 락이 걸려 한번의 하나의 쓰레드만 자원을 접근할 수 있다. 따라서 다중 쓰레드로 작업을 처리해도 자원에 접근할 수 있는 쓰레드는 1개로 제한됨. CPU 작업과 IO 작업을 병행하는 경우는 효율적임 >> 멀티 프로세스 이용

<br><br>

```python
from hashlib import sha1
from multiprocessing import Pool

result = {}
chall4 = "cd7c12473dc6449f75ac0d8746bb50e886723eab"


def sha1_hash(list):
    start = list[0]
    end = list[1]
    for i in range(start, end):
        key = str(i) + "salt_for_you"
        rand = key
        print("trying: ", key)
        for _ in range(500):
            rand = str(sha1(rand.encode("utf-8")).hexdigest())
        if chall4 == rand:
            print("answer : ", key)
            exit()


if __name__ == "__main__":
    START = 10000000
    END = 100000000
    q = (END - START) // 8

    p_list = [
        [START, START+q], [START+q, START+2*q], [START+2*q,START+3*q],[START+3*q, START+4*q],
        [START+4*q, START+5*q], [START+5*q, START+6*q], [START+6*q, START+7*q], [START+7*q, END]
    ]
    pool = Pool(processes=6)
    pool.map(sha1_hash, p_list)
    pool.close()
    pool.join()

```

cpu 사용률이 90% 를 넘은적은 처음..

3시간 이상 걸린다고 하여 스킵...

