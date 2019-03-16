import requests
from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import CrawlHistory, Table


@login_required
def sar(request, table_id):
    table = get_object_or_404(Table, pk=table_id)

    paginator = Paginator(table.result_set.all(), 25)

    page = request.GET.get('page', 1)

    results = paginator.get_page(page)
    headers = table.tableheader_set.all()

    return render(request, 'sar/table.html', {
        "headers": headers,
        "results": results,
        "table": table,
    })


def home(request):
    today = timezone.now()
    shuangseqiu_data = []
    crawl_history = CrawlHistory.objects.filter(crawled_at__date=today.date()).first()

    if crawl_history is None:
        r = requests.get('https://datachart.500.com/ssq/history/history.shtml')

        if r.status_code == requests.codes.ok:
            soup = BeautifulSoup(r.text)
            trs = soup.find_all('tr', class_='t_tr1')

            for tr in trs:
                tds = tr.find_all('td')
                values = [td.text for td in tds]
                data = dict(zip(CrawlHistory.HEADERS, values))
                shuangseqiu_data.append(data)

            if shuangseqiu_data:
                crawl_history = CrawlHistory(crawled_at=today, status='success', data=shuangseqiu_data)
                crawl_history.save()

    else:
        shuangseqiu_data = crawl_history.data

    return render(request, 'sar/home.html', {
        'tables': Table.objects.all(),
        "shuangseqiu_data": shuangseqiu_data,
        'headers': CrawlHistory.HEADERS,
        'header_labels': CrawlHistory.HEADER_LABELS
    })
