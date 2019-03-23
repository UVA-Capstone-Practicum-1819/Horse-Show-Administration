

/* register the search box to filter through the riders */
$(document).ready(function () {
    $("#searchLastName").on("keyup", function () {
        var value = $(this).val().toLowerCase();
        $("#riderTable tr").filter(function () {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
});



/* update the table with new riders */
function refreshTable(riders) {
    var rows = $("#riderTable > tr:gt(0)");
    for (let i = 0; i < riders.length; ++i) {
        var rider = riders[i];
        var row = rows.find("");
        console.log("Print all cells:");
        console.log(rows.find('td#riderLastName'));
        /* row.find("#riderLastName").html = rider['last_name'];
        row.find("#riderFirstName").html = rider['first_name'];
        row.find("#riderEmail").html = rider['email'];
        row.find("#riderAddress").html = rider['address'];
        row.find("#riderCity").html = rider['city'];
        row.find("#riderZipCode").html = rider['zip_code'];
        row.find("#riderAdult").html = rider['adult'];
        row.find("#riderBirthDate").html = rider['birth_date'];
        row.find("#riderMemberVHSA").html = rider['memberVHSA'];
        row.find("#riderMember4H").html = rider['member_4H'];
        row.find("#riderCounty").html = rider['county']; */
    }

}


/* register the delete button to delete a rider */
/* $(document).ready(function () {
    $("riders[")
}); */

$(document).ready(function () {


    $(".deleteRider").on('click', function () {
        $.ajax(
            {
                url: $(this).attr('href'),
                method: "get",
                success: function (data) {
                    newRiders = jQuery.parseJSON(data)

                    refreshTable(newRiders);
                },
                error: function (data) {
                    $("#errorBody").load(data);
                }
            }
        )
    }

    )

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
                console.log(data);
                $("#riderTable").append(data);
                $("#addRiderModal").modal('hide');
            },
            error: function (xhr, errmsg, error) {
                $("#errorBody").html(jQuery.parseJSON(xhr.responseText));

            }
        }
    );
});




