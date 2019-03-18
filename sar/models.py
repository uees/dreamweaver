from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django_extensions.db.fields.json import JSONField

User = get_user_model()


class Table(models.Model):
    name = models.CharField('表名', max_length=64)
    price = models.DecimalField('价格', max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '表格'
        verbose_name_plural = verbose_name


class TableHeader(models.Model):
    table = models.ForeignKey(Table, verbose_name="表格", on_delete=models.CASCADE)
    name = models.CharField('字段名', max_length=64)
    data = JSONField('数据')
    rank = models.SmallIntegerField('优先级', default=0)

    def clean(self):
        if not isinstance(self.data, list):
            raise ValidationError('data is not a list')

    def __str__(self):
        return "%s --> %s" % (self.table.name, self.name)

    class Meta:
        verbose_name = '表头'
        verbose_name_plural = verbose_name


class Result(models.Model):
    table = models.ForeignKey(Table, verbose_name="表格", on_delete=models.CASCADE)
    label = models.CharField(max_length=64, null=True)
    value = models.IntegerField('值')
    computed_value = JSONField('计算值', null=True, editable=False)

    def __str__(self):
        return "%s: %s" % (self.label, self.value)

    def save(self, *args, **kwargs):
        if not self.computed_value:
            self.make_computed_value()
        super().save(*args, **kwargs)

    def make_computed_value(self):
        computed_value = {}
        headers = self.table.tableheader_set.all()
        for header in headers:
            assert isinstance(header.data, list)
            for index in range(len(header.data)):
                assert isinstance(header.data[index], list)
                if self.value in header.data[index]:
                    computed_value[header.id] = index

        self.computed_value = computed_value

    class Meta:
        verbose_name = '结果'
        verbose_name_plural = verbose_name


class CrawlHistory(models.Model):
    # crawl https://datachart.500.com/ssq/history/history.shtml

    HEADERS = ['date_code', 'red_1', 'red_2', 'red_3', 'red_4', 'red_5', 'red_6',
               'blue', 'happy_sunday', 'jackpot_bonuses', 'first_prize_num', 'first_prize_bonus',
               'second_prize_num', 'second_prize_bonus', 'total_bet', 'lottery_date']

    HEADER_LABELS = {
        'date_code': '期号',
        'red_1': '红1',
        'red_2': '红2',
        'red_3': '红3',
        'red_4': '红4',
        'red_5': '红5',
        'red_6': '红6',
        'blue': '蓝球',
        'happy_sunday': '快乐星期天',
        'jackpot_bonuses': '奖池奖金(元)',
        'first_prize_num': '一等奖注数',
        'first_prize_bonus': '一等奖奖金(元)',
        'second_prize_num': '二等奖注数',
        'second_prize_bonus': '二等奖奖金(元)',
        'total_bet': '总投注额(元)',
        'lottery_date': '开奖日期'
        }

    crawled_at = models.DateTimeField('爬取时间', null=True, editable=False)
    status = models.CharField('爬取状态', max_length=32, null=True, editable=False)
    data = JSONField('数据', null=True, editable=False)


class Pay(models.Model):
    user = models.ForeignKey(User, verbose_name="用户", on_delete=models.CASCADE)
    table = models.ForeignKey(Table, verbose_name="表格", on_delete=models.CASCADE)
    price = models.DecimalField('价格', max_digits=10, decimal_places=2)
    created_at = models.DateTimeField('支付时间', editable=False, default=timezone.now)

    class Meta:
        verbose_name = '支付记录'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s: ￥%s" % (self.created_at, self.price)


class Option(models.Model):
    name = models.CharField('项目', max_length=200, unique=True, editable=False)
    slug = models.CharField('Slug', max_length=200, unique=True, editable=False)
    value = models.CharField('值', max_length=250, null=True, blank=True)
    enable = models.BooleanField(default=True)

    class Meta:
        verbose_name = '选项'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
