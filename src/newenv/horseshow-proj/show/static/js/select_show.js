$(".viewShowLink").on('click', function (event) {
    event.preventDefault();
    var button = $(this);
    $.ajax({
        url: button.attr('href'),
        type: "get",
        success: function (response) {
            console.log("view show success");
        },
        error: function (response, status, xhr) {
            console.log("view show error");
        }
    });
});