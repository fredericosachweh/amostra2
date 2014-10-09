/*
 * CONTRACTS AND KLASSES MANAGEMENT
 */

function ContractManagement() {
    this.contractsContainer = $('.contract-list');

    var my = this;

    $('.contract-list').on('click', '[data-action=klass-create]', function(e) {
        my.showForm(this, e, my.klassCreateDone, my.klassCreateClosed, my.klassLoaded);
    });
    $('.contract-list').on('click', '[data-action=klass-update]', function(e) {
        my.showForm(this, e, my.klassUpdateDone, my.klassUpdateClosed, my.klassLoaded);
    });
    $('.contract-list').on('click', '[data-action=klass-delete]', function(e) {
        my.showForm(this, e, my.klassDeleteDone, my.klassDeleteClosed);
    });

}

ContractManagement.prototype = new AjaxHandler();
ContractManagement.prototype.constructor = ContractManagement;

ContractManagement.prototype.klassLoaded = function() {
    $('[data-datepicker]').datepicker();
};

ContractManagement.prototype.klassCreateDone = function(data) {
    this.createData = data;
    this.modal.foundation('reveal', 'close');
};

ContractManagement.prototype.klassCreateClosed = function(w) {
    /*
     * Appends the just created class to the contract's class list. If the
     * client list is hidden, open it by clicking on the trigger.
     */

    if(this.createData == null || typeof(this.createData) == 'undefined')
        return

    var wrapper = $(w).parents('.module');
    var container = wrapper.find('tbody');
    var empty = container.find('tr.empty');
    if (empty.length == 1) {
        empty.replaceWith(this.createData);
    } else {
        $(this.createData).hide().appendTo(container).fadeIn('fast');
    }

    // forces a click on the slider trigger
    var accordionTrigger = wrapper.find('[data-section-title]');
    if (container.is(':hidden'))
        accordionTrigger.click();

    var counter = accordionTrigger.find('span');
    counter.text(parseInt(counter.text()) + 1);

    wrapper.find('[data-dropdown]').click();  // closes the dropdown trigger

    this.createData = null;
}

ContractManagement.prototype.klassUpdateDone = function(data) {
    this.updateData = data;
    this.modal.foundation('reveal', 'close');
};

ContractManagement.prototype.klassUpdateClosed = function(w) {
    /*
     * Replaces the old DOM instance with the updated data got through ajax.
     */
    if(this.updateData == null || typeof(this.updateData) == 'undefined')
        return

    var wrapper = $(w).parents('tr');
    wrapper.replaceWith(this.updateData);
    this.updateData = null;
};

ContractManagement.prototype.klassDeleteDone = function(data) {
    this.wasRemoved = true;
    this.modal.foundation('reveal', 'close');
}

ContractManagement.prototype.klassDeleteClosed = function(w) {
    /*
     * Hides and delete the just remove class.
     */
    if(this.wasRemoved == false || typeof(this.wasRemoved) == 'undefined')
        return;

    var container = $(w).parents('tr');
    container.fadeOut('fast', function() { $(this).remove(); });
    this.wasRemoved = false;

    var wrapper = $(w).parents('.module');
    var counter = wrapper.find('[data-section-title] span');
    counter.text(parseInt(counter.text()) - 1);
}

/*
 * TEACHER MANAGEMENT
 */

function TeacherManagement() {
    this.teachersContainer = $('.teachers-list');
    this.wasRemoved = false;
    this.removeReturnedData = null;

    var my = this;
    $('body').on('click', '[data-action=teacher-create]', function(e) {
        my.showForm(this, e, my.teacherCreateDone);
    });
    $('.teachers-list').on('click', '[data-action=teacher-update]', function(e) {
        my.showForm(this, e, my.teacherUpdateDone);
    });
    $('.teachers-list').on('click', '[data-action=teacher-delete]', function(e) {
        my.showForm(this, e, my.teacherDeleteDone, my.teacherDeleteClosed);
    });
}

TeacherManagement.prototype = new AjaxHandler();
TeacherManagement.prototype.constructor = TeacherManagement;

TeacherManagement.prototype.teacherCreateDone = function(data) {
    // If there is no contract already, removes the empty message before
    // attach the contract
    var empty = this.teachersContainer.find('tr.empty');
    if(empty.length == 1) {
        empty.replaceWith(data);
    } else {
        $(data).hide().appendTo(this.teachersContainer.find('tbody')).fadeIn('fast');
    }

    this.modal.foundation('reveal', 'close');
};

TeacherManagement.prototype.teacherUpdateDone = function(data) {
    // The user cannot change anything but the companies the teacher is
    // attached to, this way, there is no need to update the html
    // representation of the teacher, we can just close the modal
    this.modal.foundation('reveal', 'close');
};

TeacherManagement.prototype.teacherDeleteDone = function(data) {
    this.wasRemoved = true;
    this.removeReturnedData = data;
    this.modal.foundation('reveal', 'close');
};

TeacherManagement.prototype.teacherDeleteClosed = function(w) {
    if (this.wasRemoved) {
        var tr = $(w).parents('tr');
        var tbody = tr.parent();
        var returnedData = this.removeReturnedData;
        tr.fadeOut('fast', function() {
            $(this).remove();

            // when remove all teachers, the blank messages comes from the ajax output
            if(tbody.find('tr').length == 0) {
                $(returnedData).hide().appendTo(tbody).fadeIn('fast');
            }
        });
    }

    // resets container vars
    this.wasRemoved = false;
    this.removeReturnedData = null;
};


/*
 * Calls and events binding.
 */

$(document).ready(function() {
    var c = new ContractManagement();
    var t = new TeacherManagement();
});
