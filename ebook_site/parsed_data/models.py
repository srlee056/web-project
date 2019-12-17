from django.db import models


class EventData(models.Model):
    title = models.CharField(max_length=200)
    link = models.URLField()
    date = models.CharField(max_length=200)
    genre = models.CharField(max_length=200)
    eType = models.IntegerField()
    def __str__(self):
        return self.title
    #date = models.DateTimeField()

class EbookData(models.Model):
    title = models.CharField(max_length=200)
    link = models.URLField()
    events = models.ManyToManyField(
        EventData,
        through='EventLog',
        blank=True,
        through_fields=('ebook', 'event'),
    )
    def __str__(self):
        return self.title

'''ForeignKey - 1:N 관계
    ManyToManyField - N:M 관계
    - 어느쪽에서 선언해도 무방
    - blank=True는 각 모델의 인스턴스가 매번 연결되지 않아도 된다는 뜻. 
        그니까 이북에 이벤트 지정 안해도 됨

'''

class EventLog(models.Model):
    ebook = models.ForeignKey(EbookData, on_delete=models.CASCADE)
    event = models.ForeignKey(EventData, on_delete=models.CASCADE)
    #date_created = models.CharField(max_length = 20, blank=True)