from django.db import models

class NewsCategoryModel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class NewsModel(models.Model):
    news_category = models.ForeignKey(NewsCategoryModel, on_delete=models.CASCADE, blank=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.FileField(blank=True, null=True, upload_to='img')
    created_date = models.DateTimeField(auto_now_add=True)
    count_of_viewed = models.IntegerField(default=0)


    def __str__(self):
        return f"{self.title} [{self.news_category}]"
