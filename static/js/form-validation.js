// Wait for the DOM to be ready
$(function() {
    // Initialize form validation on the registration form.
    // It has the name attribute "registration"
    $("form[name='registration']").validate({
      // Specify validation rules
      rules: {
        // The key name on the left side is the name attribute
        // of an input field. Validation rules are defined
        // on the right side
        email: {
          required: true,
          // Specify that email should be validated
          // by the built-in "email" rule
          email: true
        },
        password: {
          required: true,
          minlength: 8
        },
        confirm_password: {
            required: true,
            minlength: 8,
            equalTo: "#password"
        },
        // checkbox : "required",

      },
      // Specify validation error messages
      messages: {
        password: {
          required: "Please provide a password",
          minlength: "Your password must be at least 8 characters long",
        },
        confirm_password: {
            required: "Please provide a password",
            equalTo: "Please enter the same password as above"
        },
          
        email: "Please enter a valid email address", 
        
        // checkbox : "Accept the terms"
      },
      // Make sure the form is submitted to the destination defined
      // in the "action" attribute of the form when valid
      submitHandler: function(form) {
        form.submit();
      }
    });
  });