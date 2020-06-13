import io, csv
from django import forms
from django.utils import timezone
from .models import Book, Genre, Author


class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        exclude = ['created_at']
        widgets = {
            'date': forms.SelectDateWidget(years=[x for x in range(timezone.now().year - 10, timezone.now().year + 1)]),
        }


class CSVUploadForm(forms.Form):
    file = forms.FileField(label='',
                            help_text='＊拡張子csvのファイルをアップロードして下さい。')
    
    def clean_file(self):
        file = self.cleaned_data['file']

        # ファイル名が.csvかどうかの確認
        if not file.name.endswith('.csv'):
            raise forms.ValidationError('拡張子がcsvのファイルをアップロードしてください')

        # csv.readerに渡すため、TextIOWrapperでテキストモードなファイルに変換
        csv_file = io.TextIOWrapper(file, encoding='utf-8')
        reader = csv.reader(csv_file)

        # 各行から作った保存前のモデルインスタンスを保管するリスト
        self._instances = []
        try:
            for _i, row in enumerate(reader):
                if _i != 0:
                    book, created = Book.objects.get_or_create(title=row[1])
                    if created:
                        book.genre = Genre.objects.get_or_create(name=row[2])[0]
                        book.author = Author.objects.get_or_create(name=row[3])[0]
                        book.date = row[4]
                        book.recommended = row[5]
                        book.comment = row[6]
                    self._instances.append(book)
        except UnicodeDecodeError:
                raise forms.ValidationError('ファイルのエンコーディングや、正しいCSVファイルか確認ください。')

        return file

    def save(self):
        for book in self._instances:
            book.save()
