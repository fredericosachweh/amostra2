function toggleDate(e) {
    e.preventDefault();

    var td = $(this).parents('td');

    $.ajax({
        url: this.href,
        type: 'get',
        dataType: 'json',
        success: function(data) {
            td.attr('class', data.state);
        }
    });
}

$(document).ready(function() {
    $('#excluded-dates').on('click', '[data-action=toggle-date]', toggleDate);
});
