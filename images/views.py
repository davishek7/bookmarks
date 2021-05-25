from django.shortcuts import render, redirect,get_object_or_404
from django.utils.text import slugify
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from common.decorators import ajax_required
from actions.utils import create_action
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import ImageCreateForm
from .models import Image
from actions.models import Action
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin


@login_required
def index(request):
        # Display all actions by default
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id',flat=True)
    if following_ids:
        # If user is following others, retrieve only their actions
        actions = actions.filter(user_id__in=following_ids)
    actions = actions.select_related('user', 'user__profile').prefetch_related('target')[:10]
    
    return render(request,'index.html',{'nbar':'dashboard','actions':actions})


@login_required
def image_create(request):
    if request.method == 'POST':
        form = ImageCreateForm(request.POST)
        if form.is_valid():
            form.instance.user=request.user
            form.instance.slug=slugify(form.instance.title)
            form.save()
            create_action(request.user, 'bookmarked image',form.instance)
            messages.success(request,'Image added successfully!')
            return redirect('images:index')
    else:
        form = ImageCreateForm(request.GET)
    return render(request,'images/image/create.html',{'nbar':'images','form':form})

@login_required
def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    # hitcount logic
    context={}

    hit_count = get_hitcount_model().objects.get_for_object(image)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits

    context={'nbar': 'images','image': image,}
    return render(request,'images/image/detail.html',context)


@ajax_required
@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
                create_action(request.user, 'likes', image)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status':'ok'})
        except:
            pass
    return JsonResponse({'status':'ko'})


@login_required
def image_list(request):
    images = Image.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            # If the request is AJAX and the page is out of range
            # return an empty page
            return HttpResponse('')
        # If page is out of range deliver last page of results
        images = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request,
                      'images/image/list_ajax.html',
                      {'nbar': 'images', 'images': images})
    return render(request,'images/image/list.html',{'nbar': 'images', 'images': images})


@login_required
def image_ranking(request):
    # get image ranking dictionary
    image_ranking = r.zrange('image_ranking', 0, -1, desc=True)[:10]
    image_ranking_ids = [int(id) for id in image_ranking]
    # get most viewed images
    most_viewed = list(Image.objects.filter(
                           id__in=image_ranking_ids))
    most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))
    return render(request,
                  'images/image/ranking.html',{'nbar': 'images','most_viewed': most_viewed})
