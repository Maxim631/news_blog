from django.shortcuts import render, redirect, get_object_or_404

from users.models import User
from .models import News, Comments
from django.views import View
from .forms import NewsForm, CommentForm
from .filters import NewsFilter
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import F

class NewsView(View):
    queryset = News.objects.filter(in_processing=False)

    def get(self, request):
        return render(
            request,
            'main.html',
            {
                'all_news': NewsFilter(request.GET, self.queryset).qs
            }
        )


@method_decorator(login_required, name='dispatch')
class CheckNews(View):
    def get(self, request):
        return render(
            request,
            "check_news.html",
            {"news_valid": News.objects.filter(in_processing=True)}
        )





@method_decorator(login_required, name='dispatch')
class ConfirmationNews(View):
    def post(self, request, news_slug: str):
        in_processing = request.POST.get('in_processing')
        news = get_object_or_404(News, slug=news_slug)
        User.objects.filter(id=news.author.id).update(quantity_in_process=F('quantity_in_process') - 1)
        news.in_processing = False
        news.save()
        return redirect("/news/check_news/")

@method_decorator(login_required, name='dispatch')
class DeleteCheckNews(View):
    def post(self, request, news_slug: str):
        news = get_object_or_404(News, slug=news_slug)
        User.objects.filter(id=news.author.id).update(quantity_in_process=F('quantity_in_process') - 1)
        news.delete()
        return redirect("/news/check_news/")


class CategoryNewsView(View):
    def get(self, request, category_id: int):
        queryset = News.objects.filter(category_id=category_id)
        if not request.user.is_staff:
            queryset.filter(in_processing=False)
        return render(
            request,
            'category_news.html',
            {
                "category_news": NewsFilter(request.GET, queryset).qs
            }
        )


@method_decorator(login_required, name='dispatch')
class Profile(View):
    def get(self, request, user_id: int):
        user = User.objects.get(id=user_id)
        queryset = News.objects.filter(author=user.id)
        return render(
            request,
            'profile.html',
            {
                'news_user': NewsFilter(request.GET, queryset).qs,
                'user': user
            }
        )


@method_decorator(login_required, name='dispatch')
class CreateNews(View):
    def get(self, request):
        form = NewsForm
        return render(request, 'create_news.html', {'form': form})

    def post(self, request):
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            create_news = form.save(commit=False)
            create_news.author = request.user
            User.objects.filter(id=create_news.author.id).update(quantity_in_process=F('quantity_in_process') + 1)
            if request.user.quantity_in_process >= 5:
                return render(request, 'quantity_exceeded.html')
            create_news.save()
            return redirect('/')
        return render(request, 'create_news.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class EditNews(View):
    def get(self, request, news_slug: str):
        news = get_object_or_404(News, slug=news_slug)
        form = NewsForm(instance=news)
        return render(request, 'edit_news.html', {'form': form})

    def post(self, request, news_slug: str):
        news = get_object_or_404(News, id=news_slug)
        form = NewsForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            form.save()
            return redirect('/')
        return render(request, 'edit_news.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class DeleteNews(View):
    def post(self, request, news_slug: str):
        News.objects.filter(slug=news_slug).delete()
        return redirect(f"/profile/{request.user.id}")


class NewsDetail(View):
    def get(self, request, news_slug: str):
        form = CommentForm
        news = get_object_or_404(News, slug=news_slug)
        comments_news = Comments.objects.filter(news=news.id, is_active=True)
        return render(request, 'comments.html', {'form': form,
                                                 'news': news,
                                                 'comments_news': comments_news,
                                                 })


@method_decorator(login_required, name='dispatch')
class NewComment(View):
    def post(self, request, news_slug: str):
        comment_form = CommentForm(request.POST)
        news = get_object_or_404(News, slug=news_slug)
        new_comment = None
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.news = news
            new_comment.commentator = request.user
            new_comment.save()
            return redirect(f'/news/{news.slug}')


@method_decorator(login_required, name='dispatch')
class DeleteComment(View):
    def post(self, request, comment_id: int):
        comment = get_object_or_404(Comments, id=comment_id)
        comment.delete()
        return redirect(f'/news/{comment.news.slug}')
