function formatFraction() {
    var terms = $(this).text();
    if(terms.search('/') == -1)
        return;
    else
        terms = terms.split('/');

    var tmpl = '<small class="small-group"><b>' +
               terms[0] +
               '</b><b>' +
               terms[1] +
               '</b></small>';
    $(this).replaceWith(tmpl);
}


function drawArc(context, term1, term2, slice, x, y, radius) {
    for (var i=0; i<term2; i++) {
        var start = slice * i,
            end = slice * (i + 1),
            dark;

        if ((i + 1) <= term1)
            dark = true;
        else
            dark = false;

        context.save();

        origin = 3 * Math.PI / 2;
        context.beginPath();
        context.moveTo(x, y);
        context.arc(x, y, radius, origin + start, origin + end, false);
        context.closePath();

        if (dark)
            context.fillStyle = '#a2bc18';
        else
            context.fillStyle = '#e6e6e6';
        context.fill();

        context.lineWidth = 1;
        context.strokeStyle = '#555555';
        context.stroke();

        context.restore();
    }
}

function drawPieFraction() {
    if($(this).data('terms')) {
        var terms = $(this).data('terms').split('/');
        var term1 = parseInt(terms[0]);
        var term2 = parseInt(terms[1]);
    } else {
        var term1 = parseInt($(this).data('term1'));
        var term2 = parseInt($(this).data('term2'));
    }
    var slice = 2 * Math.PI / term2;

    var x = $(this).width() / 2;
    var y = $(this).height() / 2;
    var radius = ($(this).width() - 2) / 2;

    var context = this.getContext('2d');
    context.canvas.width = $(this).width();
    context.canvas.height = $(this).height();

    if(term1 <= term2) {
        drawArc(context, term1, term2, slice, x, y, radius);
    } else {
        // Improper fractions doubles his width plus a margin to put 2 pies
        var newWidth = $(this).width() * 2 + 10;
        $(this).width(newWidth + 'px');
        context.canvas.width = newWidth;

        term1 = term1 % term2;
        drawArc(context, term2, term2, slice, x, y, radius);  // full circle
        drawArc(context, term1, term2, slice, 3*x + 10, y, radius);  // rest
    }

}


function tableSelectsStartDrag() {
    $(this).parents('table').data('drag', true);
    $(this).mouseover();
}


function tableSelectsStopDrag() {
    $(this).parents('table').data('drag', false);
}


function tableSelectsCheck(e) {
    if(!$(this).parents('table').data('drag'))
        return;

    var f = $('[name$=value]');
    if(f.val())
        var i = parseInt(f.val());
    else
        var i = 0;

    var w = $(e.target);
    w.toggleClass('selected');
    if(w.is('.selected'))
        f.val(i + 1);
    else
        f.val(i - 1);
}


function tableSelectsFill() {
    var limit = parseInt($(this).data('selected'));
    $(this).find('td').slice(0, limit).addClass('selected');
}


$(document).ready(function() {
    $('#exercise canvas.pie').each(drawPieFraction);
    $('#exercise [data-fraction]').each(formatFraction);

    // given a table, count how many cells were checked
    $('#exercise.fracoes form table td').mousedown(tableSelectsStartDrag);
    $('#exercise.fracoes form table td').mouseup(tableSelectsStopDrag);
    $('#exercise.fracoes form table td').mouseover(tableSelectsCheck);
    $('#exercise.fracoes table[data-selected]').each(tableSelectsFill);
});
