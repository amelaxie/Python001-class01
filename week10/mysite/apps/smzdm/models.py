from django.db.models import Model, IntegerField, CharField, DateTimeField, AutoField, FloatField


# 商品模型
class TGoodsProcessed(Model):
    goods_id = AutoField(primary_key=True)
    brand = CharField(max_length=64, blank=True, null=True)
    category = CharField(max_length=64, blank=True, null=True)
    price = IntegerField(blank=True, null=True)
    name = CharField(max_length=512, blank=True, null=True)
    url = CharField(max_length=160, blank=True, null=True)
    visible_price = CharField(max_length=64, blank=True, null=True)
    worth = IntegerField(blank=True, null=True)
    worthless = IntegerField(blank=True, null=True)
    time = DateTimeField(blank=True, null=True)
    update_time = DateTimeField()
    comment_num = IntegerField(blank=True, null=True)
    positive = IntegerField(blank=True, null=True)
    neutral = IntegerField(blank=True, null=True)
    negative = IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_goods_processed'


# 评论模型
class TCommentProcessed(Model):
    comment_id = AutoField(primary_key=True)
    goods_id = IntegerField(blank=True, null=True)
    text = CharField(max_length=1024, blank=True, null=True)
    time = DateTimeField(blank=True, null=True)
    update_time = DateTimeField()
    positive_prob = FloatField(blank=True, null=True)
    negative_prob = FloatField(blank=True, null=True)
    confidence = FloatField(blank=True, null=True)
    sentiment = IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_comment_processed'
