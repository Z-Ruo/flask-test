*** Settings ***
Documentation    API测试自动化 - 用户管理系统测试
Library    RequestsLibrary
Library    Collections
Suite Setup    创建会话

*** Variables ***
${BASE_URL}    http://127.0.0.1:5000
${CONTENT_TYPE}    application/json

*** Test Cases ***
测试添加用户
    [Documentation]    测试POST /user接口
    &{headers}=    Create Dictionary    Content-Type=${CONTENT_TYPE}
    &{data}=    Create Dictionary    name=张三    age=20
    ${response}=    POST On Session    flask    /user    json=${data}    headers=${headers}
    Status Should Be    201    ${response}
    ${json}=    Set Variable    ${response.json()}
    Should Be True    ${json['id']}
    Set Suite Variable    ${USER_ID}    ${json['id']}
    Should Be Equal As Strings    ${json['name']}    张三
    Should Be Equal As Strings    ${json['age']}    20

测试获取单个用户
    [Documentation]    测试GET /user/{id}接口
    ${response}=    GET On Session    flask    /user/${USER_ID}
    Status Should Be    200    ${response}
    ${json}=    Set Variable    ${response.json()}
    Should Be Equal    ${json['name']}    张三
    Should Be Equal    ${json['age']}    ${20}

测试获取用户列表
    [Documentation]    测试GET /users接口
    ${response}=    GET On Session    flask    /users
    Status Should Be    200    ${response}
    ${json}=    Set Variable    ${response.json()}
    Log    用户列表响应: ${json}
    Should Be True    ${USER_ID} in [user['id'] for user in ${json}]

测试更新用户
    [Documentation]    测试PUT /user/{id}接口
    &{headers}=    Create Dictionary    Content-Type=${CONTENT_TYPE}
    &{data}=    Create Dictionary    name=李四    age=22
    ${response}=    PUT On Session    flask    /user/${USER_ID}    json=${data}    headers=${headers}
    Status Should Be    200    ${response}
    ${json}=    Set Variable    ${response.json()}
    Should Be Equal    ${json['name']}    李四
    Should Be Equal    ${json['age']}    ${22}

测试删除用户
    [Documentation]    测试DELETE /user/{id}接口
    ${response}=    DELETE On Session    flask    /user/${USER_ID}
    Status Should Be    200    ${response}
    ${json}=    Set Variable    ${response.json()}
    Should Be Equal    ${json['message']}    User deleted
    Should Be Equal    ${json['id']}    ${USER_ID}

*** Keywords ***
创建会话
    Create Session    flask    ${BASE_URL}    verify=True
