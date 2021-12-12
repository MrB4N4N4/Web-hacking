## old_13

filter : union, #, *, limit, like, 논리/비교연산자, +, -, 

select id from chall13 where no=if( ,1,0)

if(( )in(),1,0)

![chrome_KWeFLMHC9D](https://user-images.githubusercontent.com/79683414/145674374-a0c31535-c703-4994-afbb-19e9d0cff6f6.png)

'='이 필터링 되므로 'in'사용

in : or 여러개

ex) where number in (1,3,5,7,9) / where number in (select ~~)



데이터 베이스명 알아내기

if(ord(substr(database(),1,1))in(99),1,0)