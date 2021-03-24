$(document).ready(function () {
    var currentDate = moment();
    var dateString = currentDate.format("M/D/Y").toString();
    var dateField = $("#date1");

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
    var complaintCheckbox = $("#ongoing-complaint");
    complaintCheckbox.keypress(function(key) {
        if(key.which === 32) {
            $(this).trigger("click");
        }
    });

    // ToDo: Checking this also collapses the contact info section
    var anonCheckbox = $("#anonymous-complaint");
    anonCheckbox.keypress(function(key) {
        if(key.which === 32) {
            $(this).trigger("click");
        }
    });
    anonCheckbox.click(function() {
        var contactForm = $("#contact-info-collapsible");
        contactForm.toggleClass("d-none");
        if(contactForm.attr("aria-expanded") == "false") {
            contactForm.attr("aria-expanded", "true");
        }
        else {contactForm.attr("aria-expanded", "false");}
    });

    return false;
});