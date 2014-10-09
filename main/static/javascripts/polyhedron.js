function drawImage() {
    var bgcolor = '#DDEF7E';

    var canvas = $(this);

	// parse data from html canvas tag
	var term1 = parseInt($(this).data('term1'));
	var term2 = parseInt($(this).data('term2'));
	var term3 = parseInt($(this).data('term3'));

	// Set canvas size based on lines number
    max_width = 150
    max_value = Math.max(term1, term2, term3)
	var term1 = (term1 / max_value)  * max_width;
	var term2 = (term2 / max_value) * max_width;
	var term3 = (term3 / max_value) * max_width;

	// instance canvas and context to create canvas
	var context = this.getContext("2d");

	// Set new canvas width and height based on perfect square found by tilesPerLine e linesNum
	context.canvas.width = term2 + (term3 / 2) + 10;
	context.canvas.height = term1 + (term3 / 2) + 30;

    // Front quadrangular
    context.lineWidth = 2;
    context.strokeStyle = fgcolor;
    context.rect(term3 / 2, term3 / 2, term2, term1);
	context.stroke();

    // Line top right
    context.beginPath();
    context.lineWidth = 2;
    context.strokeStyle = fgcolor;
    context.moveTo(2, 2);
    context.lineTo(term3 / 2, term3 / 2);
    context.stroke();
    context.closePath();

    // Line top left
    context.beginPath();
    context.lineWidth = 2;
    context.strokeStyle = fgcolor;
    context.moveTo(term2, 2);
    context.lineTo(term3 / 2 + term2, term3 / 2);
    context.stroke();
    context.closePath();

    // Line buttom left
    context.beginPath();
    context.lineWidth = 2;
    context.strokeStyle = fgcolor;
    context.moveTo(2, term1);
    context.lineTo(term3 / 2, (term3 / 2) + term1);
    context.stroke();
    context.closePath();

    // Line top
    context.beginPath();
    context.lineWidth = 2;
    context.strokeStyle = fgcolor;
    context.moveTo(2, 2);
    context.lineTo(2, term1);
    context.stroke();
    context.closePath();

    // Line ago left
    context.beginPath();
    context.lineWidth = 2;
    context.strokeStyle = fgcolor;
    context.moveTo(2, 2);
    context.lineTo(term2, 2);
    context.stroke();
    context.closePath();
}

$(function() {
	$('canvas.polyhedron').each(drawImage);
});
