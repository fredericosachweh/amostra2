django.jQuery(document).ready(function($) {
    $('#question_set-group .td.type select').change(function() {
        var val = $(this).val();
        var container = $(this).parent().parent();
        container.find('.td').not('.type, .position, .group').find('input, select, textarea').hide();
        if (val == 'char') {
            container.find('.td').filter('.char_value').find('input').show();
        } else if (val == 'boolean') {
            container.find('.td').filter('.boolean_value').find('select').show();
        } else if (val == 'text') {
            container.find('.td').filter('.text_value').find('textarea').show();
        } else if (val == 'image') {
            container.find('.td').filter('.image_value').find('input').show();
        }
    }).change();
});

