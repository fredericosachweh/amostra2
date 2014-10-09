function checkCustomBoolean() {
    $(this).toggleClass('checked');

    var input = $(this).prev('input[name$=value]');
    if($(this).is('.checked'))
        input.val('1');  // true
    else
        input.val('');  // false
}

$(document).ready(function() {

    $('#exercise .commas input[name$=value]').each(function() {
        $('<a>').attr('tabindex', $(this).attr('tabindex'))
                .html('<span>,</span>')
                .css('visibility', 'hidden')
                .insertAfter($(this))
                .click(checkCustomBoolean)
                .keypress(function(e) {
                    if(e.which == 13)
                        checkCustomBoolean.call(this);
                });
    });

    $('#exercise .line:last').find('input[type=text]').first().focus(function() {
        $('#exercise .commas a').css('visibility', 'visible');
    });
});


function doBorrow() {
    // The borrow information resides in the support field, if the user set the
    // support field, it means he turns borrow on. Any field is hidden by
    // default, we need to make inputs visible and deal with the checked class
    // for span and inputs as well
    var index = $(this).parent().find('span').index(this);
    var items = $(this).closest('.line').prev('.borrowed').children('span, input[type=text]');
    $(this).toggleClass('checked');

    if($(this).is('.checked'))
        items.eq(index).css('visibility', 'visible').focus();
    else
        items.eq(index).css('visibility', 'hidden').focus();
}

function adjustWidth() {
    var container = $(this).parent();
    if($(this).is('.width-ref-self')) {
        var ref = $(this);
        var first = $(this);
    } else {
        var ref = $(this).children('input[type=text], span, div');
        ref = ref.not('.commas');
        var first = ref.first();
    }

    var width = 0;
    ref.each(function() {
        width += $(this).outerWidth(true);  // including padding, border and margin
    });

    var prevWidth = container.data('width');
    if(typeof(prevWidth) == 'undefined')
        prevWidth = 0;

    container.data('width', prevWidth + width);
    container.width(prevWidth + width + 'px');
}

function applyWidth(container) {
    var refs = $(container).find('.width-ref:visible');
    for(var i=refs.length; i>0; i--)
        adjustWidth.call(refs[i-1]);
}

//adjustWidth.call($('.detail section:eq(1) .width-ref')[0])

function Timer(container) {
    this.container = $(container);
    this.interval = 0;

    this.timeFormat = function(s) {
        var seconds = parseInt(s);
        var hh = Math.floor(seconds / 3600);
        var mm = Math.floor((seconds - (hh * 3600)) / 60);
        var ss = seconds - (hh * 3600) - (mm * 60);

        if (mm < 10) { mm = '0' + mm }
        if (ss < 10) { ss = '0' + ss }

        var t = mm + ':' + ss;

        if (hh > 0) {
            if (hh < 10) { hh = '0' + hh }
            t = hh + ':' + t;
        }

        return t;
    };

    this.updateTime = function() {
        this.interval += 1;
        this.container.text(this.timeFormat(this.interval));
    };

    this.activate = function () {
        var my = this;
        this.timer = setInterval(function() { my.updateTime() }, 1000);
    };
}

$(document).ready(function() {
    // adjust the width of the content area based in how many fields there is
    // in the reference line.
    applyWidth($('#exercise'));
    var hiddenSections = $('#exercise .section-container section').not('.active');
    hiddenSections.one('opened.fndtn.section', function() {
        applyWidth($(this));
    });

    // Controls the boolean fields for borrow in subtractions
    $('#exercise form .borrow span').click(doBorrow);

    // In detail views, make the checked borrowed visually checked
    $('#exercise .detail .borrow span[data-check=checked]').each(doBorrow);

    $('[data-counter]').each(function() {
        var timer = new Timer(this);
        timer.activate();
    });

    var inputs = $('form input[tabindex]')
    inputs.not('[tabindex="1"]').css('visibility', 'hidden');
    inputs.focus(function() {
        var next = parseInt($(this).attr('tabindex')) + 1;
        var next_elem = inputs.filter('[tabindex="' + next + '"]');
        next_elem.css('visibility', 'visible');

        // show initially-hidden elements
        var container = next_elem.parent();
        if(container.is(':hidden'))
            container.show();
    });
});
