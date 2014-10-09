function drawTriangle() {
    var borderColor = '#a2bc18';
    var fillColor = '#DDEF7E';
    var canvas = $(this);

    // parse data from html canvas tag
    var term1 = parseInt($(this).data('term1'));
    var term2 = parseInt($(this).data('term2'));

    // Set canvas size based on lines number
    var max_width = 150;
    var max_value = Math.max(term1, term2);
    var term1 = (term1 / max_value + 0.3)  * max_width;
    var term2 = (term2 / max_value + 0.3) * max_width;

    // instance canvas and context to create canvas
    var context = this.getContext("2d");

    // Set new canvas width and height based on perfect square found by tilesPerLine e linesNum
    context.canvas.width = term2 + 5;
    context.canvas.height = term1 + 25;

    // Triangle
    context.beginPath();
    context.lineWidth = 2;
    context.strokeStyle = borderColor;
    context.fillStyle = fillColor;
    context.opacity = 1;
    context.moveTo(2, 2);
    context.lineTo(2, term1);
    context.lineTo(term2, term1 - 2);
    context.lineTo(2, 2);
    context.stroke();
    context.fill();
    context.closePath();

    // Small square
    context.beginPath();
    context.lineWidth = 2;
    context.strokeStyle = borderColor;
    context.fillStyle = fillColor;
    context.opacity = 1;
    context.moveTo(2, term1 - 20);
    context.lineTo(22, term1 - 20);
    context.lineTo(22, term1);
    context.stroke();
    context.fill();
    context.closePath();

    // Point
    context.beginPath();
    context.lineWidth = 2;
    context.strokeStyle = borderColor;
    context.fillStyle = fillColor;
    context.opacity = 1;
    context.moveTo(12, term1 - 8);
    context.lineTo(12, term1 - 10);
    context.stroke();
    context.fill();
    context.closePath();
    
    // Text
    context.beginPath();
    context.font = '20px Helvetica';
    context.fillStyle = 'black';
    context.fillText("b",term2 / 2 - 10, term1 + 20);
    context.fillText("h", 5, (term1 / 2 + 20));
    context.closePath();
}

$(function() {
	$('canvas.triangle').each(drawTriangle);
});
