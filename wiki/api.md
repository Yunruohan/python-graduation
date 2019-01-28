# 1. 用户管理类

## 1.1. 用户注册

- path: /user/register
- method: POST
- param:

    ``` javascript
    {
      "username": "sdm@sina.com",
      "password": "123456"
    }
    ```

- return: 

    ``` javascript
    {
    "resperr": "",
    "respcd": "0000",
    "respmsg": "",
    "data": {"userid": 1001,  // 用户ID
            }
    }

    ```
    
## 1.2. 用户登陆

- path: /user/login
- method: POST
- param:

    ``` javascript
    {
      "username": "sdm@sina.com",
      "password": "123456"
    }
    ```

- return: 

    ``` javascript
    {
    "resperr": "",
    "respcd": "0000",
    "respmsg": "",
    "data": {"sessionid": "saaaxaasas",  // 用户session
             "userid": 1001,  // 用户ID
            }
    }

    ```
    
## 1.3. 用户登出

- path: /user/logout
- method: POST
- param:

    ``` javascript
    无
    ```

- return: 

    ``` javascript
    无

    ```