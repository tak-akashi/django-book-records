import re, io, csv
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import generic
from django.db.models import Q
from records.models import Book, Genre, Author
from records.forms import BookForm, CSVUploadForm


class IndexView(generic.ListView):
    model = Book
    context_object_name = 'book_list'
    template_name='index.html'
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        queryset = Book.objects.all()
        q_words = self.request.GET.get('query')
        
        if q_words:
            # 複数語検索（単語の間を全角・半角スペース（１つ以上）で区切った場合に、分割して単語リストを作成）
            q_words = re.sub('(　| )+', ' ', q_words).split(' ')
            # 単語毎にfor文を回して、querysetを絞り込み
            for q_word in q_words:
                queryset = queryset.filter(
                    Q(title__icontains=q_word) | Q(genre__name__icontains=q_word) | Q(author__name__icontains=q_word) | Q(date__icontains=q_word) 
                )
            
        return queryset.order_by('-date')


class BookCreateView(generic.CreateView):
    model = Book
    form_class = BookForm

class BookDeleteView(generic.DeleteView):
    model = Book
    success_url = reverse_lazy('index')

class BookUpdateView(generic.UpdateView):
    model = Book
    form_class = BookForm

class GenreListView(generic.ListView):
    model = Genre
    context_object_name = 'genre_list'

class GenreCreateView(generic.CreateView):
    model = Genre
    fields = '__all__'
    success_url = reverse_lazy('records:genre_list')

class GenreUpdateView(generic.UpdateView):
    model = Genre
    fields = '__all__'

class GenreDeleteView(generic.DeleteView):
    model = Genre
    success_url = reverse_lazy('records:genre_list')


class AuthorListView(generic.ListView):
    model = Author
    context_object_name = 'author_list'

class AuthorCreateView(generic.CreateView):
    model = Author
    fields = '__all__'
    success_url = reverse_lazy('records:author_list')

class AuthorUpdateView(generic.UpdateView):
    model = Author
    fields = '__all__'
    success_url = reverse_lazy('records:author_list')

class AuthorDeleteView(generic.DeleteView):
    model = Author
    success_url = reverse_lazy('records:author_list')


class AllBookDeleteView(generic.ListView):
    model = Book
    template_name = 'records/all_book_confirm_delete.html'

    def post(self, request):
        self.model.objects.all().delete()
        return redirect('index') 

class BookImport(generic.FormView):
    template_name = 'records/import.html'
    success_url = reverse_lazy('index')
    form_class = CSVUploadForm

    def form_valid(self, form):
        form.save()
        return redirect('index')


def book_export(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="books.csv"'
    # HttpResponseオブジェクトはファイルっぽいオブジェクトなので、csv.writerにそのまま渡せます。
    writer = csv.writer(response)
    writer.writerow(['No', 'タイトル', 'ジャンル', '著者', '読了日', 'おすすめ度', 'コメント'])
    for i, book in enumerate(Book.objects.all()):
        writer.writerow([i+1, book.title, book.genre, book.author, book.date, book.recommended, book.comment])
    return response


