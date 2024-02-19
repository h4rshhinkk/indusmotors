function setCookie(name, value, days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

$(function () {
    'use strict'

    $('select.select:not(.offcanvas select)').select2({
        minimumResultsForSearch: '',
        placeholder: "Search",
        width: '100%',
        allowClear: true,
    });

    // $(".offcanvas select").select2({ dropdownParent: "#offcanvasFilter" });

    $('.niceselect').select2({
        minimumResultsForSearch: -1,
        placeholder: "Search",
        width: '100%',
    });

    $('.selectmultiple').select2({
        minimumResultsForSearch: '',
        placeholder: "Search",
        width: '100%'
    });

    $('.select2').on('click', () => {
        let selectField = document.querySelectorAll('.select2-search__field')
        selectField.forEach((element, index) => {
            element?.focus();
        })
    });

    $('input.dateinput').bootstrapdatepicker({
        format: "dd/mm/yyyy",
        viewMode: "date",
        multidate: false,
        multidateSeparator: "-",
        orientation: "bottom right",
        autoclose: true,
        todayHighlight: true
    });

    // $('input.datetimeinput').bootstrapdatepicker({
    //     format: "dd/mm/yyyy hh:ii",
    //     viewMode: "time",
    //     multidate: false,
    //     multidateSeparator: "-",
    //     orientation: "bottom right"
    // })

    // $('input.timeinput').bootstrapdatepicker({
    //     format: "hh:ii",
    //     viewMode: "time",
    //     multidate: false,
    //     multidateSeparator: "-",
    //     orientation: "bottom right"
    // })



    $('.theme-layout').on('click', () => {
        if (document.body.className.split(" ").indexOf("dark-mode") >= 0) {
            setCookie("mode", "dark-mode", 7);
        };
        if (document.body.className.split(" ").indexOf("light-mode") >= 0) {
            setCookie("mode", "light-mode", 7);
        };
    });

    var mode = getCookie("mode");
    $('body').removeClass('light-mode');
    $('body').removeClass('dark-mode');
    $('body').addClass(mode);

    $('.timeinput').timepicker({
        timeFormat: 'HH:mm',
        interval: 5,
        dynamic: true,
        dropdown: true,
        scrollbar: false
    });

    $(document).on("click", ".instant-action-button", function (e) {
        e.preventDefault();
        var key = $(this).attr("data-key");
        var url = $(this).attr("data-url");
        var title = $(this).attr("data-title");
        $.ajax({
            type: "GET",
            url: url,
            dataType: "json",
            data: { pk: key },
            success: function (data) {
                var status = data.status;
                var message = data.message;
                if (status == "success") {
                    title ? (title = title) : (title = "Success");
                    $(`[data-key="${key}"]`).html(
                        `<i class="bi bi-check-square-fill text-success"></i>`
                    );
                    $(`span#${key}`).html(message);
                } else {
                    title ? (title = title) : (title = "An Error Occurred");
                    alert(message);
                }
            },
            error: function (data) {
                var title = "An error occurred";
                var message = "An error occurred. Please try again later.";
            },
        });
    });


    // add .row class to .form-horizontal and .col-md-3 to add its children with .mb-3 class
    $(".form-horizontal").each(function () {
        $(this).addClass("row");
        $(this).find(".mb-3").addClass("col-lg-3 col-md-4 col-sm-6 col-12");

        if ($(this).find("#div_id_customer_voice").length > 0) {
            $(this).find("#div_id_customer_voice").removeClass("col-lg-3 col-md-4 col-sm-6 col-12").addClass("col-lg-12 col-md-6 col-sm-6 col-12");
        }

        if ($(this).find("#div_id_d15_calling_remark").length > 0) {
            $(this).find("#div_id_d15_calling_remark").removeClass("col-lg-3 col-md-4 col-sm-6 col-12").addClass("col-lg-12 col-md-6 col-sm-6 col-12");
        }

        if ($(this).find("#div_id_is_chassis_blocked").length > 0) {
            $(this).find("#div_id_is_chassis_blocked").removeClass("mb-3 form-check col-lg-3 col-md-4 col-sm-6 col-12").addClass("mb-3 p-2 form-check col-lg-12 col-md-4 col-sm-6 col-12");
        }

    });

    $(".form-horizontal-col-six").each(function () {
        $(this).addClass("row");
        $(this).find(".mb-3").addClass("col-lg-6 col-md-4 col-sm-6 col-12");
        if ($(this).find("#div_id_customer_salutation").length > 0) {
            $(this).find("#div_id_customer_salutation").removeClass("col-lg-6 col-md-6 col-sm-6 col-12").addClass("col-lg-2 col-md-2 col-sm-6 col-6");
        }
        if ($(this).find("#div_id_customer_name").length > 0) {
            $(this).find("#div_id_customer_name").removeClass("col-lg-6 col-md-6 col-sm-6 col-12").addClass("col-lg-4 col-md-2 col-sm-6 col-6");
        }
        if ($(this).find("#div_id_guardian_salutation").length > 0) {
            $(this).find("#div_id_guardian_salutation").removeClass("col-lg-6 col-md-6 col-sm-6 col-12").addClass("col-lg-2 col-md-2 col-sm-6 col-6");
        }
        if ($(this).find("#div_id_guardian_name").length > 0) {
            $(this).find("#div_id_guardian_name").removeClass("col-lg-6 col-md-6 col-sm-6 col-12").addClass("col-lg-4 col-md-2 col-sm-6 col-6");
        }

        

    });


});
