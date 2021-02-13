from django.urls import path, reverse_lazy
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.PostListView.as_view(), name='home'),
    path('manage', views.ManagePostListView.as_view(), name='main'),
    path('manage/post/create', views.ManagePostCreateView.as_view(), name='create'),
    path('manage/post/<int:pk>/update', views.ManagePostUpdateView.as_view(), name='update'),
    path('manage/post/<int:pk>/delete', views.ManagePostDeleteView.as_view(), name='delete'),
    path('<int:pk>/<templ>', views.PostDetailView.as_view(), name='article'),
    #path('search/', views.SearchListView.as_view(), name='search_results'),
    path('comment/<int:pk>/<templ>', views.CommentCreateView.as_view() , name="comment")
]