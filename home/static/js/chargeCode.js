jQuery(document).ready(function ($) {
    var chargeCodeModal = document.getElementById("chargeCodeModal");
    var chargeCodeForm = document.getElementById("chargeCodeForm");
    var chargeCodeClose = document.getElementById("chargeCodeModalClose");

    chargeCodeClose.onclick = function () {
        chargeCodeModal.style.display = "none";
    }

    window.onclick = function (event) {
        if (event.target == chargeCodeModal) {
            chargeCodeModal.style.display = "none";
        }
    }
    
    $('#create-chargecode').click(function () {
        console.log(("Create Charge Code Modal..."))
        chargeCodeModal.style.display = "block";
    });

    $('#active-chargecodes .fa-cogs').click(function (e) {
        console.log(("Edit Charge Code..."))
        var item = $(this),
            target = $(e.target);
        var id_code = target.attr("id_code");

        $.ajax({
            type: 'GET',
            cache: true,
            traditional: true,
            url: 'get-chargecode',
            async: false,
            data: { id_code: id_code },
            success: function (data) {
                console.log(data);
                $('#id_name').val(data["response"]["name"]);
                $('#id_code').val(data["response"]["code"]);
                $('#id_hours_allocated').val(data["response"]["hours_allocated"]);
                $('#id_hours_spent').val(data["response"]["hours_spent"]);
                $('#id_start').val(data["response"]["start_date"]);
                $('#id_end').val(data["response"]["end_date"]);
                $('#id_tax_code').val(data["response"]["tax_code"]);
                $('#id_personal_list').val(data["response"]["personal_list"]);
                $('#id_color').val(data["response"]["color"]);
                $('#id_name').val(data["response"]["name"]);
                $('#id_chargecode').val(id_code)
                
                chargeCodeModal.style.display = "block";
            }
        });

    });

    $('#active-chargecodes .fa-trash').click(function (e) {
        console.log(("Delete Charge Code..."))
        var item = $(this),
            target = $(e.target);
        var id_code = target.attr("id_code");

        var _temp = confirm("Are you sure you want to remove this charge code?");
        
        if (_temp) {
            $.ajax({
                type: 'GET',
                cache: true,
                traditional: true,
                url: 'delete-chargecode',
                data: { id_code: id_code },
                success: function (data) {
                    console.log('Success: Charge Code...');
                    location.reload();
                },
                error: function (data) {
                    alert("Failed: Charge Code Delete... " + data);
                },
            });
        }
        
    });
    
});

function getChargeCode(id, edit=false) {
    $.ajax({
        type: 'GET',
        cache: true,
        traditional: true,
        url: 'get-chargecode',
        data: { id_code: id },
        success: function (data) {
            return data;
        }
    });
}
