/* when modal pops up, send button information (url) to the modal */
$("#updateComboModal").on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    var url = button.data('url');

    var formContainer = $("#formContainer");
    var updateComboForm = $("#updateComboForm");
    var updateComboButton = $("#updateComboButton");
    var comboModalTitle = $("#comboModalTitle");
    form_url = $("#formURL").data('url');


    comboModalTitle.html("Edit Combo");

    var comboPk = button.data('combopk');
    $.ajax({
        type: "get",
        url: form_url + "/" + comboPk,
        success: function (response) {
            formContainer.html(response);
            updateComboForm.attr('action', url);
            updateComboButton.html("Edit Combo");
        },
        error: function (response, status, xhr) {
            console.log(response.responseText);
        }

    });


});


/* button listener for adding a class to the combo */
$("#addClassToComboForm").on('submit', function (event) {
    event.preventDefault();
    addClassForm = $(this);
    $.ajax({
        url: addClassForm.data('action'),
        type: "post",
        data: addClassForm.serialize(),
        success: function (response) {
            $("#riderTable").append(response['template']);
            $("#classNumField").html("");
            $("#classNumHelp").html("");
            $("#billCell").html(response['combo_bill']);
        },
        error: function (response, status, xhr) {
            $("#classNumHelp").html(response['responseText']);
        }
    });
});

/* button listener for deleting a class from a combo */
$("#classTable").on('click', '.deleteClassFromCombo', function (event) {
    event.preventDefault();
    var deleteButton = $(this);
    $.ajax({
        url: deleteButton.data('url'),
        type: "get",
        success: function (response) {
            deleteButton.parent().parent().remove();
            $("#billCell").html(response['combo_bill']);
        },
        error: function (response, status, xhr) {

        }
    });
});