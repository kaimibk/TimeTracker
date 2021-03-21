jQuery(document).ready(function ($) {
    var taskAuthorizationModal = document.getElementById("taskAuthorizationModal");
    var taskAuthorizationForm = document.getElementById("taskAuthorizationForm");
    var taskAuthorizationClose = document.getElementById("taskAuthorizationModalClose");

    taskAuthorizationClose.onclick = function () {
        taskAuthorizationModal.style.display = "none";
    }

    window.onclick = function (event) {
        if (event.target == taskAuthorizationModal) {
            taskAuthorizationModal.style.display = "none";
        }
    }

    $('#create-taskauthorization').click(function () {
        console.log(("Create Charge Code Modal..."))
        taskAuthorizationModal.style.display = "block";
    });

    $('#active-taskauthorizations .fa-cogs').click(function (e) {
        console.log(("Edit Charge Code..."))
        var item = $(this),
            target = $(e.target);
        var id_code = target.attr("ta_ccId");

        $.ajax({
            type: 'GET',
            cache: true,
            traditional: true,
            url: 'get-taskauthorization',
            async: false,
            data: { id_code: id_code },
            success: function (data) {
                console.log('HAAAAAAAAAAAAAAAAAAAAA');
                console.log(data);
                $('#ta_name').val(data["response"]["name"]);
                $('#ta_codeId').val(data["response"]["code"]);
                $('#ta_hours_allocated').val(data["response"]["hours_allocated"]);
                $('#ta_hours_spent').val(data["response"]["hours_spent"]);
                $('#ta_start_date').val(data["response"]["start_date"]);
                $('#ta_end_date').val(data["response"]["end_date"]);
                // $('#ta_tax_code').val(data["response"]["tax_code"]);
                // $('#ta_personal_list').val(data["response"]["personal_list"]);
                // $('#ta_color').val(data["response"]["color"]);
                $('#ta_file').val(data["response"]["ta_file"]);
                $('#id_ta').val(id_code)

                taskAuthorizationModal.style.display = "block";
            }
        });

    });

    $('#active-taskauthorizations .fa-trash').click(function (e) {
        console.log(("Delete Task Authorization..."))
        var item = $(this),
            target = $(e.target);
        var id_code = target.attr("id_code");

        var _temp = confirm("Are you sure you want to remove this task authorization?");

        if (_temp) {
            $.ajax({
                type: 'GET',
                cache: true,
                traditional: true,
                url: 'delete-taskauthorization',
                data: { id_code: id_code },
                success: function (data) {
                    console.log('Success: Task Authorization...');
                    location.reload();
                },
                error: function (data) {
                    alert("Failed: Task Authorization Delete... " + data);
                },
            });
        }

    });

});

function getTaskAuthorization(id, edit = false) {
    $.ajax({
        type: 'GET',
        cache: true,
        traditional: true,
        url: 'get-taskauthorization',
        data: { id_code: id },
        success: function (data) {
            return data;
        }
    });
}
