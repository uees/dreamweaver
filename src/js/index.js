const $ = window.$;

window.drawLine = function drawLine(context, color, start, end) {
    context.strokeStyle = color;
    context.moveTo(start.left, start.top);
    context.lineTo(end.left, end.top);
    context.stroke();
};

window.fixedCol = function fixedCol() {
    $("#content").scroll(function () {
        const left = $(this).scrollLeft(); // 获取盒子滚动距离
        const tds = $("#content table tr .label-title");   // 获取所有要固定的td
        if (left > 0) {
            // 获取每一行下面的 td 或者 th , 设置相对定位，偏移距离为盒子滚动的距离即 left
            tds.each(function (i) {
                $(this).css({
                    "position": "relative",
                    "top": "0",
                    "left": left,
                    "background": "#999",
                    'z-index': 66,
                    'opacity': 0.9,
                });
            });
        } else {
            tds.each(function (i) {
                $(this).css({
                    "position": "static",
                    "top": "none",
                    "left": 'none',
                    "background": "#fbfbfb",
                    'z-index': 'auto',
                    'opacity': 1,
                });
            });
        }
    });
};

window.FixedHead = function FixedHead() {
    if (!(this instanceof FixedHead)) {
        return new FixedHead()
    }

    this.$dom = $('thead'); // 表头外层dom
    this.offsetTop = this.$dom.offset().top; // 表头外层dom距离顶部的高度
    this.parents = this.$dom.parents('#content'); //  表头外层dom最外面的盒子（包裹着table的盒子）
    this.outBoxHeight = this.parents.height(); // 表头外层dom最外面的盒子（包裹着table的盒子）的高度
    this.maxHeight = this.offsetTop + this.outBoxHeight; // 滚动的零界点 最多能滚动到哪里

    this.scroll();
};

window.FixedHead.prototype = {
    constructor: FixedHead,
    scroll: function () {
        const that = this;
        $(window).scroll(function () {
            const scrollTop = $(this).scrollTop();
            if ((scrollTop > that.offsetTop) && (scrollTop < that.maxHeight)) {
                that.$dom.css({
                    'top': (scrollTop - that.offsetTop) + 'px',
                    'position': 'absolute',
                    'z-index': 99,
                });
                that.parents.css({
                    'position': 'relative',
                    'padding-top': `${that.$dom.height()}px`,
                });
            } else {
                const topCss = that.$dom.css('position');
                if (topCss !== 'static') {
                    that.$dom.css({
                        'top': '0px',
                        'position': 'static',
                        'z-index': 'auto',
                    });
                    that.parents.css({
                        'position': 'static',
                        'padding-top': 0,
                    })
                }
            }
        })
    }
};

window.resetTable = function resetTable() {
    const table = $('table.table');
    const content = $('#content');

    content.height(table.height());

    if (table.width() > content.width()) {
        content.css({
            'overflow-x': 'scroll',
            'overflow-y': 'hidden',
        });
        content.height(table.height() + 25);
    }
};

window.drawLines = function drawLines(headers_length, results_length) {
    const table = document.querySelector('table');
    const table_height = $(table).height();
    const tableOffset = $(table).offset();
    const pointsMap = [];

    for (let i = 0; i < headers_length; i++) {
        const points = [];
        for (let j = 0; j < results_length; j++) {
            const pointOffset = $(`#result-${j} span.point-${i}`).offset();
            const point = {
                top: pointOffset.top - tableOffset.top + 2,
                left: pointOffset.left - tableOffset.left + 7,
            };
            points.push(point);
        }
        pointsMap.push(points);
    }

    const canvas = document.getElementById("my-canvas");

    canvas.width = $(table).width();
    canvas.height = table_height - 55;
    canvas.style.top = '-' + table_height + 'px';

    const context = canvas.getContext("2d");
    pointsMap.forEach(function (points) {
        points.reduce(function (total, currentValue, currentIndex) {
            if (currentIndex > 0) {
                // 画线
                drawLine(context, '#007bff', total, currentValue)
            }
            return currentValue
        })
    });
};

$(function () {
    $('[data-toggle="offcanvas"]').on('click', function () {
        $('.offcanvas-collapse').toggleClass('open')
    });
});
