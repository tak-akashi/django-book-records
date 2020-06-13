from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
from django.utils import timezone

class Author(models.Model):
    name = models.CharField('著者名', max_length=255)
    description = models.TextField('備考', blank=True)

    def __str__(self):
        return self.name
    

class Genre(models.Model):
    name = models.CharField('ジャンル名', max_length=255)
    description = models.TextField('備考', blank=True)

    def __str__(self):
        return self.name
    
CHOICES = (
    (5, '5: とてもオススメ'),
    (4, '4: オススメ'),
    (3, '3: 普通'),
    (2, '2: どうだろう'),
    (1, '1: オススメせず')
)

class Book(models.Model):
    title = models.CharField('タイトル', max_length=255)
    genre = models.ForeignKey(Genre, verbose_name='ジャンル', related_name='books', blank=True, null=True, on_delete=models.SET_NULL)
    author = models.ForeignKey(Author, verbose_name='著者', related_name='books', blank=True, null=True, on_delete=models.SET_NULL)
    date = models.DateField('読了日', default = timezone.now().today, blank=True)
    created_at = models.DateTimeField('作成日', default=timezone.now)
    recommended = models.IntegerField('おすすめ度', default=3, choices=CHOICES)
    comment = models.TextField('コメント', blank=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        # return reverse('records:detail', kwargs={'pk': self.pk})
        return reverse('index')
    



