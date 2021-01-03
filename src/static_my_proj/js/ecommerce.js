$(document).ready(function(){
  // Contact Form handler

  var contactForm = $(".contact-form");
  var contactFormMethod = contactForm.attr("method");
  var contactFormEndpoint = contactForm.attr("action");

  function displaySubmitting(submitBtn, defaultText, doSubmit){
      if (doSubmit) {
          submitBtn.add("disabled");
          submitBtn.html("<i class='fa fa-spin fa-spinner'></i> Sending...");
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
          method: contactFormMethod,
          url: contactFormEndpoint,
          data: contactFormData,
          success: function(data){
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
          error: function(error){
              console.log("ERROR:" + error.responseJSON);
              var jsonData = error.responseJSON;
              var msg = "";

              $.each(jsonData, function(key, value){ // key, value 만약 array라면 index, value임.
                  msg += key + ": " + value[0].message + "<br/>";
              });

              $.alert({
                  title: "Oops!",
                  content: msg,
                  theme: "modern",
              });

              setTimeout(function(){
                  displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnTxt, false);
              }, 500)
          }
      });

  });

  // Auto Search
  var searchForm = $(".search-form");
  // 아래는 input tag를 object를 가져온다. 즉 input name='q' 이런식으로 정의되어 있음.
  var searchInput = searchForm.find("[name='q']") // input name='q'
  var typingTimer;
  var typingInterval = 500; // 0.5 seconds
  var searchBtn = searchForm.find("[type='submit']");

  // 키를 눌렀다 해제할때 0.5초 이후 performSearch 수행함.
  // 만약 0.5초 이내에 다른 키를 typing한다면,
  // keydown순간 performSearch를 수행할 timer는 해제가 된다. 즉 performSearch를 수행하지 않고 stop한닫.
  // 그리고 다시 해제하는 순간 0.5초를 기다렸다가 수행함.
  // 이때 performSearch를 수행할때 searchInput 의 값으로 q를 설정하여 검색함.
  // 실제 검색시에는 1초 후 검색을 시작한다.
  searchInput.keyup(function(event){
      clearTimeout(typingTimer);
      typingTimer = setTimeout(performSearch, typingInterval);
  });

  searchInput.keydown(function(event){
      // key pressed
      clearTimeout(typingTimer);
  });

  function displaySearching(){
      searchBtn.addClass("disabled");
      searchBtn.html("<i class='fa fa-spin fa-spinner'></i> Searching...");
  }

  function performSearch(){
      displaySearching();
      var query = searchInput.val();
      setTimeout(function(){
          window.location.href='/search/?q=' + query
      }, 1000)
  }

  // Cart + add products
  var productForm = $(".form-product-ajax");

  productForm.submit(function(event){
      event.preventDefault();
      console.log("Form is not sending");
      var thisForm = $(this);
      //var actionEndPoint = thisForm.attr("action");
      var actionEndPoint = thisForm.attr("data-endpoint");
      var httpMethod = thisForm.attr("method");
      var formData = thisForm.serialize();

      $.ajax({
          url: actionEndPoint,
          method: httpMethod,
          data: formData,
          success: function (data){
              var submitSpan = thisForm.find(".submit-span");
              if (data.added) {
                  submitSpan.html("In Cart<button class=\"btn btn-link\">Remove?</button>");
              } else {
                  submitSpan.html("<button class=\"btn btn-success\">Add to Cart</button>");
              }
              var navbarCount = $(".navbar-cart-count");
              navbarCount.text(data.cartItemCount);
              var currentPath = window.location.href;
              console.log("-----");
              console.log(currentPath);
              console.log(currentPath.indexOf('cart'));
              console.log("-----");


              if (currentPath.indexOf("cart") != -1) {
                  refreshCart();
              }
          },
          error: function (errorData){
              console.log("error");
              console.log(errorData);
              $.alert({
                  title: "Opps!",
                  content: "An error occurred",
                  theme: "modern",
              });
          }
      });
  });

  function refreshCart(){
      console.log("in current cart");
      var cartTable = $(".cart-table");
      var cartBody = cartTable.find(".cart-body");
      //cartBody.html("<h1>Chaged</h1>");
      var productRows = cartBody.find(".cart-product");
      var currentUrl = window.location.href;

      var refreshCarUrl = '/api/cart/';
      var refreshMethod = 'GET';
      var data = {};

      $.ajax({
          url: refreshCarUrl,
          method: refreshMethod,
          data: data,
          success: function(data) {

              var hiddenCartItemRemoveForm = $(".cart-item-remove-form");

              if (data.products.length > 0) {
                  productRows.html(" ");
                  i = data.products.length;
                  $.each(data.products, function(index, value){
                      console.log(value);
                      var newCartItemRemove = hiddenCartItemRemoveForm.clone();
                      newCartItemRemove.css("display", "block")
                      //newCartItemRemove.remove("hidden-class")
                      newCartItemRemove.find(".cart-item-product-id").val(value.id)
                      cartBody.prepend("<tr><th scope='row'>" + i + "</th><td>"
                          + "<a href='" + value.url + "'>" + value.name + "</a>" + newCartItemRemove.html() + "</td><td>" + value.price + "</td></tr>");
                      i--;
                  })
                  cartBody.find(".cart-subtotal").text(data.subtotal);
                  cartBody.find(".cart-total").text(data.total);
              } else {
                  window.location.href = currentUrl;
              }
          },
          error: function(errorData) {
              console.log("error");
              console.log(errorData);
              $.alert({
                  title: "Opps!",
                  content: "An error occurred",
                  theme: "modern",
              });
          }
      })

  }
});
