from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect


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

