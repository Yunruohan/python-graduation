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
    
# 2. 图片处理类

## 2.1. 上传图片

- path: /pictures/upload
- method: POST
- param:

    ``` javascript
    {
      "content": 图片文件,
    }
    ```

- return: 

    ``` javascript
    {
    "resperr": "",
    "respcd": "0000",
    "respmsg": "",
    "data": {"url": "http://120.79.17.239/1005/4163ca54-243a-11e9-bc5b-a45e60bb775f.jpg",}
    }

    ```
## 2.2. 展示图片

- path: /pictures/show
- method: GET
- param:

    ``` javascript
    无
    ```

- return: 

    ``` javascript
    {
    "resperr": "",
    "respcd": "0000",
    "respmsg": "",
    "data": [
        {
            "url": "http://120.79.17.239/1005/4163ca54-243a-11e9-bc5b-a45e60bb775f.jpg",
            "create_time": "2019-01-30 10:53:43",
            "name": null
        }
    ]

    ```