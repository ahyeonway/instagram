from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect

# User클래스 자체를 가져올때는 get_user_model()
# ForeignKey에 User모델을 지정할때는 settings.AUTH_USER_MODEL
User = get_user_model()


def login_view(request):
    # print(request.POST)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # 받은 username과 password에 해당하는 User가 있는지 인증
        user = authenticate(request, username=username, password=password)

        # 인증에 성공하면 post:post-list로 이동
        if user is not None:
            # 세션값을 만들어 DB에 저장하고, HTTP response의 Cookie에 해당값을 담아보내도록 하는
            # login()함수를 실행한
            login(request, user)
            return redirect('posts:post-list')
        # 인증에 실패한 경우 다시 members:login으로 이동
        else:
            # 다시 로그인 페이지로 redirect
            return redirect('members:login')
    # GET 요청일 경우
    else:
        # form이 있는 template을 보여준다
        return render(request, 'members/login.html')


def logout_view(request):
    logout(request)
    return redirect('index')


def signup(request):
    context = {
        'errors': [],
    }
    if request.method == 'POST':
        # 입력되지 않은 필드에 대한 오류를 추가
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        email = request.POST['email']

        # print(locals())
        # 반드시 내용이 채워져야 하는 form의 필드 (위 변수명)

        # required_fields = ['username', 'email', 'password', 'password2']
        # for field_name in required_fields:
        #     print('field_name:', field_name)
        #     print('locals().[field_name]:', locals()[field_name])
        #     if not locals()[field_name]:
        #         context['errors'].append('{}를(을) 채워주세요'.format(field_name))

        required_fields = {
            'username': {
                'verbose_name': '아이디',
            },
            'email': {
                'verbose_name': '이메일',
            },
            'password': {
                'verbose_name': '비밀번호',
            },
            'password2': {
                'verbose_name': '비밀번호 확인',
            }
        }
        for field_name in required_fields.keys():
            if not locals()[field_name]:
                context['errors'].append('{}를(을) 채워주세요'.format(field_name))


        # 입력데이터 채워넣기
        context['username'] = username
        context['email'] = email

        # form에서 전송한 데이터들이 올바른지 검사
        if User.objects.filter(username=username).exists():
            context['errors'].append('유저가 이미 존재함')
        # password, password2를 검사
        if password != password2:
            context['errors'].append('비밀번호가 일치하지 않음')
        # errors가 존재하면 render


        if not context['errors']:
            user = User.objects.created_user(
                username=username,
                password=password,
            )
            login(request, user)
            return redirect('index')

    return render(request, 'members/signup.html', context)


