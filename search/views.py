import logging
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .forms import SearchForm, PostForm
from django.db.models import Q
from django.shortcuts import render, redirect, reverse
from .models import Post
from .serializers import PostSerializer, UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CustomUser
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import action
import csv
from io import TextIOWrapper, StringIO

logger = logging.getLogger('development')


class IndexView(LoginRequiredMixin, generic.ListView):

    paginate_by = 5
    template_name = 'search/index.html'
    model = Post

    def post(self, request, *args, **kwargs):

        form_value = [
            self.request.POST.get('Score', None),
            self.request.POST.get('Sentence', None),
        ]
        request.session['form_value'] = form_value

        # 検索時にページネーションに関連したエラーを防ぐ
        self.request.GET = self.request.GET.copy()
        self.request.GET.clear()

        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # sessionに値がある場合、その値をセットする。（ページングしてもform値が変わらないように）
        Score = ''
        Sentence = ''
        if 'form_value' in self.request.session:
            form_value = self.request.session['form_value']
            Score = form_value[0]
            Sentence = form_value[1]

        default_data = {'Score': Score,  # タイトル
                        'Sentence': Sentence,  # 内容
                        }

        test_form = SearchForm(initial=default_data)  # 検索フォーム
        context['test_form'] = test_form

        return context

    def get_queryset(self):

        # sessionに値がある場合、その値でクエリ発行する。
        if 'form_value' in self.request.session:
            form_value = self.request.session['form_value']
            Score = form_value[0]
            Sentence = form_value[1]

            # 検索条件
            condition_Score = Q()
            condition_Sentence = Q()

            if len(Score) != 0 and Score[0]:
                condition_Score = Q(Score__icontains=Score)
            if len(Sentence) != 0 and Sentence[0]:
                condition_Sentence = Q(Sentence__contains=Sentence)

            return Post.objects.select_related().filter(condition_Score & condition_Sentence)
        else:
            # 何も返さない
            return Post.objects.none()


class CreateView(generic.CreateView):
    # 登録画面
    model = Post
    form_class = PostForm

    def get_success_url(self):  # 詳細画面にリダイレクトする。
        return reverse('search:detail', kwargs={'pk': self.object.pk})

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super().get_form_kwargs(*args, **kwargs)
        form_kwargs['initial'] = {'author': self.request.user}  # フォームに初期値を設定する。
        return form_kwargs


class DetailView(generic.DetailView):
    # 詳細画面
    model = Post
    template_name = 'search/detail.html'

class TopView(generic.ListView):
    # トップ画面
    model = Post
    template_name = 'search/top.html'


class PostViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        post = self.get_object()
        return Response(post.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'posts': reverse('post-list', request=request, format=format),
    })

def upload(request):
    if 'csv' in request.FILES:
        form_data = TextIOWrapper(request.FILES['csv'].file, encoding='utf-8')
        csv_file = csv.reader(form_data)
        for line in csv_file:
            weapon, created = Post.objects.get_or_create(No=line[0])
            weapon.No = line[0]
            weapon.TOEIC = line[1]
            weapon.Score = line[2]
            weapon.Sex = line[3]
            weapon.Date = line[4]
            weapon.Sentence = line[5]
            #weapon.continuous_power = line[8]
            #weapon.fixed_num = line[9]
            weapon.save()

        return render(request, 'search/upload.html')

    else:
        return render(request, 'search/upload.html')