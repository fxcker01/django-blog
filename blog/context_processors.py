from .models import News

def sidebar_articles(request):
    return {
        'top_articles': News.objects.order_by('-views')[:3]
    }