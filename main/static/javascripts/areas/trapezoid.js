function drawTrapezoid() {
    var borderColor = '#a2bc18';
    var fillColor = '#DDEF7E';
    var canvas = $(this);

    // parse data from html canvas tag
    var height = parseInt($(this).data('height'));
    var largerBase = parseInt($(this).data('larger-base'));
    var shorterBase = parseInt($(this).data('shorter-base'));

    // Set canvas size based on lines number
    var maxWidth = 150;
    var maxValue = Math.max(height, largerBase);
    var height = (height / maxValue + 0.3)  * maxWidth;
    var largerBase = (largerBase / maxValue + 0.3) * maxWidth;
    var shorterBase = (shorterBase / maxValue + 0.3)  * maxWidth;

    // instance canvas and context to create canvas
    var context = this.getContext("2d");

    // Set new canvas width and height based on perfect square found by tilesPerLine e linesNum
    context.canvas.width = largerBase + 10;
    context.canvas.height = height + 10;

    context.beginPath();
    context.lineWidth = 2;
    context.strokeStyle = borderColor;
    context.fillStyle = fillColor;
    context.opacity = 1;

    delta = (largerBase - shorterBase) / 2;

    context.moveTo(5, height + 5);
    context.lineTo(5 + largerBase, height + 5);
    context.lineTo(5 + shorterBase + delta, 5);
    context.lineTo(5 + delta, 5);
    context.lineTo(5 + 0, height + 5);
    context.stroke();
    context.fill();
    context.closePath();

    // Dotted line
    context.beginPath();
    context.setLineDash([5]);
    context.lineWidth = 2;
    context.strokeStyle = borderColor;
    context.moveTo(delta + 5, height + 5);
    context.lineTo(delta + 5, 5);
    context.stroke();
    context.closePath();

    // Text
    context.beginPath();
    context.font = '20px Helvetica';
    context.fillStyle = 'black';
    context.fillText("b", largerBase / 2, 30);
    context.fillText("B", largerBase / 2, height - 5);
    context.fillText("h", delta + 10, height / 2 + 20);
    context.closePath();
}

$(function() {
	$('canvas.trapezoid').each(drawTrapezoid);
});
