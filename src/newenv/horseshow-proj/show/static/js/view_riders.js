$("#updateRiderModal").on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    var op = button.data('op');
    var url = button.data('url');
    $("#updateRiderForm").attr('action') = url;
    if (op == "add") {
        $("#updateRiderButton").val("Add Rider");
        $("#riderModalTitle").val("Add Rider");
    } else {
        $("#updateRiderButton").val("Edit Rider");
        $("#riderModalTitle").val("Edit Rider");

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
    riderPk = data.find("tr").attr('id');
    $("#row-" + riderPk).replaceWith(data);
    $("#updateRiderModal").modal('hide');
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
        url: $(this).attr('action'),
        data: form.serialize(),
        success: successHandler,
        error: function (response, status, xhr) {
            form.find("#errorBody").html(jQuery.parseJSON(xhr.statusText));

        }
    });
};

/* register the delete button to delete a rider */
$(".delete-rider").on('click', deleteRider);

$("#updateRiderForm").on('submit', function (event) {
    event.preventDefault();
    updateForm = $(this);
    $.ajax({
        type: updateForm.attr('method'),
        url: updateForm.attr('action'),
        data: updateForm.serialize(),
        success: function (response) {

        },
        error: function (response, status, xhr) {
            form.find("#errorBody").html(jQuery.parseJSON(xhr.statusText));

        }
    });

});