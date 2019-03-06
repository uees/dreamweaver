from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import Table, CrawlHistory


def sar(request, table_id):
    table = get_object_or_404(Table, pk=table_id)

    paginator = Paginator(table.result_set.all(), 25)

    page = request.GET.get('page', 1)

    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)

    return render(request, 'sar/table.html', {
        "headers": table.tableheader_set.all(),
        "results": results,
        "table": table,
    })


def home(request):
    # TODO 获取当前时间, 查今天的爬取历史, 获取双色球数据
    # 如果没有数据，则爬
    # shuangseqiu_data = ...
    return render(request, 'sar/home.html', {
        # "shuangseqiu_data": shuangseqiu_data,
    })
