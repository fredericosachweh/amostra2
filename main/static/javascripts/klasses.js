function updateModules(items) {
    var modules = $.map(items, function(el) {
        return $(el).data('module');
    })
    $('.program-modules').prev('input').val(modules.join(','));
}

function hideModules(items) {
    items.hide();
}

function showModules(items) {
    items.show();
    updateModules(items);
}

$(document).ready(function() {
    // hides any program, they will be shown after choose a program
    hideModules($('.program-modules li'));

    // makes the internal buttons to continue and go back triggers the section tabs
    $('[data-section-alt]').click(function(event) {
        event.preventDefault();
        $('.title a[href="' + $(this).attr('href') + '"]').click()
    });

    $('.program input[type=radio]').click(function() {
        $('.program').removeClass('active');
        $(this).parents('.program').addClass('active');

        // when choose the program, also shows the proper modules
        hideModules($('.program-modules li'));
        showModules($('.program-modules li[data-program="' + $(this).val() + '"]'));
    });

    $('.program-modules').sortable();
    $('.program-modules').bind('sortupdate', function() {
        var items = $(this).find('li:visible');
        updateModules(items);
    });
});
