/* when modal pops up, send button information (url, operation (e.g. add, edit) to the modal */
$("#updateRiderModal").on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    var op = button.data('op');
    var url = button.data('url');
    var updateForm = $("#updateRiderForm");
    updateForm.attr('action', url);
    updateForm.data('op', op);
    if (op == "add") {
        $("#updateRiderButton").html("Add Rider");
        $("#riderModalTitle").html("Add Rider");

    } else {
        $("#updateRiderButton").html("Edit Rider");
        $("#riderModalTitle").html("Edit Rider");

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
$("#riderTable").on('click', '#deleteRider', deleteRider);

/* the data will be the row html of the new rider row */
function addRider(response) {
    var riderTable = $("#riderTable");
    riderTable.append(response);
    $.ajax({
        type: "get",
        url: "{% url 'get_rider_form' %}",
        success: function (response) {

        },
        error: function (response, status, xhr) {
            console.log(response.responseText)
        }

    })
};

/* the data will be the combined rider row html with the location of the row within the table  */
function editRider(response) {
    riderPk = response.find("tr").attr('id');
    $("#row-" + riderPk).replaceWith(data);
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



/* perform the AJAX request to add/edit rider with approp. form info */
$("#updateRiderForm").on('submit', function (event) {
    event.preventDefault();
    updateForm = $(this);
    $.ajax({
        type: updateForm.attr('method'),
        url: updateForm.attr('action'),
        data: updateForm.serialize(),
        success: function (response) {
            $("#updateRiderModal").modal('hide');
            updateForm.data('op') == "add" ? addRider(response) : editRider(response);

        },
        error: function (response, status, xhr) {
            updateForm.find("#errorBody").html(jQuery.parseJSON(response.responseText));

        }
    });

});