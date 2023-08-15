### 원티드 프리온보딩 백엔드 인턴십 - 선발 과제

---

https://ssu-uky.store/

---

## 1. 지원자의 성명
- 이수현
- id_suhyun@naver.com
---

## 2. 애플리케이션의 실행 방법
root 폴더에 `.env` , `my_settings.py` 파일 추가
```py
.env

SECRET_KEY 추가
```
```py
my_settings.py

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "db_name",
        "USER": "db_user",
        "PASSWORD": "db_passwd",
        "HOST": "server ip",
        "PORT": "3306",
    }
}
```

```py
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py runserver
```

---

## 2-1. 엔드 포인트 호출 방법

BASE_URL = https://ssu-uky.store/

| description | method | url | permission |
| ---- | ---- | ---- | ----|
| 회원가입 | `POST` | /api/users/signup/ | `AllowAny` |
| 로그인 | `POST` | /api/users/login/ | `AllowAny` |
| 로그아웃 | `POST` | /api/users/logout/ | `IsAuthenticated` |
| 게시글 목록 조회 | `GET` | /api/boards/list/ | `AllowAny` |
| 게시글 작성 | `POST` | /api/boards/write/ | `IsAuthenticated` |
| 특정 게시글 조회 | `GET` | /api/boards/detail/<board_id>/ | `IsAuthenticated` , `IsAdminUser` |
| 특정 게시글 수정 | `PUT` | /api/boards/detail/<board_id>/ | `IsAuthenticated` |
| 특정 게시글 삭제 | `DELETE` | /api/boards/detail/<board_id>/ | `IsAuthenticated` |

<board_id> = int:pk

---

## 3. 데이터베이스 테이블 구조
<a href="https://i.ibb.co/F02DFXF/2023-08-15-7-00-01.png"><img src="https://i.ibb.co/F02DFXF/2023-08-15-7-00-01.png" width="1500px" alt="Wanted" border="0"></a>

---

## 4. API 데모 영상 링크
> <a href="https://photos.google.com/share/AF1QipOQisp2leM-nzDLaHci7q9a1AsBT557ddhPpMqFt0Uy3lNzB9wk08NP1Cniz58_8g/photo/AF1QipNWOfedlvSIgkwdjkb1k0qpFpjLPd3JMwelTOth?key=TG95MUF1T1YyLXdKTkQyU2lZX2hhRXUwcjlXYjd3">
> 데모 영상 링크 </a>

---

## 5. 구현 방법 및 이유에 대한 간략한 설명

### users
<a href="https://ssu-uky.store/api/users/signup/"> 회원가입(SignUpView)</a> <br>
{"email":"wanted@wanted.com","password":"wanted123"}
- 사용자로부터 이메일과 비밀번호를 입력받습니다.
- 이메일은 '@'를 포함해야 하고, 비밀번호는 8자 이상이어야 하는 유효성 검사를 실행합니다.
- 유효성 검사가 통과되면, 비밀번호는 암호화하고, 유저를 데이터베이스에 저장합니다.
- 회원가입 성공 시 생성 된 사용자의 정보를 반환해줍니다. 이 때, 비밀번호는 암호화해서 반환해줍니다. <br>
 

<a href="https://ssu-uky.store/api/users/login/">로그인(LoginView) </a> <br>
{"email":"wanted@wanted.com","password":"wanted123"}
- 사용자로부터 이메일과 비밀번호를 입력받습니다.
- 입력 받은 값의 유효성을 검사하고, authenticate 함수를 이용하여 사용자를 인증합니다.
- 인증에 성공하면, JWT를 생성하여 access token과 refresh token을 반환합니다.
- refresh token은 HttpOnly 쿠키에 저장해서 세션을 유지합니다. <br>


<a href="https://ssu-uky.store/api/users/logout/">로그아웃(LogoutView)</a> <br>
- 로그아웃 요청 시, 쿠키에서 refresh token을 blacklist token에 추가하여 token을 만료시킵니다.
- 쿠키에서 session id와 만료된 refresh token을 삭제하여 사용자의 값을 지운 후 로그아웃을 완료합니다.
<br>

### boards


<a href="https://ssu-uky.store/api/boards/list/">게시글 목록 조회(BoardListView)</a> <br>
- Pagination을 구현하여 응답시간을 줄이고, 한 페이지에 5개씩 보여줍니다.
- 게시글은 작성시간 기준으로 정렬하여 조회합니다. <br>

<a href="https://ssu-uky.store/api/boards/write/">게시글 작성(BoardWriteView - POST)</a> <br>
{"title":"게시글 제목 입니다.","contents":"게시글 내용입니다","job_type":"backend"}
- permission_classes로 IsAuthenticated를 지정하여 로그인 된 사용자만 게시글 작성이 가능합니다.
- title, contents, job_type, link(선택사항)을 입력 받고, 유효성 검사에 통과 되면 새로운 게시글을 생성한 후 데이터베이스에 저장합니다. <br>


<a href="https://ssu-uky.store/api/boards/detail/1/">게시글 내용 조회(BoardDetailView - GET)</a>
<a href="https://ssu-uky.store/api/boards/detail/<int:pk>/"> </a> <br>
- 게시글의 ID를 기반으로 get_object 를 사용하여 특정 게시물을 가져옵니다.
- 게시글의 자세한 내용은 로그인 한 사용자 = 게시글 작성자 와, 관리자만 조회가 가능합니다. <br>
 

<a href="https://ssu-uky.store/api/boards/detail/1/">게시글 내용 수정(BoardDetailView - PUT)</a>
<a href="https://ssu-uky.store/api/boards/detail/<int:pk>/"> </a> <br>
{"contents":"수정 한 게시글 내용입니다","link":"https://velog.io/@ssu-uky"}
- 게시글의 ID를 기반으로 get_object 를 사용하여 특정 게시물을 가져옵니다.
- 게시글 작성자만 내용 수정이 가능합니다. (title, contents, job_type, link)
- link의 형식이 올바르지 않으면 수정이 되지 않습니다.
- partial=True 를 사용하여 부분적으로도 수정이 가능합니다. (4개 중 하나도 가능) <br>

<a href="https://ssu-uky.store/api/boards/detail/1/">게시글 삭제(BoardDetailView - DELETE)</a>
<a href="https://ssu-uky.store/api/boards/detail/<int:pk>/"> </a> <br>
- 게시글의 ID를 기반으로 get_object 를 사용하여 특정 게시물을 가져옵니다.
- 게시글 작성자만 게시글 삭제가 가능합니다.


---

## 6. API 명세서
<a href="https://ssu-uky.gitbook.io/wanted-pre-onboarding-backend/"> 원티드 프리온보딩 사전 과제 API 명세서 </a>
<br>

### users
  
회원가입  `POST` <br>
https://ssu-uky.store/api/users/signup/

<details>
<summary> Request parameters </summary>

| Parameter | Description |
| --- | --- |
| email | email 형식에 맞아야한다. |
| password | 최소 8자 이상이어야한다. |

```py
{"email":"email@email.com","password":"email~!~!"}
```
</details>

<details>
<summary>Response</summary>
  
#### HTTP 201 Created
  
```py
  {
    "message": "회원가입이 완료되었습니다. 로그인을 해주세요.",
    "email": "email@email.com",
    "password": "pbkdf2_sha256$600000$Op0Rj4nXrKGw3hMCLcN24U$I3V99IwPQ9B4BHPzZsb4GsER22LebfQ43Wi+HhoCWXo="
}
```

#### 400 Bad Request
- 이메일이나 비밀번호가 유효성 검사에서 통과되지 않을 경우 (형식에 맞지 않을 경우)

```py

{
    "email": [
        "유효한 이메일 주소를 입력하십시오."
    ],
    "password": [
        "비밀번호는 8자리 이상이어야 합니다."
    ]
}

```

- 중복된 이메일 일 경우

```py
{
    "email": [
        "이미 존재하는 이메일입니다."
    ]
}
```
</details>


로그인  `POST` <br>
https://ssu-uky.store/api/users/login/

<details>
<summary> Request parameters </summary>

| Parameter | Description |
| --- | --- |
| email | 가입 된 이메일이어야한다. |
| password | 가입 했을 시 비밀번호와 같아야한다. |

```py
{"email":"email@email.com","password":"email~!~!"}
```
</details>


<details>
<summary>Response</summary>
  
#### HTTP 200 OK
  
```py
  {
    "message": "로그인 성공!",
    "email": "email@email.com",
    "token": {
        "access_token": "access_token",
        "refresh_token": "refresh_token"
    }
}
```

#### 400 Bad Request
- 이메일이나 비밀번호가 db에 저장 된 값과 다를 경우 (가입 된 값과 다를 경우)

```py

{
    "message": "이메일과 비밀번호를 확인해주세요."
}

```
</details>



로그아웃  `POST`  <br>
https://ssu-uky.store/api/users/logout/

<details>
<summary> Request parameters </summary>

#### HTTP 200 OK

```py
{
    "message": "로그아웃 성공"
}
```
</details>

<br>

### boards

글 목록 조회 `GET` <br>
https://ssu-uky.store/api/boards/list/

<details>
<summary> Response </summary>

#### HTTP 200 OK

```py

> count : 총 글의 갯수
> next : pagination 의 다음 페이지 
> previous : pagination 의 이전 페이지 
> results : 글의 목록 

{
    "count": 7,
    "next": "https://ssu-uky.store/api/boards/list/?page=2", 
    "previous": null,
    "results": [
        {
            "id": 1,
            "writer": "popo@popo.com",
            "title": "dgasd",
            "job_type": "PM"
        },
        {
            "id": 2,
            "writer": "happy@happy.com",
            "title": "happy의 이력서",
            "job_type": "FRONTEND"
        },
        {
            "id": 3,
            "writer": "hoho@hoho.com",
            "title": "suhyun의 원티드 과제",
            "job_type": "BACKEND"
        },
        {
            "id": 4,
            "writer": "roro@roro.com",
            "title": "suhyun의 원티드 과제",
            "job_type": "BACKEND"
        },
        {
            "id": 5,
            "writer": "coco@coco.com",
            "title": "suhyun의 원티드 과제",
            "job_type": "BACKEND"
        }
    ]
}
```

</details>



글 작성  `POST` <br>
https://ssu-uky.store/api/boards/write/

<details>
<summary> Request parameters </summary>

| Parameter | Description | Comments |
| --- | --- | --- |
| title | 이력서 제목 | - |
| contents | 이력서 내용 | - |
| job_type | 직업 종류 | frontend, backend, pm, marketing, design |
| link | 추가적으로 넣을 링크 (optional) | 링크 형식에 맞아야 합니다. |

```py
{"title":"이력서 제목 입니다.","contents":"이력서 내용 입니다.","job_type":"backend"}
```
</details>


<details>
<summary>Response</summary>
  
#### HTTP 201 Created
  
```py
{
    "id": 8,
    "writer": "email@email.com",
    "title": "이력서 제목 입니다.",
    "contents": "이력서 내용 입니다.",
    "job_type": "BACKEND",
    "link": null,
    "created_at": "2023-08-15T08:28:54.269680",
    "updated_at": "2023-08-15T08:28:54.269732"
}
```

#### 400 Bad Request
- title, contents, job_type을 작성하지 않았을 경우

```py

{
    "title": [
        "이 필드는 null일 수 없습니다."
    ],
    "contents": [
        "이 필드는 null일 수 없습니다."
    ],
    "job_type": [
        "이 필드는 null일 수 없습니다."
    ]
}
```

- job_type이 choices 내의 값이 아닌 경우

```py
{
    "job_type": [
        "\"MARKET\"이 유효하지 않은 선택(choice)입니다."
    ]
}
```
</details>


특정 글 조회  `GET` <br>
https://ssu-uky.store/api/boards/detail/1/ <br>
https://ssu-uky.store/api/boards/detail/board_id/

<details>

<summary>Response</summary>
  
#### HTTP 200 OK
  
```py
{
    "id": 8,
    "writer": "email@email.com",
    "title": "이력서 제목 입니다.",
    "contents": "이력서 내용 입니다.",
    "job_type": "BACKEND",
    "link": null,
    "created_at": "2023-08-15T08:28:54.269680",
    "updated_at": "2023-08-15T08:28:54.269732"
}
```

#### HTTP 401 Unauthorized
- 로그인을 하지 않았을 경우

```py
{
    "message": "로그인이 필요합니다."
}
```

#### HTTP 403 Forbidden
- 본인이 작성한 글이 아닐 경우

```py
{
    "message": "권한이 없습니다."
}
```
</details>


특정 글 수정  `PUT` <br>
https://ssu-uky.store/api/boards/detail/1/ <br>
https://ssu-uky.store/api/boards/detail/board_id/

<details>
<summary> Request parameters </summary>

작성자 본인만 부분적으로 수정이 가능합니다.

| Parameter | Description | Comments |
| --- | --- | --- |
| title | 이력서 제목 | - |
| contents | 이력서 내용 | - |
| job_type | 직업 종류 | frontend, backend, pm, marketing, design |
| link | 추가적으로 넣을 링크 (optional) | 링크 형식에 맞아야 합니다. |

```py
{"contents":"수정된 이력서 내용 입니다.","link":"https://velog.io/@ssu-uky"}
```
</details>

<details>

<summary>Response</summary>
  
#### HTTP 200 OK
  
```py
{
    "id": 8,
    "writer": "email@email.com",
    "title": "이력서 제목 입니다.",
    "contents": "수정된 이력서 내용 입니다.",
    "job_type": "BACKEND",
    "link": "https://velog.io/@ssu-uky",
    "created_at": "2023-08-15T08:28:54.269680",
    "updated_at": "2023-08-15T08:47:18.421726"
}
```

#### HTTP 400 Bad Request
- 유효한 링크가 아닐 경우

```py
{
    "link": [
        "유효한 URL을 입력하십시오."
    ]
}
```

#### HTTP 401 Unauthorized
- 로그인을 하지 않았을 경우

```py
{
    "message": "로그인이 필요합니다."
}
```

#### HTTP 403 Forbidden
- 본인이 작성한 글이 아닐 경우

```py
{
    "message": "권한이 없습니다."
}
```

</details>


특정 글 삭제  `DELETE` <br>
https://ssu-uky.store/api/boards/detail/1/ <br>
https://ssu-uky.store/api/boards/detail/board_id/

<details>
<summary> Request parameters </summary>

작성자 본인만 작성한 글을 삭제할 수 있습니다

</details>

<details>

<summary>Response</summary>
  
#### HTTP 204 No Content


</details>

---

## 7. Architecture

<a href="https://i.ibb.co/Bf3JJbp/wanted-architecture.png"><img src="https://i.ibb.co/Bf3JJbp/wanted-architecture.png" alt="wanted-architecture" border="0"></a>

---

## 8. testcode 실행 방법
```py
python manage.py test

<users>
python manage.py test users.tests

<boards>
python manage.py test boards.tests
```
