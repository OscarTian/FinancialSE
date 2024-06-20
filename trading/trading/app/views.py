from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from wallet.models import Wallet

# Create your views here.

def register(request):
    """
    group_name = 'default'
    group = Group.objects.get(name=group_name)
    group.user_set.add(user)
    :param request:
    :return:
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        nickname = request.POST.get('nickname')
        if User.objects.filter(username=username):
            return render(request, 'admin/reister.html', {'error': "当前用户已经注册,请直接登录"})
        if password == password2:
            user = User.objects.create_user(username=username, password=password)
            user.is_staff = True
            if nickname:
                user.last_name = nickname
            user.save()
            Wallet.objects.create(user=user, balance=1000)

            group_name = 'default'
            group = Group.objects.get(name=group_name)
            group.user_set.add(user)
            group.save()

            return redirect('/')
        else:
            return render(request, 'admin/reister.html', {'error': "两次输入密码不一样!"})
    return render(request, 'admin/reister.html')
