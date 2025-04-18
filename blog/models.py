from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class News(models.Model):
    title = models.CharField('Article title', max_length=100, unique=True)
    text = models.TextField('Main article content')
    date = models.DateTimeField('Publication date', default=timezone.now)
    avtor = models.ForeignKey(User, verbose_name='Author', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='news_images', blank=True, null=True, default='default-img.jpg')

    views = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='liked_news', blank=True)

    # sizes = (
    #     ('S', 'Small'),
    #     ('M', 'Medium'),
    #     ('L', 'Large'),
    #     ('XL', 'X Large'),
    # )

    # shop_sizes = models.CharField(max_length=2, verbose_name='Размеры', choices=sizes, default='S')

    def get_absolute_url(self):
        return reverse('news-detail', kwargs={'pk': self.pk})

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f'{self.title}'

    class Meta: 
        verbose_name = 'News article'
        verbose_name_plural = 'News'


class Comment(models.Model):
    post = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    likes = models.ManyToManyField(User, related_name='liked_comments', blank=True)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f'Comment by {self.name}'
