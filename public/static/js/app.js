'use strict';

const drawLine = function(context, color, start, end) {
    context.strokeStyle = color;
    context.moveTo(start.left, start.top);
    context.lineTo(end.left, end.top);
    context.stroke();
};

$(function () {
    $('[data-toggle="offcanvas"]').on('click', function () {
        $('.offcanvas-collapse').toggleClass('open')
    });
});
