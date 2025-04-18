from django.shortcuts import render, redirect
from common.forms import UserForm
from django.contrib.auth import authenticate, login, logout


def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            row_password = form.cleaned_data.get("password1")
            # 사용자 인증 담당 : 아이디와 비밀번호가 DB랑 같은지 비교
            user = authenticate(username=username , password=row_password)
            # 로그인 담당 : 사용자에게 입력받은 request와 인증기록인 user를 통해 로그인 허용 또는 거부
            login(request, user)
            return redirect("home")
    else: # Get 요청일 떄
        form = UserForm()
    return render(request, "common/signup.html", {"form": form})

def logout_view(request):
    logout(request)