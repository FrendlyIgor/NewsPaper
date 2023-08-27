from django.urls import path
from .views import PostList, PostDetail, AuthorList, AuthorDetail, postSearch

urlpatterns = [
    # path -- означает путь. 
    path('', PostList.as_view()),
    path('<int:pk>', PostDetail.as_view()),
    path('', AuthorList.as_view()),
    path('<int:pk>', AuthorDetail.as_view()),
    path('search/', postSearch.as_view())
]