/* when modal pops up, send button information (url, operation (e.g. add, edit) to the modal */
$("#updateRiderModal").on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    var op = button.data('op');
    var url = button.data('url');
    var updateRiderButton = $("#updateRiderButton");
    updateRiderButton.data('url', url);
    updateRiderButton.data('op', op);
    form_url = $("#formURL").data('url');

    if (op == "add") {
        $("#updateRiderButton").html("Add Rider");
        $("#riderModalTitle").html("Add Rider");

        $.ajax({
            type: "get",
            url: form_url,
            success: function (response) {
                $("#updateRiderForm").replaceWith(response);
                $("#updateRiderButton").html("Add Rider");
            },
            error: function (response, status, xhr) {
                console.log(response.responseText);
            }

        });

    } else {
        $("#riderModalTitle").html("Edit Rider");
        $("#riderModalTitle").html("Edit Rider");
        var riderPk = button.data('riderpk');
        $.ajax({
            type: "get",
            url: form_url + "/" + riderPk,
            success: function (response) {
                $("#updateRiderForm").replaceWith(response);
                $("#updateRiderButton").html("Edit Rider");
            },
            error: function (response, status, xhr) {
                console.log(response.responseText);
            }

        });
    }

});

/* deletes a rider and also the rider row in which the button was located */
function deleteRider(event) {
    event.preventDefault();
    button = $(this)
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

/* register the delete button on every delete button in the rider table to delete a rider */
$("#riderTable").on('click', '.deleteRider', deleteRider);

/* the data will be the row html of the new rider row */
function addRider(response) {
    var riderTable = $("#riderTable");
    riderTable.append(response);
};

/* the data will be the combined rider row html with the location of the row within the table  */
function editRider(response) {
    var riderRow = $($.parseHTML(response));
    var rowPk = riderRow.attr('id');
    console.log("rowPk: " + rowPk);
    $("#" + rowPk).replaceWith(response);
};

/* register the search box to filter through the riders */
$(document).ready(function () {
    $("#searchLastName").on("keyup", function () {
        var value = $(this).val().toLowerCase();
        $("#riderTable tr").filter(function () {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
});



/*  perform the AJAX request to add/edit rider with approp. form info */
$("#updateRiderButton").on('click', function (event) {
    event.preventDefault();
    updateButton = $(this);
    updateForm = $("#updateRiderForm");
    $.ajax({
        type: "post",
        url: updateButton.data('url'),
        data: updateForm.serialize(),
        success: function (response) {
            $("#updateRiderModal").modal('hide');
            updateButton.data('op') == "add" ? addRider(response) : editRider(response);

        },
        error: function (response, status, xhr) {
            updateForm.find("#errorBody").html(jQuery.parseJSON(response.responseText));

        }
    });

});