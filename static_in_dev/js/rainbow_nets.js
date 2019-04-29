"use strict";

//Change values for different effect:
var settings = {
    pointsCount: 180,
    colorSteps: 2,
    mouseRadius: 150,
    maxLineLength: 80,
    radius: {
        max: 2.5,
        min: 0.5
    },
    speed: {
        max: 0.05,
        min: 0.01
    }
};
window.onload = function () {
    startNetAnimation();
}

var animationRunning = false;

function startNetAnimation() {
    if (!animationRunning) {
        animationRunning = true;
        initNetAnimation()
    } else {
        animationRunning = false;
    }
}

var canvas;
var ctx;
var points = [];

function initNetAnimation() {
    canvas = document.getElementById('netAnimationCanvas');
    ctx = canvas.getContext("2d");
    var header = $('#netAnimation');
    canvas.width = header.outerWidth();
    canvas.height = header.outerHeight();

    document.onmousemove = mouseOver;
    document.addEventListener('touchstart', touchHandler, false)

    for (var i = 0; i < settings.pointsCount; i++) {
        points.push(new Point())
    }

    draw();
}

function draw() {
    if (!animationRunning) return;
    requestAnimationFrame(draw);

    ctx.fillStyle = "rgb(0,0,0)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    for (var i = 0; i < points.length; i++) {
        updatePointPos(points[i]);
    }

    var pointsAround = getPointsAroundMouse();
    for (var a = 0; a < pointsAround.length; a++) {
        for (var b = a + 1; b < pointsAround.length; b++) {
            drawGradient(pointsAround[a], pointsAround[b]);
        }
    }
}

function getPointsAroundMouse() {
    return points.filter(function (point) {
        return Math.sqrt((point.x - mouse.x) * (point.x - mouse.x) + (point.y - mouse.y) * (point.y - mouse.y)) < settings.mouseRadius
    })
}

function drawGradient(point1, point2) {
    if ((point1.x - point2.x) * (point1.x - point2.x) + (point1.y - point2.y) * (point1.y - point2.y) < settings.maxLineLength * settings.maxLineLength) {
        var grad = ctx.createLinearGradient(point1.x, point1.y, point2.x, point2.y);
        grad.addColorStop(0, point1.color);
        grad.addColorStop(1, point2.color);
        ctx.strokeStyle = grad;
        ctx.beginPath();
        ctx.moveTo(point1.x, point1.y);
        ctx.lineTo(point2.x, point2.y);
        ctx.stroke();
    }
}

var colorCounter = 0;

function Point() {
    var radius = Math.floor(Math.random() * settings.radius.max) + settings.radius.min;
    var brightness = Math.floor(Math.random() * 10) + 45;
    var color = "hsl(" + (colorCounter += settings.colorSteps) + ", 100%, " + brightness + "%)";
    if (colorCounter >= 360) colorCounter = 0;
    var positionX = Math.floor(Math.random() * canvas.width) + radius / 2;
    var positionY = Math.floor(Math.random() * canvas.height) + radius / 2;
    var speed = Math.random() * settings.speed.max + settings.speed.min;
    var speedX = Math.random() * 2 - 1;
    var speedY = Math.random() * 2 - 1;
    var speedCorrection = speed / Math.sqrt(speedX * speedX + speedY * speedY);
    speedX *= speedCorrection;
    speedY *= speedCorrection;
    this.construct(radius, color, positionX, positionY, speedX, speedY);
}

Point.prototype = {
    construct: function (radius, color, x, y, speedX, speedY) {
        this.radius = radius;
        this.x = x;
        this.y = y;
        this.color = color;
        this.vx = speedX;
        this.vy = speedY;

    },
    draw: function () {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2, false);
        ctx.fillStyle = this.color;
        ctx.fill();
        ctx.closePath();
    }
};

function updatePointPos(point) {

    point.y += point.vy;
    point.x += point.vx;

    if (point.y - point.radius <= 0) {
        point.y = point.radius;
        point.vy = -point.vy;
    } else if (point.y + point.radius >= canvas.height) {
        point.y = canvas.height - point.radius;
        point.vy = -point.vy
    }

    if (point.x - point.radius <= 0) {
        point.x = point.radius;
        point.vx = -point.vx;
    } else if (point.x + point.radius >= canvas.width) {
        point.x = canvas.width - point.radius;
        point.vx = -point.vx;
    }

    point.draw();
}

var mouse = {
    x: 0,
    y: 0
};

function mouseOver(e) {
    var canvasRect = canvas.getBoundingClientRect();
    mouse = {
        x: e.clientX - canvasRect.left,
        y: e.clientY - canvasRect.top
    };
}

function touchHandler(e) {
    e.preventDefault();
    var touchobj = e.changedTouches[0];
    var canvasRect = canvas.getBoundingClientRect();
    mouse = {
        x: touchobj.clientX - canvasRect.left,
        y: touchobj.clientY - canvasRect.top
    };
}