$("#addClassToComboButton").on('click', function () {
    var button = $(this);
    $.ajax({
        url: button.data('url'),
        type: "get",

    })
});