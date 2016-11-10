from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, Http404
from django.contrib.auth.decorators import login_required

from .models import Comment
from .forms import CommentForm


@login_required(login_url='login')
def comment_delete(request, id):
    try:
        comment = Comment.objects.get(id=id)
    except:
        raise Http404

    if comment.user != request.user:
        response = HttpResponse("You do not have permission to view this.")
        response.status_code = 403
        return response


    if request.method == "POST":
        parent_obj_url = comment.content_object.get_absolute_url()
        comment.delete()
        messages.success(request, "This has been deleted ")
        return HttpResponseRedirect(parent_obj_url)
    context = {
        "comment": comment,
    }
    return  render(request, "comment_delete.html", context)

# Create your views here.
def comment_thread(request, id):
    try:
        comment = Comment.objects.get(id=id)
    except:
        raise Http404

    if not comment.is_parent:
        comment = comment.parent

    initial_data = {
        "content_type": comment.content_type,
        "object_id": comment.object_id
    }

    comment_form = CommentForm(request.POST or None, initial=initial_data)
    if comment_form.is_valid() and request.user.is_authenticated():
        c_type = comment_form.cleaned_data.get('content_type')
        content_type = ContentType.objects.get(model=c_type)
        obj_id = comment_form.cleaned_data.get('object_id')
        content_data = comment_form.cleaned_data.get('content')
        parent_obj = None
        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None

        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()


        new_comment, created = Comment.objects.get_or_create(
                                                user=request.user,
                                                content_type=content_type,
                                                object_id=obj_id,
                                                content=content_data,
                                                parent=parent_obj,
                                            )
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())
    context = {
        "comment": comment,
        "comment_form": comment_form,
    }
    return render(request, "comment_thread.html", context)