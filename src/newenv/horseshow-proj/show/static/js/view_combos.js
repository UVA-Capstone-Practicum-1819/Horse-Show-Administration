/* when modal pops up, send button information (url, operation (e.g. add, edit) to the modal */
$("#updateComboModal").on('show.bs.modal', function (event) {
    /* grab relevant info */
    var button = $(event.relatedTarget);
    var op = button.data('op');
    var url = button.data('url');
    var formContainer = $("#formContainer");
    var updateComboForm = $("#updateComboForm");
    var updateComboButton = $("#updateComboButton");
    var comboModalTitle = $("#comboModalTitle");
    form_url = $("#formURL").data('url');

    /* if the form being loaded is an add form */
    if (op == "add") {

        comboModalTitle.html("Add Combo");

        $.ajax({
            type: "get",
            url: form_url,
            success: function (response) {
                formContainer.html(response);
                updateComboForm.attr('action', url);
                updateComboForm.data('op', op);
                updateComboButton.html("Add Combo");

            },
            error: function (response, status, xhr) {
                console.log(response.responseText);
            }

        });

        /* if the form that is loaded is an edit form */
    } else {
        comboModalTitle.html("Edit Combo");

        var comboPk = button.data('combopk');
        $.ajax({
            type: "get",
            url: form_url + "/" + comboPk,
            success: function (response) {
                formContainer.html(response);
                updateComboForm.attr('action', url);
                updateComboForm.data('op', op);
                updateComboButton.html("Edit Combo");

            },
            error: function (response, status, xhr) {
                console.log(response.responseText);
            }

        });
    }

});

/* deletes a combo and also the combo row in which the button was located */
function deleteCombo(event) {
    event.preventDefault();
    button = $(this);
    $.ajax({
        url: $(this).attr('href'),
        method: "get",
        success: function () {
            button.parent().parent().remove();
        },
        error: function (data) {
            $("#errorBody").html(data);
        }
    });
};

/* register the delete button on every delete button in the combo table to delete a combo */
$("#comboTable").on('click', '.deleteCombo', deleteCombo);

/* the data will be the row html of the new combo row */
function addCombo(response) {
    var comboTable = $("#comboTable");
    comboTable.append(response);
};

/* the data will be the combined combo row html with the location of the row within the table  */
function editCombo(response) {
    var comboRow = $($.parseHTML(response));
    var rowPk = comboRow.attr('id');
    $("#" + rowPk).replaceWith(response);
};

/* register the search box to filter through the combos */
$(document).ready(function () {
    $("#search").on("keyup", function () {
        var value = $(this).val().toLowerCase();
        $("#comboTable tr").filter(function () {
            $(this).toggle($(this).find(".numLink").text().toLowerCase().indexOf(value) > -1)
        });
    });
});



/*  perform the AJAX request to add/edit combo with approp. form info */
$("#updateComboForm").on('submit', function (event) {
    event.preventDefault();
    updateForm = $(this);

    $.ajax({
        type: updateForm.attr('method'),
        url: updateForm.attr('action'),
        data: updateForm.serialize(),
        success: function (response) {
            $("#updateComboModal").modal('hide');
            updateForm.data('op') == "add" ? addCombo(response) : editCombo(response);

        },
        error: function (response, status, xhr) {
            console.log(response);
            $("#formContainer").find("#errorBody").html(response.responseText);

        }
    });

});