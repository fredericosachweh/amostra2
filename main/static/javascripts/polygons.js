function drawRegularPolygon() {
    var context = this.getContext('2d');
    var numberOfSides = parseInt($(this).data('term'));
        if ($(this).width() == 0) {
            size = 70,
            Xcenter = window.x,
            Ycenter = window.y;
        }
        else {
            size = 70,
            Xcenter = $(this).width() / 2,
            Ycenter = $(this).height() / 2;
            //get xcenter, ycenter to centralize polygon of incorrect answer
            window.x = Xcenter;
            window.y = Ycenter;
        }

    context.beginPath();
    context.moveTo(Xcenter +  size * Math.cos(0), Ycenter +  size *  Math.sin(0));

    for (var i = 1; i <= numberOfSides;i += 1) {
        context.lineTo (Xcenter + size * Math.cos(i * 2 * Math.PI / numberOfSides), Ycenter + size * Math.sin(i * 2 * Math.PI / numberOfSides));
    }

    context.strokeStyle = "#000000";
    context.fillStyle = '#a2bc18';
    context.lineWidth = 6;
    context.stroke();
    context.fill();
}

$(document).ready(function() {
    $('#exercise canvas.polygon').each(drawRegularPolygon);
});
