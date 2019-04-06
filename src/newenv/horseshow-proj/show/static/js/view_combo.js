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

function addClass(data) {
    var class_num = data['class_num'];
    var class_name = data['class_name'];
    var div_name = data['div_name'];
    var delete_url = data['delete_url'];
    var combo_bill = data['combo_bill'];



}

/* button listener for adding a class to the combo */
$("#addClassToComboForm").on('submit', function (event) {
    event.preventDefault();
    addClassForm = $(this);
    $.ajax({
        url: addClassForm.attr('action'),
        type: addClassForm.attr('method'),
        data: addClassForm.serialize(),
        success: function (response) {

            var data = response.responseJSON;
            var participation = data['participation'];

            $("#classTable").append(data['template']);
            $("#classNumField").html("");
            $("#classNumHelp").html("");
            $("#billCell").html(data['combo_bill']);

        },
        error: function (response, status, xhr) {

            var data = response.responseJSON
            $("#messages").html(data['message']);
        }
    })
});

/* button listener for deleting a class from a combo */
$("#classTable").on('click', '.deleteClassFromComboButton', function (event) {
    event.preventDefault();
    var deleteButton = $(this);
    console.log(deleteButton.data('url'));
    $.ajax({
        url: deleteButton.data('url'),
        type: "get",
        success: function (response) {
            var data = response.responseJSON;
            deleteButton.parent().parent().remove();
            $("#billCell").html(data['combo_bill']);
        },
        error: function (response, status, xhr) {
            var data = response.responseJSON;
            $("#messages").html(data['message']);
        }
    });
});