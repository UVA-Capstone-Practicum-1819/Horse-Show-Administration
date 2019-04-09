/*  perform the AJAX request to add/edit rider with approp. form info */
/* $("#viewComboForm").on('submit', function (event) {
    event.preventDefault();
    viewForm = $(this);

    formData = viewForm.serialize();
    viewURL = $("#viewURL").data('url') + "/" + formData['combo_num']
    $.ajax({
        type: viewForm.attr('method'),
        url: formData['combo_num'],
        data: viewForm.serialize(),
        success: function (response) {
            $("#updateRiderModal").modal('hide');
            updateForm.data('op') == "add" ? addRider(response) : editRider(response);

        },
        error: function (response, status, xhr) {

            $("#formContainer").find("#errorBody").html(response.responseText);

        }
    });

}); */