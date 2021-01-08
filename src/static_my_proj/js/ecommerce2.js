$(document).ready(function(){
    var contactForm = $(".contact-form");
    var contactFormMethod = contactForm.attr("method");
    var contactFormEndPoint = contactForm.attr("action");

    function displaySubmitting(submitBtn, defaultText, doSubmit){
        if (doSubmit) {
            submitBtn.add("disabled");
            submitBtn.html("<i class='fa fa-spin fa-spinner>></i> Sending...");
        } else {
            submitBtn.removeClass("disabled");
            submitBtn.html(defaultText);
        }
    }

    contactForm.submit(function(event){
        event.preventDefault();

        var contactFormSubmitBtn = contactForm.find("[type='submit']");
        var contactFormSubmitBtnTxt = contactFormSubmitBtn.text();
        var contactFormData = contactForm.serialize();
        var thisForm = $(this);

        displaySubmitting(contactFormSubmitBtn, "", true);

        $.ajax({
            url: contactFormEndPoint,
            method: contactFormMethod,
            data: contactFormData,
            success: function(data) {
                contactForm[0].reset();
                $.alert({
                    title: "success",
                    content: data.message,
                    theme: "modern",
                });

                setTimeout(function(){
                    displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnTxt, false);
                }, 500);
            },
            error: function(errorData){
                var jsonData = error.responseJSON;
                console.log("ERROR:" + jsonData);
                var msg = "";

                $.each(jsonData, function(key, value){
                    msg += key + ": " + value[0].message + "<br/>";
                });

                $.alert({
                    title: "Oops!",
                    content: msg,
                    theme: "modern",
                });

                setTimeout(function(){
                    displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnTxt, false);
                }, 500);
            }
        });
    });

    var searchForm = $(".search-form");
    var searchInput = searchForm.find("[name='q']");
    var typingTimer;
    var typingInterval = 500;
    var searchBtn = searchForm.find("[type='submit']");

    searchInput.keyup(function(event){
        clearTimeout(typingTimer);
        typingTimer = setTimeout(performSearch, typingInterval);
    });

    searchInput.keydown(function(event){
        clearTimeout(typingTimer);
    });

    function performSearch() {
        displaySearching();
        var query = searchInput.val();
        setTimeout(function(){
            window.location.href='/search/?q=' + query;
        }, 1000);
    }

})