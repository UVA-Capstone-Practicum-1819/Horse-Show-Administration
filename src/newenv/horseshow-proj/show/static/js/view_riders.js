

/* register the search box to filter through the riders */
$(document).ready(function () {
    $("#searchLastName").on("keyup", function () {
        var value = $(this).val().toLowerCase();
        $("#riderTable tr").filter(function () {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
});

/* register the add rider button to create a new rider and refresh the page */
$('#addRiderForm').on('submit', function (event) {
    event.preventDefault();

    $.ajax(
        {
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            data: $(this).serialize(),
            success: function (data) {
                $("#riderTable").append(data);
                $("#addRiderModal").modal('hide');
            },
            error: function (xhr, errmsg, error) {
                $("#errorBody").html(jQuery.parseJSON(xhr.responseText));

            }
        }
    );
});


/* register the delete button to delete a rider */

$(".delete-rider").on('click', function (event) {
    event.preventDefault();
    button = $(this)
    $.ajax(
        {
            url: $(this).attr('href'),
            method: "get",
            success: function (data) {

                button.parent().parent().remove();
            },
            error: function (data) {
                $("#errorBody").load(data);
            }
        }
    )
});










