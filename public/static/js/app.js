'use strict';

const createPoint = function (container, x, y) {
    const node = document.createElement('div');
    node.className = 'line';
    node.style.top = y + 'px';
    node.style.left = x + 'px';
    container.appendChild(node);
};

const line = function (startX, startY, endX, endY, container) {
    if (startX === endX) {
        if (startY > endY) {
            let tempY = startY;
            startY = endY;
            endY = tempY;
        }
        for (let k = startY; k < endY; k++) {
            createPoint(container, startX, k);
        }
    }
    // y = ax + b
    let a = (startY - endY) / (startX - endX);
    let b = startY - ((startY - endY) / (startX - endX)) * startX;

    if (startX > endX) {
        let tempX = endX;
        endX = startX;
        startX = tempX;
    }
    for (let i = startX; i <= endX; i++) {
        createPoint(container, i, a * i + b);
    }
};

$(function () {
    $('[data-toggle="offcanvas"]').on('click', function () {
        $('.offcanvas-collapse').toggleClass('open')
    });
});
