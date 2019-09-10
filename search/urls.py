from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

app_name = 'search'

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register('posts', views.PostViewSet)
router.register('users', views.UserViewSet)

urlpatterns = [
    # 検索画面
    path('search/', views.IndexView.as_view(), name='index'),

    # トップ画面
    path('', views.TopView.as_view(), name='top'),

    # 登録画面
    path('create/', views.CreateView.as_view(), name='create'),

    # 詳細画面
    path('search/<int:pk>/', views.DetailView.as_view(), name='detail'),

    # APIのルート
    path('api/', include(router.urls)),

    path('upload/', views.upload, name='upload'),
]