from django.core.management import BaseCommand

from sar.models import Option


class Command(BaseCommand):
    help = '填充 options 表'

    def handle(self, *args, **options):
        Option.objects.get_or_create(
            name="网站名称", slug="site_name",
            defaults=dict(value='Sar888'))
        Option.objects.get_or_create(
            name="网站描述", slug="site_description",
            defaults=dict(value='精彩"6+1"预测走势'))
        Option.objects.get_or_create(
            name="QRCode标题", slug="qrcode_title",
            defaults=dict(value='精彩"6+1"预测走势'))
        # options = [Option(slug=slug, value=None) for slug in []]
        # Option.objects.bulk_create(options)
        self.stdout.write(self.style.SUCCESS('填充 options 表成功'))
