function drawImage() {
    var borderColor = '#a2bc18';
    var fillColor = '#DDEF7E';
    var canvas = $(this);

    var term1 = $(this).data('segments').split(',');
    var letters = ['A', 'B', 'C', 'D', 'E'];

    // Set canvas size based on lines number
    var max_width = 444;

    // instance canvas and context to create canvas
    var context = this.getContext("2d");

    // Set new canvas width and height based on perfect square found by tilesPerLine e linesNum
    context.canvas.width = max_width + 25;
    context.canvas.height = 80;

    // Straight
    context.beginPath();
    context.lineWidth = 2;
    context.strokeStyle = borderColor;
    context.opacity = 1;
    context.moveTo(7, 15);
    context.lineTo(max_width + 7, 15);
    context.stroke();
    context.closePath();

    var width = 0;
    var space = max_width / 10;

    // Vertical Lines
    while (width <= max_width) {
        context.beginPath();
        context.lineWidth = 2;
        context.strokeStyle = 'black';
        context.opacity = 1;
        context.moveTo(width + 7, 25);
        context.lineTo(width + 7, 5);
        context.stroke();
        context.closePath();
        width = width + space;
    }

    // Letters
    for (var i in term1) {
        context.beginPath();
        context.font = '20px Helvetica';
        context.fillStyle = 'black';
        context.fillText(letters[i], (parseInt(term1[i])) * space, 45);
        context.closePath();
    }
}

$(function() {
	$('canvas.segments').each(drawImage);
});
