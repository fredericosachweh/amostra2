function drawTiles() {
    var canvas = $(this);

	// parse data from html canvas tag
	var term1 = parseInt($(this).data('term1'));
	var extraStroke = $(this).data('extra-stroke');
	var maxTileSize = parseInt($(this).data('max-tile-size'));

	// find next perfect square from term1
	var tilesPerLine = Math.ceil(Math.sqrt(term1));
	// set number of lines needed to build tiles
	var linesNum = Math.ceil(term1 / tilesPerLine);
	// Set canvas size based on lines number
	var canvasWidth = tilesPerLine * maxTileSize;
	var canvasHeight = linesNum * maxTileSize;
	// set tile size based on data-max-tile-size from html
	var tileSize = canvasWidth / tilesPerLine;

	// instance canvas and context to create canvas
	var context = this.getContext("2d");

	// Set new canvas width and height based on perfect square found by tilesPerLine e linesNum
	context.canvas.width = canvasWidth;
	context.canvas.height = canvasHeight;

	// set draw common variables
	var i = 1;
	var row = 1;
	var column = 0;
	var posx = 0;
	var posy = 0;

	while (i <= term1) {
        // Build rectangles
		context.rect(posx, posy, tileSize, tileSize);
		context.fillStyle = 'orange';
		context.fill();

        context.lineWidth = 1;
        context.strokeStyle = 'black';
        context.stroke();

		if (extraStroke == '1') {
			// Add right stroke to last tile of the first line
			if (row == 1 && (i == tilesPerLine)) {
				context.beginPath();
				context.lineWidth = 5;
				context.strokeStyle = 'black';
				context.moveTo((posx + tileSize - 2), posy);
				context.lineTo((posx + tileSize - 2), (posy + tileSize));
				context.stroke();
				context.closePath();

				// Add bottom stroke to last tile of the first line if the tiles dont fill a entire row
				if (Math.pow(tilesPerLine, 2) > term1 && (tilesPerLine * linesNum) != term1 && tilesPerLine != linesNum){
					context.beginPath();
					context.lineWidth = 5;
					context.strokeStyle = 'black';
					context.moveTo((posx - 5), (posy + tileSize));
					context.lineTo((posx + tileSize), (posy + tileSize));
					context.stroke();
					context.closePath();
				}
			}

			// Add right stroke to last item of the row, only if row is not the first or last
			if(row > 1 && linesNum == tilesPerLine && (i % tilesPerLine) == 0){
				context.beginPath();
				context.lineWidth = 5;
				context.strokeStyle = 'black';
				context.moveTo((posx + tileSize - 2), posy);
				context.lineTo((posx + tileSize - 2), (posy + tileSize));
				context.stroke();
				context.closePath();
			}

			// Add bottom stroke to tiles on the last row
			if ((linesNum) == row) {
				context.beginPath();
				context.lineWidth = 5;
				context.strokeStyle = 'black';
				context.moveTo(0, (posy + tileSize - 2));
				context.lineTo((posx + tileSize - 2), (posy + tileSize - 2));
				context.stroke();
				context.closePath();
			}

			if (i == (term1)) {
				// Add right stroke to last tile of last row
				context.beginPath();
				context.lineWidth = 5;
				context.strokeStyle = 'black';
				context.moveTo((posx + tileSize - 2), posy);
				context.lineTo((posx + tileSize - 2), (posy + tileSize));
				context.stroke();
				context.closePath();

                // Add top right stroke to last tiles of last rown until canvas right side
				context.beginPath();
				context.lineWidth = 5;
				context.strokeStyle = 'black';
				context.moveTo((posx + tileSize - 5), posy);
				context.lineTo(canvasWidth, posy);
				context.stroke();
				context.closePath();
			}
		}

		// Change tile x-position
		column = column + 1;
		posx = column * tileSize;

		// Breaks tiles to build a perfect square
		if ((i % (tilesPerLine)) == 0) {
			row = row + 1;
			posy = (row - 1) * tileSize;
			posx = 0;
			column = 0;
		}

		i++;
	}

	// if extra stroke is set up, make a top perimeter border
	if (extraStroke == '1') {
		//set canvas full width top stroke
		context.beginPath();
		context.lineWidth = 5;
		context.strokeStyle = 'black';
		context.moveTo(2, 2);
		context.lineTo(canvasWidth + 2, 2);
		context.stroke();
		context.closePath();

		//set canvas full height left stroke
		context.beginPath();
		context.lineWidth = 5;
		context.strokeStyle = 'black';
		context.moveTo(2, 0);
		context.lineTo(2, canvasHeight + 2);
		context.stroke();
		context.closePath();
	}
}

$(function() {
	$('canvas.tile').each(drawTiles);
});
