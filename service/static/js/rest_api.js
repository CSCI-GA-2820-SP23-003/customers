$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#customer_id").val(res.id);
        $("#customer_firstname").val(res.first_name);
        $("#customer_lastname").val(res.last_name);
        $("#customer_email").val(res.email);
        $("#customer_password").val(res.password);
        $("#customer_street").val(res.addresses[0].street);
        $("#customer_city").val(res.addresses[0].city);
        $("#customer_state").val(res.addresses[0].state);
        $("#customer_country").val(res.addresses[0].country);
        $("#customer_pincode").val(res.addresses[0].pin_code);
        if (res.active == true) {
            $("#customer_active").val("true");
        } else {
            $("#customer_active").val("false");
        }
    }


    /// Clears all form fields
    function clear_form_data() {
        $("#customer_id").val("");
        $("#customer_firstname").val("");
        $("#customer_lastname").val("");
        $("#customer_email").val("");
        $("#customer_password").val("");
        $("#customer_street").val("");
        $("#customer_city").val("");
        $("#customer_state").val("");
        $("#customer_country").val("");
        $("#customer_pincode").val("");
        $("#customer_active").val("true");
    }

    function removeAllNotifications() {
        const fields = [
            "firstname",
            "lastname",
            "email",
            "password",
            "street",
            "city",
            "state",
            "country",
            "pincode",
        ];

        fields.forEach(function(field) {
            input = "#customer_"+field  
            removeFieldRequiredNotification(input)
        });
    }    

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // Function to regex check the format of the email
    function validateEmail($email) {
        let emailReg = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return emailReg.test($email);
    }

    function displayEmailFormatErrorNotification(){
        input = "#customer_email"
        $(input).closest(".form-group").addClass("has-error");
        $(input+"_err p").html("");
        $(input+"_err p").append("This doesn't appear to be a valid email address").show();
    }

    function displayFieldRequiredNotification(input){
        $(input).closest(".form-group").addClass("has-error");
        $(input+"_err p").html("");
        $(input+"_err p").text("Required field").show();
    }

    function removeFieldRequiredNotification(input){
        $(input).closest(".form-group").removeClass("has-error");
        $(input+"_err p").html("");
        $(input+"_err p").hide();
    }   
    
    function convertActiveDropdownToInt(active){
        if (active == "true")
            return 1
        else
            return 0
    }

    // ****************************************
    // Create a Customer
    // ****************************************

    $("#create-btn").click(function () {

        let first_name = $("#customer_firstname").val().trim();
        let last_name = $("#customer_lastname").val().trim();
        let email = $("#customer_email").val().trim();
        let password = $("#customer_password").val().trim();
        let street = $("#customer_street").val().trim();
        let city = $("#customer_city").val().trim();
        let state = $("#customer_state").val().trim();
        let country = $("#customer_country").val().trim();
        let pin_code = $("#customer_pincode").val().trim();
        let active = ($("#customer_active").val().toLowerCase() === 'true');

        let addr_data = {
            "street": street,
            "city": city,
            "state": state,
            "country": country,
            "pin_code": pin_code,
            "customer_id": 0

        };

        let to_pass = [addr_data];

        let cust_data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password,
            "active": active,
            "addresses": to_pass,
        };

        // Check for missing required data in form
        dataError = 0
        for (let i in cust_data) {
            input = "#customer_"+i
            if (!cust_data[i]) {
                displayFieldRequiredNotification(input)
                dataError++
            } else {
                removeFieldRequiredNotification(input)
            }
        }

        // Check the email is in the correct format
        if (email)
            if (!validateEmail(email)) {
                displayEmailFormatErrorNotification();
                dataError++;
            }

        // Stop the execution of the script if there are data errors
        if (dataError > 0) {
            $("#flash_message").html("Form Error(s)")
            return false
        }

        // Add active status to payload after user input validation
        cust_data.acc_active = convertActiveDropdownToInt(active);
        
        $("#flash_message").empty();
        
        // Send the form data to the API
        let ajax = $.ajax({
            type: "POST",
            url: "/customers",
            contentType: "application/json",
            data: JSON.stringify(cust_data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update a Customer
    // ****************************************

    $("#update-btn").click(function () {

        let customer_id = $("#customer_id").val();
        let first_name = $("#customer_firstname").val().trim();
        let last_name = $("#customer_lastname").val().trim();
        let email = $("#customer_email").val().trim();
        let password = $("#customer_password").val().trim();
        let street = $("#customer_street").val().trim();
        let city = $("#customer_city").val().trim();
        let state = $("#customer_state").val().trim();
        let country = $("#customer_country").val().trim();
        let pin_code = $("#customer_pincode").val().trim();
        let active = ($("#customer_active").val().toLowerCase() === 'true');
        
        let addr_data = {
            "street": street,
            "city": city,
            "state": state,
            "country": country,
            "pin_code": pin_code,
            "customer_id": 0

        };

        let to_pass = [addr_data];

        let cust_data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password,
            "active": active,
            "addresses": to_pass,
        };

        // Check for missing required data in form
        dataError = 0
        for (let i in cust_data) {
            input = "#customer_"+i
            if (!cust_data[i]) {
                displayFieldRequiredNotification(input)
                dataError++
            } else {
                removeFieldRequiredNotification(input)
            }
        }

        // Check the email is in the correct format
        if (email)
            if (!validateEmail(email)) {
                displayEmailFormatErrorNotification();
                dataError++;
            }
        
        // Stop the execution of the script if there are data errors
        if (dataError > 0) {
            $("#flash_message").html("Form Error(s)")
            return false
        }
        
        $("#flash_message").empty();
        
        // Add active status to payload after user input validation
        cust_data.acc_active = convertActiveDropdownToInt(active);

        let ajax = $.ajax({
                type: "PUT",
                url: `/customers/${customer_id}`,
                contentType: "application/json",
                data: JSON.stringify(cust_data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a Customer
    // ****************************************

    $("#retrieve-btn").click(function () {

        let customer_id = $("#customer_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/customers/${customer_id}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a Customer
    // ****************************************

    $("#delete-btn").click(function () {

        let customer_id = $("#customer_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/customers/${customer_id}`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Customer has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#customer_id").val("");
        $("#flash_message").empty();
        clear_form_data()
        removeAllNotifications()
    });

    // ****************************************
    // Search for a Customer
    // ****************************************

    $("#search-btn").click(function () {
        let first_name = $("#customer_firstname").val();
        let last_name = $("#customer_lastname").val();
        let email = $("#customer_email").val();
        let street = $("#customer_street").val();
        let city = $("#customer_city").val();
        let state = $("#customer_state").val();
        let country = $("#customer_country").val();
        let pin_code = $("#customer_pincode").val();
        let active = ($("#customer_active").val().toLowerCase() === 'true');
       
        let queryString = ""

        if (first_name){
            queryString += 'first_name=' + first_name
        }

        else if (last_name) {
            queryString += 'last_name=' + last_name
        }

        else if (email) {
            queryString += 'email=' + email
        }

        else if (street) {
            queryString += 'street=' + street
        }

        else if (city) {
            queryString += 'city=' + city
        }

        else if (state) {
            queryString += 'state=' + state
        }
        
        else if (country) {
            queryString += 'country=' + country
        }

        else if (pin_code) {
            queryString += 'pin_code=' + pin_code
        }
        
        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/customers?${queryString}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            $("#search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-1">Cust_ID</th>'
            table += '<th class="col-md-2">First Name</th>'
            table += '<th class="col-md-2">Last Name</th>'
            table += '<th class="col-md-2">Email</th>'
            table += '<th class="col-md-2">Password</th>'
            table += '<th class="col-md-2">Street</th>'
            table += '<th class="col-md-2">City</th>'
            table += '<th class="col-md-2">State</th>'
            table += '<th class="col-md-2">Country</th>'
            table += '<th class="col-md-2">Pincode</th>'
            table += '<th class="col-md-2">Active</th>'
            table += '</tr></thead><tbody>'
            let firstCustomer = "";
            
            // iterate over customers
            for(let i = 0, counter = 0; i < res.length; i++) {
                let customer = res[i];
                let num_addresses = customer.addresses.length;

                for(let j = 0; j < num_addresses; j++){
                    table +=  `<tr id="row_${counter}">
                    <td>${customer.id}</td>
                    <td>${customer.first_name}</td>
                    <td>${customer.last_name}</td>
                    <td>${customer.email}</td>
                    <td>${customer.password}</td>
                    <td>${customer.addresses[j].street}</td>
                    <td>${customer.addresses[j].city}</td>
                    <td>${customer.addresses[j].state}</td>
                    <td>${customer.addresses[j].country}</td>
                    <td>${customer.addresses[j].pin_code}</td>
                    <td>${customer.active}</td></tr>`;
                    counter++;
                }

                counter++;
                
                if (i == 0) {
                    firstCustomer = customer;
                }
            }
            table += '</tbody></table>';
            $("#search_results").append(table);

            // copy the first result to the form
            if (firstCustomer != "") {
                update_form_data(firstCustomer)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

});