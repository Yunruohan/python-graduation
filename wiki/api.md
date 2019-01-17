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
      "userid": 1001,  // 用户ID
    }
    ```