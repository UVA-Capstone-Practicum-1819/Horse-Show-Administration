/* when modal pops up, send button information (url, operation (e.g. add, edit) to the modal */
$("#updateHorseModal").on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    var op = button.data('op');
    var url = button.data('url');

    var formContainer = $("#formContainer");
    var updateHorseForm = $("#updateHorseForm");
    var updateHorseButton = $("#updateHorseButton");
    var horseModalTitle = $("#horseModalTitle");
    form_url = $("#formURL").data('url');

    if (op == "add") {

        horseModalTitle.html("Add Horse");

        $.ajax({
            type: "get",
            url: form_url,
            success: function (response) {
                formContainer.html(response);
                updateHorseForm.attr('action', url);
                updateHorseForm.data('op', op);
                updateHorseButton.html("Add Horse");
            },
            error: function (response, status, xhr) {
                console.log(response.responseText);
            }

        });

    } else {
        horseModalTitle.html("Edit Horse");

        var horsePk = button.data('horsepk');
        $.ajax({
            type: "get",
            url: form_url + "/" + horsePk,
            success: function (response) {
                formContainer.html(response);
                updateHorseForm.attr('action', url);
                updateHorseForm.data('op', op);
                updateHorseButton.html("Edit Horse");
            },
            error: function (response, status, xhr) {
                console.log(response.responseText);
            }

        });
    }

});

/* deletes a horse and also the horse row in which the button was located */
function deleteHorse(event) {
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

/* register the delete button on every delete button in the horse table to delete a horse */
$("#horseTable").on('click', '.deleteHorse', deleteHorse);

/* the data will be the row html of the new horse row */
function addHorse(response) {
    var horseTable = $("#horseTable");
    horseTable.append(response);
};

/* the data will be the combined horse row html with the location of the row within the table  */
function editHorse(response) {
    var horseRow = $($.parseHTML(response));
    var rowPk = horseRow.attr('id');
    $("#" + rowPk).replaceWith(response);
};

/* register the search box to filter through the horses */
$(document).ready(function () {
    $("#search").on("keyup", function () {
        var value = $(this).val().toLowerCase();
        $("#horseTable tr").filter(function () {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
});



/*  perform the AJAX request to add/edit horse with approp. form info */
$("#updateHorseForm").on('submit', function (event) {
    event.preventDefault();
    updateForm = $(this);

    $.ajax({
        type: updateForm.attr('method'),
        url: updateForm.attr('action'),
        data: updateForm.serialize(),
        success: function (response) {
            $("#updateHorseModal").modal('hide');
            updateForm.data('op') == "add" ? addHorse(response) : editHorse(response);

        },
        error: function (response, status, xhr) {
            console.log(response);
            $("#formContainer").find("#errorBody").html(response.responseText);

        }
    });

});