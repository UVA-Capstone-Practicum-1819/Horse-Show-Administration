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
            $("#errorBody").load(data);
        }
    });
};

/* the data will be the row html of the new rider row */
function addRider(data) {
    var riderTable = $("#riderTable")
    riderTable.append(data);
    riderTable.find(".delete-rider").on('click', deleteRider);
    riderTable.find(".edit-rider").on('click', change_url);
    $("#addRiderModal").modal('hide');
};

/* the data will be the combined rider row html with the location of the row within the table  */
function editRider(data) {
    var riderTable = $("#riderTable");
    var button
    riderTable.find("tr:eq() ")
    $("#addRiderModal").modal('hide');
};

/* when the edit button is pressed, change the form URL to the URL of the edit button */
function change_url(event) {
    event.preventDefault();
    $("#editRiderForm").attr('action') = $(this).attr('href');
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


/* form ajax handler */
function handle_form_ajax(form, successHandler) {
    $.ajax({
        type: "post",
        url: $(this).attr('href'),
        data: form.serialize(),
        success: successHandler,
        error: function (xhr, errmsg, error) {
            form.find("#errorBody").html(jQuery.parseJSON(xhr.responseText));

        }
    });
};

/* register the delete button to delete a rider */
$(".delete-rider").on('click', deleteRider);

/* register the edit buttons to edit the rider */
$(".edit-rider").on('click', change_url);

$("#add-form").on('click', function (event) {
    event.preventDefault();
    handle_form_ajax($(this), addRider);
});

$("#edit-form").on('click', function (event) {
    event.preventDefault();
    handle_form_ajax($(this), editRider);
});