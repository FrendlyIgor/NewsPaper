from django_filters import FilterSet 
from .models import Post
 
 
# создаём фильтр
class PostFilter(FilterSet):
    
    class Meta:
        model = Post
        fields = ('author', 'title', 'dataCategory') # поля, которые мы будем фильтровать (т.е. отбирать по каким-то критериям, имена берутся из моделей)