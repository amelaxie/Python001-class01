from django.db import models


# Create your models here.

# 从数据库反向生成的模型
class TMovieComment(models.Model):
    id = models.BigAutoField(primary_key=True)
    star = models.IntegerField()
    comment = models.CharField(max_length=1024)
    sentiment = models.FloatField(blank=True, null=True)

    class Meta:
        # False不影响数据库表相关信息
        managed = False
        db_table = 't_movie_comment'
