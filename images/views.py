from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from common.decorators import ajax_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import ImageCreateForm
from .models import Image


@login_required
def index(request):
    return render(request,'index.html',{'nbar':'dashboard'})

@login_required
def image_create(request):
    if request.method == 'POST':
        form = ImageCreateForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            form.instance.user=request.user
            form.instance.slug=slugify(form.instance.title)
            # new_item = form.save(commit=False)
            # new_item.user=request.user
            # new_item.save()
            form.save()
            messages.success(request,'Image added successfully!')
            # return redirect(new_item.get_absolute_url())
            return redirect('/')
    else:
        form = ImageCreateForm(request.GET)
    return render(request,'images/image/create.html',{'nbar':'images','form':form})

def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(request,'images/image/detail.html',{'nbar': 'images','image': image})

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
                # create_action(request.user, 'likes', image)
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
