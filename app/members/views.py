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
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # exists를 사용해서 유저가 이미 존재하면 signup으로 다시 redirect
        if User.objects.filter(username=username).exists():
            return redirect('members:signup')
        # 존재하지 않는 경우에만 아래 로직 실행
        user = User.objects.created_user(
            username=username,
            password=password,
        )
        login(request, user)
        return redirect('index')
    return render(request, 'members/signup.html')

