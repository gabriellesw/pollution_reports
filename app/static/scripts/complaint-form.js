$(document).ready(function () {
    let currentDate = moment();
    let dateString = currentDate.format("M/D/Y").toString();
    let dateField = $("#date1");

    // Set date field to today's date
    dateField.val(dateString);

    // Initialize datepicker
    dateField.datepicker({
        weekDayFormat: "narrow",
        markup: "bootstrap4",
        inputFormat: "M/d/y",
        max: dateString,
    })

    // Set values in timepicker to current time
    $("#hours").val(currentDate.format("h"));
    $("#minutes").val(currentDate.format("m"));
    $("#ampm").val(currentDate.format("a"));

    // Make checkbox buttons toggle-able with spacebar
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
    anonCheckbox.click(function() {
        if($(this).prop("checked") === true) {
            $("#confirm-anon-modal").modal();
        }
    });

    let privacyPolicy = $("#privacy-policy-button");
    privacyPolicy.keypress(function(key) {
        if(key.which === 32) {
            $(this).trigger("click");
        }
    });

    let privacyPolicyOK = $("#privacy-policy-ok");
    privacyPolicy.click(function() {
        if($(this).prop("checked") === true) {
            privacyPolicyOK.html('<i class="fas fa-check" aria-hidden="true"></i> I Accept the ');
        }
        else {
            privacyPolicyOK.text('I Accept the ');
            // ToDo: switch placeholder for PP required modal
            $("#confirm-anon-modal").modal();
        }
    });

    let privacyPolicyLink = $("#privacy-policy-link-button");
    privacyPolicyLink.keypress(function (key) {
        if(key.which === 32 || key.which ===13) {
            $(this).trigger("click");
        }
    });
    privacyPolicyLink.click(function () {
        // ToDo: switch placeholder for PP modal
        $("#privacy-policy-modal").modal();
    });

    // Make "Go Back" & "submit" buttons clickable w/spacebar & enter
    let buttons = [$("#cancel-anonymous-report"), $("#submit-anonymous-report")];
    for(i = 0; i < 2; i++) {
         buttons[i].keypress(function (key) {
             if(key.which === 32 || key.which === 13) {
                 $(this).trigger("click");
             }
         });
    }

    // Dismissing modal triggers reset of "anonymous" button
    let modal = $("#confirm-anon-modal");
    modal.on("hide.bs.modal", function() {
        anonCheckbox.trigger("click");
        // ToDo: move to PP required modal
        privacyPolicy.trigger("click");
    });

    // ToDo: Submit-anonymous submits entire form (might need to bypass validation)

    return false;
});