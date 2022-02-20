from django.shortcuts import render, redirect
from .models import UserModel
from django.http import HttpResponse
from django.contrib.auth import get_user_model # 사용자가 있는지 검사하는 함수
from django.contrib import auth # 사용자 auth 기능
from django.contrib.auth.decorators import login_required

# Create your views here.
def sign_up_view(request):
    if request.method == 'GET': # GET 메서드로 요청이 들어 올 경우
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'user/signup.html')
    elif request.method == 'POST': # POST 메서드로 요청이 들어 올 경우
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        bio = request.POST.get('bio', None)

        if password != password2:
            # 패스워드가 같지 않다고 알람
            return render(request, 'user/signup.html', {'error':'패스워드를 확인 해 주세요!'})
        else:
            if username == '' or password =='':
                return render(request, 'user/signup.html', {'error': '사용자 이름과 비밀번호는 필수 값 입니다!'})

            exist_user = get_user_model().objects.filter(username=username)
            if exist_user:
                return render(request, 'user/signup.html', {'error': '사용자가 존재합니다.'}) # 사용자가 존재하기 때문에 사용자를 저장하지 않고 회원가입 페이지를 다시 띄움
            else:
                UserModel.objects.create_user(username=username, password=password, bio=bio)
                return redirect('/sign-in') # 회원가입이 완료되었으므로 로그인 페이지로 이동

def sign_in_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        me = auth.authenticate(request, username=username, password=password) # 사용자 불러오기
        if me is not None: # 저장된 사용자의 패스워드와 입력받은 패스워드 비교
            auth.login(request, me)
            return redirect('/')
        else:
            return render(request, 'user/signin.html', {'error':'유저이름 혹은 패스워드를 확인 해 주세요'}) # 로그인 실패

    elif request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'user/signin.html')

@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')

# user/views.py

@login_required
def user_view(request):
    if request.method == 'GET':
        # 사용자를 불러오기, exclude와 request.user.username 를 사용해서 '로그인 한 사용자'를 제외하기
        user_list = UserModel.objects.all().exclude(username=request.user.username)
        return render(request, 'user/user_list.html', {'user_list': user_list})


@login_required
def user_follow(request, id):
    me = request.user # 로그인한 사용자
    click_user = UserModel.objects.get(id=id) # 로그인한 사용자가 팔로우하거나 팔로우를 취소할 사용자
    if me in click_user.followee.all(): # click_user를 팔로우한 사용자안에 로그인한 사용자 있으면
        click_user.followee.remove(request.user) # 두 번 누른 것이므로 팔로우 취소
    else:
        click_user.followee.add(request.user) # 없다면 팔로우
    return redirect('/user')