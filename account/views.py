from django.http import JsonResponse
from django.shortcuts import render, redirect,get_object_or_404
# from django.urls import reverse_lazy
# from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm, ProfileUpdateForm, UserUpdateForm
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from common.decorators import ajax_required
from .models import Contact


def register_user(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, f'Account was created for {username}!')
            return redirect('account:login')

    context = {"form": form}
    return render(request, 'account/register.html', context)


@login_required
def update_user(request):

	if request.method == 'POST':
		u_form=UserUpdateForm(request.POST,instance=request.user)
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request,'Your account has been updated')
			return redirect('account:update_user')
	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)

	context={'u_form':u_form,'p_form':p_form,'nbar':'profile'}

	return render(request,'account/update_user.html',context)

@login_required
def user_list(request):
    users = User.objects.filter(is_active=True).exclude(username=request.user.username)
    return render(request,
                  'account/user/list.html',
                  {'nbar': 'people',
                   'users': users})


@login_required
def user_detail(request, username):
    user = get_object_or_404(User,
                             username=username,
                             is_active=True)
    return render(request,
                  'account/user/detail.html',
                  {'nbar': 'people',
                   'user': user})


@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user,
                                              user_to=user)
                # create_action(request.user, 'is following', user)
            else:
                Contact.objects.filter(user_from=request.user,
                                       user_to=user).delete()
            return JsonResponse({'status':'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status':'ko'})
    return JsonResponse({'status':'ko'})
