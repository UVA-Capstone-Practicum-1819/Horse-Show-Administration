/* button listener for deleting a class from a combo */
$("#comboTable").on('click', '.deleteComboFromClassButton', function (event) {
    event.preventDefault();
    var deleteButton = $(this);
    $.ajax({
        url: deleteButton.data('url'),
        type: "get",
        success: function (response) {
            var data = response;
            deleteButton.parent().parent().remove();

        },
        error: function (response, status, xhr) {
            var data = response
            $("#messages").html(data['message']);
        }
    });
});