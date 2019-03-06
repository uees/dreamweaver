from django.db import models
from django.core.exceptions import ValidationError
from django_extensions.db.fields.json import JSONField


class Table(models.Model):
    name = models.CharField('表名', max_length=64)

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
    value = models.IntegerField('值')
    computed_value = JSONField('计算值', null=True, editable=False)

    def __str__(self):
        return "%s(%s)" % (self.table.name, self.value)

    def save(self, *args, **kwargs):
        self.computed_value = self._computed_value()
        super().save(*args, **kwargs)

    def _computed_value(self):
        computed_value = {}
        headers = self.table.tableheader_set.all()
        for header in headers:
            assert isinstance(header.data, list)
            for index in range(len(header.data)):
                assert isinstance(header.data[index], list)
                if self.value in header.data[index]:
                    computed_value[header.id] = index

        return computed_value

    class Meta:
        verbose_name = '结果'
        verbose_name_plural = verbose_name


class CrawlHistory(models.Model):
    # crawl https://datachart.500.com/ssq/history/history.shtml
    crawled_at = models.DateTimeField('爬取时间', null=True, editable=False)
    status = models.CharField('爬取状态', max_length=32, null=True, editable=False)
    data = JSONField('数据', null=True, editable=False)
