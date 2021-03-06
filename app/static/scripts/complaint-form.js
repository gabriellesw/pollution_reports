$(document).ready(function () {
    let currentDate = moment();
    let dateString = currentDate.format("MM/DD/Y").toString();
    let dateField = $("#date1");

    // Set date field to today's date
    dateField.val(dateString);

    // Initialize datepicker
    dateField.datepicker({
        weekDayFormat: "narrow",
        markup: "bootstrap4",
        inputFormat: "MM/dd/y",
        outputFormat: "MM/dd/y",
        max: dateString,
    })

    // Set values in timepicker to current time
    let hours = $("#hours");
    let minutes = $("#minutes");
    let ampm = $("#ampm");
    hours.val(currentDate.format("h"));
    minutes.val(currentDate.format("m"));
    ampm.val(currentDate.format("A"));

    // Auto-set hidden field with full datetime for 3rd-party form
    let fullDate = $("#full_date")
    fullDate.val(dateField.val()+" "+hours.val()+":"+minutes.val()+" "+ampm.val());

    // Update this hidden field on subsequent manual changes to time
    hours.add(minutes).add(ampm).change(function () {
        fullDate.val(dateField.val()+" "+hours.val()+":"+minutes.val()+" "+ampm.val());
    });

    // Make checkbox buttons toggle-able with spacebar
    let refineryCheckbox = $("#refinery");
    refineryCheckbox.keypress(function(key) {
        if(key.which === 32) {
            $(this).trigger("click");
        }
    });
    let refineryCheckDescription = $("#is-refinery");
    refineryCheckbox.click(function() {
        if($(this).prop("checked") === true) {
            refineryCheckDescription.html('<i class="fas fa-check" aria-hidden="true"></i> Polluter is a Refinery');
        }
        else {
            refineryCheckDescription.text("Polluter is a Refinery");
        }
    })


    let complaintCheckbox = $("#ongoing-complaint");
    complaintCheckbox.keypress(function(key) {
        if(key.which === 32) {
            $(this).trigger("click");
        }
    });
    let complaintCheckDescription = $("#is-it-ongoing");
    complaintCheckbox.click(function() {
        if($(this).prop("checked") === true) {
            complaintCheckDescription.html('<i class="fas fa-check" aria-hidden="true"></i> Still Ongoing');
        }
        else {
            complaintCheckDescription.text("Still Ongoing");
        }
    })

    let phoneNumber = $("#phone");
    phoneNumber.inputmask("(999) 999-9999")

    let landlineCheckbox = $("#landline-button");
    landlineCheckbox.keypress(function (key) {
       if(key.which === 32) {
           $(this).trigger("click");
       }
    });

    let landLineDescription = $("#is-landline");
    landlineCheckbox.click(function() {
        if($(this).prop("checked") === true) {
            landLineDescription.html('<i class="fas fa-check" aria-hidden="true"></i> My Phone is a Landline');
        }
        else {
            landLineDescription.text(" My Phone is a Landline");
        }
    });

    // Make Anonymous complaint checkbox button toggle confirmation Modal
    let anonCheckbox = $("#anonymous-complaint");
    anonCheckbox.keypress(function(key) {
        if(key.which === 32) {
            $(this).trigger("click");
        }
    });
    let confirmAnonModal = $("#confirm-anon-modal");
    anonCheckbox.click(function() {
        if($(this).prop("checked") === true) {
            confirmAnonModal.modal();
        }
    });

    let privacyPolicy = $("#privacy-policy-button");
    privacyPolicy.keypress(function(key) {
        if(key.which === 32) {
            $(this).trigger("click");
        }
    });

    let privacyPolicyOK = $("#privacy-policy-ok");
    let ppRequired = $("#pp-required-modal");
    privacyPolicy.click(function() {
        if($(this).prop("checked") === true) {
            privacyPolicyOK.html('<i class="fas fa-check" aria-hidden="true"></i> I Accept the ');
        }
        else {
            privacyPolicyOK.text('I Accept the ');
            ppRequired.modal();
        }
    });

    let privacyPolicyLink = $("#privacy-policy-link-button");
    privacyPolicyLink.keypress(function (key) {
        if(key.which === 32 || key.which ===13) {
            $(this).trigger("click");
        }
    });
    privacyPolicyLink.click(function () {
        $("#privacy-policy-modal").modal();
    });

    // Make "Go Back" & "submit" buttons clickable w/spacebar & enter
    let cancelAnonymousReport = $("#cancel-anonymous-report")
    let submitAnonymousReport = $("#submit-anonymous-report")
    let buttons = [cancelAnonymousReport, submitAnonymousReport];
    for(i = 0; i < 2; i++) {
         buttons[i].keypress(function (key) {
             if(key.which === 32 || key.which === 13) {
                 $(this).trigger("click");
             }
         });
    }

    // Dismissing modal triggers reset of "anonymous" button
    confirmAnonModal.on("hide.bs.modal", function() {
        anonCheckbox.trigger("click");
    });

    ppRequired.on("hide.bs.modal", function() {
        privacyPolicy.trigger("click");
    });

    let submitSuccess = $("#complaint-submitted-modal");
    submitSuccess.on("hide.bs.modal", function () {
        $("#ok-report-submitted-dismissed")[0].click();
    })

    let submitFailed = $("#complaint-error-modal");
    submitFailed.on("hide.bs.modal", function () {
        $("#ok-report-failed-dismissed")[0].click();
    })

    // Submitting anonymously dismisses modal first to prevent unscrollable captcha
    let submit = $("#submit-report")
    submitAnonymousReport.click(function () {
        confirmAnonModal.modal("hide");
        anonCheckbox.prop("checked", true);
        $("#email, #confirm-email, #first-name, #last-name, #address, #lat, #lng, #street_number, #route, #locality, #administrative_area_level_1, #administrative_area_level_2, #postal_code").add(phoneNumber).val("");
        submit.trigger("click");
    });

    // Remove validation error feedback immediately when user goes to correct
    $(".is-invalid").each(function () {
        $(this).focus(function () {
            $(this).removeClass("is-invalid");
        });
    });

    return false;

});