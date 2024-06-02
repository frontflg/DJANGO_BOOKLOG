from django.db import models
from datetime import date
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Booklog(models.Model):
    STATE = {
        "未": "未読",
        "中": "読書中",
        "了": "読了",
    }
    isbn13 = models.CharField("ISBN13", max_length=13)
    isbn10 = models.CharField("ISBN10", max_length=10, null=True, blank=True)
    bookname = models.CharField("書籍タイトル", max_length=50)
    author = models.CharField("筆者", max_length=25, null=True, blank=True)
    publisher = models.CharField("出版社", max_length=25, null=True, blank=True)
    genre = models.CharField("ジャンル", max_length=25, null=True, blank=True)
    issuedate = models.DateField("発行日", null=True, blank=True)
    getdate = models.DateField("取得日", default=date.today())
    readdate = models.DateField("読了日", null=True, blank=True)
    ownership = models.BooleanField("所有",default=False)
    purchase = models.IntegerField("価格", validators=[MinValueValidator(0), MaxValueValidator(999999)])
    library = models.CharField("取得元", max_length=25, null=True, blank=True)
    overview = models.CharField("概要", max_length=255, null=True, blank=True)
    impressions = models.TextField("感想", null=True, blank=True)
    state = models.CharField("状態", max_length=1, choices=STATE)
    coverimg = models.CharField("表紙", max_length=40, null=True, blank=True)

    def __str__(self):
        return self.isbn13
