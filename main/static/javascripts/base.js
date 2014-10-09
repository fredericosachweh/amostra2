function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = $.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function setHeader(xhr, settings) {
    xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
}

/*
 * Adds a checkbox with ID check-all to make it controls the checked property
 * of checkboxes in the same module container.
 */
$(function() {
    $('#check-all').change(function() {
        $(this).parents('.module').find('input[type=checkbox]').not(this).prop('checked', $(this).is(':checked'));
    });
});


function AjaxHandler() {
    /**
      * Class to deal with ajax forms.
      */
}

AjaxHandler.prototype.showForm = function(w, e, successHandler, closedHandler, loadedHandler) {
    /**
      * Opens the form within a modal instance and configure the
      * events after the modal complete.
      *
      * Can receive a successHandler that will be called after the ajax
      * form is posted, a closedHandler to act after the modal is closed and
      * a loadedHandler called just after opens the modal.
      */
    e.preventDefault();
    var my = this;

    my.modal = $('<div>').addClass('reveal-modal small').appendTo('body');
    $.get($(w).attr('href'), function(data) {
        // replace modal content and add a remove link
        my.modal.empty().html(data);
        my.modal.append('<a class="close-reveal-modal">&#215;</a>');

        // when closed, runs the calls handler
        my.modal.bind('closed.fndtn.reveal', function() {
            if (typeof(closedHandler) != 'undefined') {
                closedHandler.call(my, w);
            }
        });

        // when opened, bind the form submission
        my.modal.bind('opened.fndtn.reveal', function() {
            my.modal.on('submit', '.ajax-form', function(e) { my.processData(this, e, successHandler, loadedHandler) });
        });

        // open reveal and attach any close link in the content
        my.modal.foundation('reveal', 'open');
        my.modal.on('click', '[data-reveal-close]', function(event) {
            event.preventDefault();
            my.modal.foundation('reveal', 'close');
        });

        if(typeof(loadedHandler) != 'undefined')
            loadedHandler.call(my);
    });
};

AjaxHandler.prototype.processData = function(form, e, successHandler, loadedHandler) {
    /*
     * Handles the ajax form submit. In case of errors, replace the form with
     * the error response.
     */
    e.preventDefault();
    var my = this;
    $.ajax({
        url: $(form).attr('action'),
        type: 'post',
        dataType: 'html',
        data: $(form).serialize(),
        beforeSend: function(xhr, settings) { setHeader(xhr, settings); },
        success: function(data) { successHandler.call(my, data); },
        error: function(xhr) {
            $(form).replaceWith(xhr.responseText);

            if(typeof(loadedHandler) != 'undefined')
                loadedHandler.call(my);
        }
    });
};


function QuickModal() {
}

QuickModal.prototype = new AjaxHandler();
QuickModal.prototype.constructor = QuickModal;

QuickModal.prototype.openModal = function(selector, successHandler, closedHandler, loadedHandler) {
    var my = this;

    $('body').on('click', selector, function(e) {
        my.showForm(this, e, successHandler, closedHandler, loadedHandler);
    });
}

function quickModal(selector, successHandler, closedHandler, loadedHandler) {
    var modal = new QuickModal();
    modal.openModal(selector, successHandler, closedHandler, loadedHandler);
    return modal;
}
