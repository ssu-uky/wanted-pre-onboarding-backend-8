### 원티드 프리온보딩 백엔드 인턴십 - 선발 과제

> ## 지원자의 성명
> ### 이수현

---

> ## 애플리케이션 실행 방법
> * python -m venv .venv <br>
> * source .venv/bin/activate <br>
> * pip install -r requirements.txt <br>
> * python manage.py runserver <br>

--- 

> ## 배포 링크
> <a> https://www.ssu-uky.store/ </a>

---

> ## 구현 방법 및 이유
>
> ### users
> * 회원가입(SignUpView)<br>
> <a>https://ssu-uky.store/api/users/signup/</a> <br>
>    <b>{"email":"wanted@wanted.com","password":"wanted123"}</b>
>   - 사용자로부터 이메일과 비밀번호를 입력받습니다.
>   - 이메일은 '@'를 포함해야 하고, 비밀번호는 8자 이상이어야 하는 유효성 검사를 실행합니다.
>   - 유효성 검사가 통과되면, 비밀번호는 암호화하고, 유저를 데이터베이스에 저장합니다.
>   - 회원가입 성공 시 생성 된 사용자의 정보를 반환해줍니다. 이 때, 비밀번호는 암호화해서 반환해줍니다.
>     
> * 로그인(LoginView)<br>
> <a>https://ssu-uky.store/api/users/login/</a> <br>
>    <b>{"email":"wanted@wanted.com","password":"wanted123"}</b>
>   - 사용자로부터 이메일과 비밀번호를 입력받습니다.
>   - 입력 받은 값의 유효성을 검사하고, authenticate 함수를 이용하여 사용자를 인증합니다.
>   - 인증에 성공하면, JWT를 생성하여 access token과 refresh token을 반환합니다.
>   - refresh token은 HttpOnly 쿠키에 저장해서 세션을 유지합니다.
> 
> * 로그아웃(LogoutView)<br>
> <a>https://ssu-uky.store/api/users/logout/</a> <br>
>   - 로그아웃 요청 시, 쿠키에서 refresh token을 blacklist token에 추가하여 token을 만료시킵니다.
>   - 쿠키에서 session id와 만료된 refresh token을 삭제하여 사용자의 값을 지운 후 로그아웃을 완료합니다.
>
> ### boards
> * 게시글 작성(BoardWriteView - POST)<br>
> <a>https://ssu-uky.store/api/boards/write/</a> <br>
>    <b>{"title":"게시글 제목 입니다.","contents":"게시글 내용입니다","job_type":"backend"}</b>
>   - permission_classes로 IsAuthenticated를 지정하여 로그인 된 사용자만 게시글 작성이 가능합니다.
>   - title, contents, job_type, link(선택사항)을 입력 받고, 유효성 검사에 통과 되면 새로운 게시글을 생성한 후 데이터베이스에 저장합니다.
> 
> * 게시글 목록 조회(BoardListView)<br>
> <a>https://ssu-uky.store/api/boards/list/</a> <br>
>   - Pagination을 구현하여 응답시간을 줄이고, 한 페이지에 5개씩 보여줍니다.
>   - 게시글은 작성시간 기준으로 정렬하며 조회합니다.
>
> * 게시글 내용 조회(BoardDetailView - GET)<br>
> <a>https://ssu-uky.store/api/boards/detail/int:pk/</a> <br>
> <a>https://ssu-uky.store/api/boards/detail/1/</a>
>   - 게시글의 ID를 기반으로 get_object 를 사용하여 특정 게시물을 가져옵니다.
>   - 게시글의 자세한 내용은 로그인 한 사용자 = 게시글 작성자 와, 관리자만 조회가 가능합니다.
> 
> * 게시글 내용 수정(BoardDetailView - PUT)<br>
> <a>https://ssu-uky.store/api/boards/detail/int:pk/</a> <br>
> <a>https://ssu-uky.store/api/boards/detail/1/</a>
>   - 게시글의 ID를 기반으로 get_object 를 사용하여 특정 게시물을 가져옵니다.
>   - 게시글 작성자만 내용 수정이 가능합니다. (title, contents, job_type, link)
>   - partial=True 를 사용하여 부분적으로도 수정이 가능합니다. (4개 중 하나도 가능)
>
> * 게시글 삭제(BoardDetailView - DELETE)<br>
> <a>https://ssu-uky.store/api/boards/detail/int:pk/</a> <br>
> <a>https://ssu-uky.store/api/boards/detail/1/</a>
>   - 게시글의 ID를 기반으로 get_object 를 사용하여 특정 게시물을 가져옵니다.
>   - 게시글 작성자만 게시글 삭제가 가능합니다.

---

> ## API 데모 영상 링크
> <a href="https://photos.google.com/share/AF1QipOQisp2leM-nzDLaHci7q9a1AsBT557ddhPpMqFt0Uy3lNzB9wk08NP1Cniz58_8g/photo/AF1QipNWOfedlvSIgkwdjkb1k0qpFpjLPd3JMwelTOth?key=TG95MUF1T1YyLXdKTkQyU2lZX2hhRXUwcjlXYjd3">
> 데모 영상 링크 </a>

---

> ## API 명세서
> <a href="https://ssu-uky.gitbook.io/wanted-pre-onboarding-backend/"> 원티드 프리온보딩 사전 과제 API 명세서 </a>

---

> ## Architecture
> <a href="https://i.ibb.co/Bf3JJbp/wanted-architecture.png"><img src="https://i.ibb.co/Bf3JJbp/wanted-architecture.png" alt="wanted-architecture" border="0"></a>

---

> ## 데이터베이스 테이블 구조
> <a href="https://i.ibb.co/0CTCxVK/Wanted.png"><img src="https://i.ibb.co/T464sq1/Wanted.png" width="1500px" alt="Wanted" border="0"></a>

---

> ## test code 실행 방법
> * python manage.py test
> * python manage.py test users.tests == users test
> * python manage.py test boards.tests == boards test