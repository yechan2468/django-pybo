from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone

from ..forms import CommentForm
from ..models import Question, Comment


@login_required(login_url='common:login')
def comment_create_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.question = question
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.save()
            return redirect(f'{resolve_url("pybo:detail", question_id=comment.question.id)}#comment_{comment.id}')
    else:
        form = CommentForm()
    return render(request, 'pybo/comment_form.html', {'form': form})

@login_required(login_url='common:login')
def comment_modify_question(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    
    if request.user != comment.author:
        messages.error(request, '수정 권한이 없습니다')
        return redirect('pybo:detail', question_id=comment.question.id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()
            comment.save()
            return redirect(f'{resolve_url("pybo:detail", question_id=comment.question.id)}#comment_{comment.id}')
    else:
        form = CommentForm(instance=comment)
    context = {'comment': comment, 'form': form}
    return render(request, 'pybo/comment_form.html', context)

@login_required(login_url='common:login')
def comment_delete_question(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    
    if request.user != comment.author:
        messages.error(request, '삭제 권한이 없습니다')
        return redirect('pybo:detail', question_id=comment.question.id)
    else:
        comment.delete()
        return redirect('pybo:detail', question_id=comment.question.id)
