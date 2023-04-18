Feature: The customers service back-end
    As a Customer Service Manager/ System Admin
    I need the ability to do CRUD operations on customers and addresses
    So that I can maintain customer's records

Background:
    Given the following customers
        |    First Name     |   Last Name    |         Email         |   Password   |   Active   |     Street         |   City        |  State        |   Country         | Pin Code   |
        | FNU              | Akshama       | akshama@gmail.com     | 123456       | True       |    Casselberry Way |   Monroe      |   New Jersey  |   United States   |   07310   |
        | Ayush            | Jain          | ayush@gmail.com       | 234567       | True       |    Tonnelle Ave    |   Journal Sq  |   New Jersey  |   United States   |   07311   |
        | Marwan           | Aljumiah      | marwan@gmail.com      | 345678       | True       |    Washington Blvd |   Newport     |   New Jersey  |   United States   |   07312   |
        | Sai Himal        | Allu          | saihimal@gmail.com    | 456789       | True       |    Broadway        |   Manhattan   |   New York    |   United States   |   07313   |
        | FNU              | Sreevishnu    | sreevishnu@gmail.com  | 549871       | False       |    Jackson Heights |   Queens      |   New York    |   United States   |   07314   |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Customers RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Retrieve a Customer and corresponding Address
    When I visit the "Home Page"
    And I set the "First Name" to "Bob"
    And I set the "Last Name" to "Alice"
    And I set the "Email" to "bob@gmail.com"
    And I set the "Password" to "test"
    And I set the "Street" to "Newport Pkwy"
    And I set the "City" to "Jersey City"
    And I set the "State" to "New Jersey"
    And I set the "Country" to "United States"
    And I set the "Pin Code" to " 07310"
    And I select "True" in the "active" dropdown
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then I should see the message "Cleared"
    And the "Id" field should be empty
    And the "First Name" field should be empty
    And the "Last Name" field should be empty
    And the "Email" field should be empty
    And the "Password" field should be empty
    And the "Street" field should be empty
    And the "City" field should be empty
    And the "State" field should be empty
    And the "Country" field should be empty
    And the "Pin Code" field should be empty
    And I should see "True" in the "Active" dropdown
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Bob" in the "First Name" field
    And I should see "Alice" in the "Last Name" field
    And I should see "bob@gmail.com" in the "Email" field
    And I should see "test" in the "Password" field
    And I should see "True" in the "Active" dropdown
    And I should see "Newport Pkwy" in the "Street" field
    And I should see "Jersey City" in the "City" field
    And I should see "New Jersey" in the "State" field
    And I should see "United States" in the "Country" field
    And I should see "07310" in the "Pin Code" field

Scenario: Create a Customer
    When I visit the "Home Page"
    And I set the "First Name" to "John"
    And I set the "Last Name" to "Doe"
    And I set the "Email" to "johndoe@gmail.com"
    And I set the "Password" to "test"
    And I set the "Street" to "Newport Pkwy"
    And I set the "City" to "Jersey City"
    And I set the "State" to "New Jersey"
    And I set the "Country" to "United States"
    And I set the "Pin Code" to " 07310"
    And I select "True" in the "Active" dropdown
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then I should see the message "Cleared"
    And the "Id" field should be empty
    And the "First Name" field should be empty
    And the "Last Name" field should be empty
    And the "Email" field should be empty
    And the "Password" field should be empty
    And the "Street" field should be empty
    And the "City" field should be empty
    And the "State" field should be empty
    And the "Country" field should be empty
    And the "Pin Code" field should be empty
    And I should see "True" in the "Active" dropdown
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "John" in the "First Name" field
    And I should see "Doe" in the "Last Name" field
    And I should see "johndoe@gmail.com" in the "Email" field
    And I should see "test" in the "Password" field
    And I should see "True" in the "Active" dropdown
    And I should see "Newport Pkwy" in the "Street" field
    And I should see "Jersey City" in the "City" field
    And I should see "New Jersey" in the "State" field
    And I should see "United States" in the "Country" field
    And I should see "07310" in the "Pin Code" field

Scenario: Create a Customer with Bad Email format
    When I visit the "Home Page"
    And I set the "First Name" to "John"
    And I set the "Last Name" to "Doe"
    And I set the "Email" to "BAD_EMAIL_FORMAT"
    And I set the "Password" to "test"
    And I set the "Street" to "Newport Pkwy"
    And I set the "City" to "Jersey City"
    And I set the "State" to "New Jersey"
    And I set the "Country" to "United States"
    And I set the "Pin Code" to " 07310"
    And I select "True" in the "Active" dropdown
    And I press the "Create" button
    Then I should see the message "Form Error(s)"
    And I should see "This doesn't appear to be a valid email address" in the "Email" error string

Scenario: Create a Customer with Missing First Name
    When I visit the "Home Page"
    And I set the "Last Name" to "Doe"
    And I set the "Email" to "jd@gmail.com"
    And I set the "Password" to "test"
    And I set the "Street" to "Newport Pkwy"
    And I set the "City" to "Jersey City"
    And I set the "State" to "New Jersey"
    And I set the "Country" to "United States"
    And I set the "Pin Code" to " 07310"
    And I select "True" in the "Active" dropdown
    And I press the "Create" button
    Then I should see the message "Form Error(s)"
    And I should see "Required field" in the "First Name" error string
    When I set the "First Name" to "John"
    And I press the "Create" button
    Then The "First Name" error string should be gone

Scenario: Create a Customer with Missing Last Name
    When I visit the "Home Page"
    And I set the "First Name" to "John"
    And I set the "Email" to "jd@gmail.com"
    And I set the "Password" to "test"
    And I set the "Street" to "Newport Pkwy"
    And I set the "City" to "Jersey City"
    And I set the "State" to "New Jersey"
    And I set the "Country" to "United States"
    And I set the "Pin Code" to " 07310"
    And I select "True" in the "Active" dropdown
    And I press the "Create" button
    Then I should see the message "Form Error(s)"
    And I should see "Required field" in the "Last Name" error string
    When I set the "Last Name" to "Doe"
    And I press the "Create" button
    Then The "Last Name" error string should be gone

Scenario: Create a Customer with Missing Email
    When I visit the "Home Page"
    And I set the "First Name" to "John"
    And I set the "Last Name" to "Doe"
    And I set the "Password" to "test"
    And I set the "Street" to "Newport Pkwy"
    And I set the "City" to "Jersey City"
    And I set the "State" to "New Jersey"
    And I set the "Country" to "United States"
    And I set the "Pin Code" to " 07310"
    And I select "True" in the "Active" dropdown
    And I press the "Create" button
    Then I should see the message "Form Error(s)"
    And I should see "Required field" in the "Email" error string
    When I set the "Email" to "jd_@gmail.com"
    And I press the "Create" button
    Then The "Email" error string should be gone

Scenario: Create a Customer with Missing Password
    When I visit the "Home Page"
    And I set the "First Name" to "John"
    And I set the "Last Name" to "Doe"
    And I set the "Email" to "jd@gmail.com"
    And I set the "street" to "Newport Pkwy"
    And I set the "City" to "Jersey City"
    And I set the "State" to "New Jersey"
    And I set the "Country" to "United States"
    And I set the "Pin Code" to " 07310"
    And I select "True" in the "Active" dropdown
    And I press the "Create" button
    Then I should see the message "Form Error(s)"
    And I should see "Required field" in the "Password" error string
    When I set the "Password" to "test"
    And I press the "Create" button
    Then The "Password" error string should be gone

Scenario: Deactivate and Activate a Customer
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    When I press the "Deactivate" button
    Then I should see the message "Customer has been Deactivated!"
    And I should see "False" in the "Active" dropdown
    When I copy the "Id" field
    And I press the "Clear" button
    Then I should see the message "Cleared"
    And the "Id" field should be empty
    And the "First Name" field should be empty
    And the "Last Name" field should be empty
    And the "Email" field should be empty
    And the "Password" field should be empty
    And the "Street" field should be empty
    And the "City" field should be empty
    And the "State" field should be empty
    And the "Country" field should be empty
    And the "Pin Code" field should be empty
    And I should see "True" in the "Active" dropdown
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "False" in the "Active" dropdown
    When I press the "Activate" button
    Then I should see the message "Customer has been Activated!"
    And I should see "True" in the "Active" dropdown
    When I copy the "Id" field
    And I press the "Clear" button
    Then I should see the message "Cleared"
    And the "Id" field should be empty
    And the "First Name" field should be empty
    And the "Last Name" field should be empty
    And the "Email" field should be empty
    And the "Password" field should be empty
    And the "Street" field should be empty
    And the "City" field should be empty
    And the "State" field should be empty
    And the "Country" field should be empty
    And the "Pin Code" field should be empty
    And I should see "True" in the "Active" dropdown
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "True" in the "Active" dropdown

Scenario: Search with first name
    When I visit the "Home Page"
    And I set the "First Name" to "Ayush"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Ayush" in the results
    And I should not see "Akshama" in the results
    And I should not see "Marwan" in the results
    And I should not see "Sai Himal" in the results
    And I should not see "Sreevishnu" in the results

Scenario: Search with last name
    When I visit the "Home Page"
    And I set the "Last Name" to "Sreevishnu"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should not see "Akshama" in the results
    And I should not see "Ayush" in the results
    And I should not see "Marwan" in the results
    And I should not see "Sai Himal" in the results
    And I should see "Sreevishnu" in the results

Scenario: Search with email
    When I visit the "Home Page"
    And I set the "Email" to "sreevishnu@gmail.com"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should not see "Akshama" in the results
    And I should not see "Ayush" in the results
    And I should not see "Marwan" in the results
    And I should not see "Sai Himal" in the results
    And I should see "Sreevishnu" in the results

Scenario: Search with street
    When I visit the "Home Page"
    And I set the "Street" to "Washington Blvd"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Marwan" in the results
    And I should not see "Akshama" in the results
    And I should not see "Ayush" in the results
    And I should not see "Sai Himal" in the results
    And I should not see "Sreevishnu" in the results

Scenario: Search with city
    When I visit the "Home Page"
    And I set the "City" to "Manhattan"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Sai Himal" in the results
    And I should not see "Akshama" in the results
    And I should not see "Ayush" in the results
    And I should not see "Marwan" in the results
    And I should not see "Sreevishnu" in the results

Scenario: Search with state
    When I visit the "Home Page"
    And I set the "State" to "New Jersey"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Akshama" in the results
    And I should see "Ayush" in the results
    And I should see "Marwan" in the results
    And I should not see "Sai Himal" in the results
    And I should not see "Sreevishnu" in the results

Scenario: Search with country
    When I visit the "Home Page"
    And I set the "Country" to "United States"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Akshama" in the results
    And I should see "Ayush" in the results
    And I should see "Marwan" in the results
    And I should see "Sai Himal" in the results
    And I should see "Sreevishnu" in the results

Scenario: Search with pin code
    When I visit the "Home Page"
    And I set the "Pin Code" to "07310"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Akshama" in the results
    And I should not see "Ayush" in the results
    And I should not see "Marwan" in the results
    And I should not see "Sai Himal" in the results
    And I should not see "Sreevishnu" in the results

Scenario: Search for active
    When I visit the "Home Page"
    And I select "True" in the "Active" dropdown
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Akshama" in the results
    And I should see "Ayush" in the results
    And I should see "Marwan" in the results
    And I should see "Sai Himal" in the results
    And I should not see "Sreevishnu" in the results

Scenario: Search for not active
    When I visit the "Home Page"
    And I select "False" in the "Active" dropdown
    And I press the "Search" button
    Then I should see the message "Success"
    And I should not see "Akshama" in the results
    And I should not see "Ayush" in the results
    And I should not see "Marwan" in the results
    And I should not see "Sai Himal" in the results
    And I should see "Sreevishnu" in the results
Scenario: Update a Customer
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I set the "First Name" to "Test FN"
    And I set the "Last Name" to "Test LN"
    And I set the "Email" to "test@gmail.com"
    And I set the "Password" to "test788pass"
    And I select "True" in the "Active" dropdown
    And I set the "Street" to "10th Casselberry Way"
    And I set the "City" to "monroe"
    And I set the "Pin Code" to " 07319"
    And I set the "State" to "NJ"
    And I set the "Country" to "USA"
    And I press the "update" button
    Then I should see the message "Success"
    When I press the "clear" button
    And I paste the "Id" field
    And I press the "retrieve" button
    Then I should see the message "Success"
    And I should see "Test FN" in the "First Name" field
    And I should see "Test LN" in the "Last Name" field
    And I should see "test@gmail.com" in the "email" field
    And I should see "test788pass" in the "password" field
    And I should see "True" in the "Active" dropdown
    And I should see "10th Casselberry Way" in the "street" field
    And I should see "monroe" in the "city" field
    And I should see "NJ" in the "state" field
    And I should see "USA" in the "country" field

Scenario: Update a Customer with Bad Email format
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    When I set the "First Name" to "Test FN"
    And I set the "Last Name" to "Test LN"
    And I set the "Email" to "BAD_EMAIL_FORMAT"
    And I set the "Password" to "test788pass"
    And I select "True" in the "Active" dropdown
    And I set the "Street" to "10th Casselberry Way"
    And I set the "City" to "monroe"
    And I set the "Pin Code" to " 07319"
    And I set the "State" to "NJ"
    And I set the "Country" to "USA"
    And I press the "update" button
    Then I should see the message "Form Error(s)"
    And I should see "This doesn't appear to be a valid email address" in the "Email" error string

Scenario: Update a Customer with Missing First Name
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    When I set the "First Name" to " "
    And I set the "Last Name" to "Test LN"
    And I set the "Email" to "test_ff@domain.com"
    And I select "True" in the "Active" dropdown
    And I set the "Street" to "10th Casselberry Way"
    And I set the "City" to "monroe"
    And I set the "Pin Code" to " 07319"
    And I set the "State" to "NJ"
    And I set the "Country" to "USA"
    And I press the "update" button
    Then I should see the message "Form Error(s)"
    And I should see "Required field" in the "First Name" error string
    When I set the "First Name" to "test"
    And I press the "Update" button
    Then The "First Name" error string should be gone

Scenario: Update a Customer with Missing Last Name
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    When I set the "First Name" to "Test FN"
    And I set the "Last Name" to " "
    And I set the "Email" to "test_ff@domain.com"
    And I select "True" in the "Active" dropdown
    And I set the "Street" to "10th Casselberry Way"
    And I set the "City" to "monroe"
    And I set the "Pin Code" to " 07319"
    And I set the "State" to "NJ"
    And I set the "Country" to "USA"
    And I press the "update" button
    Then I should see the message "Form Error(s)"
    And I should see "Required field" in the "Last Name" error string
    When I set the "Last Name" to "test"
    And I press the "Update" button
    Then The "Last Name" error string should be gone

Scenario: Update a Customer with Missing Email
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    When I set the "First Name" to "Test FN"
    And I set the "Last Name" to "Test LN"
    And I set the "Email" to " "
    And I select "True" in the "Active" dropdown
    And I set the "Street" to "10th Casselberry Way"
    And I set the "City" to "monroe"
    And I set the "Pin Code" to " 07319"
    And I set the "State" to "NJ"
    And I set the "Country" to "USA"
    And I press the "update" button
    Then I should see the message "Form Error(s)"
    And I should see "Required field" in the "Email" error string
    When I set the "Email" to "test@gmail.com"
    And I press the "Update" button
    Then The "Email" error string should be gone

Scenario: Update a Customer with Missing Password
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    When I set the "First Name" to "Test FN"
    And I set the "Last Name" to "Test LN"
    And I set the "Email" to "test_ff@domain.com"
    And I set the "Password" to " "
    And I select "True" in the "Active" dropdown
    And I set the "Street" to "10th Casselberry Way"
    And I set the "City" to "monroe"
    And I set the "Pin Code" to " 07319"
    And I set the "State" to "NJ"
    And I set the "Country" to "USA"
    And I press the "update" button
    Then I should see the message "Form Error(s)"
    And I should see "Required field" in the "Password" error string
    When I set the "Password" to "test"
    And I press the "Update" button
    Then The "Password" error string should be gone 

Scenario: Delete a Customer that Exists
    When I visit the "Home Page"
    And I press the "Search" button
    And I copy the "Id" field
    And I press the "Clear" button
    Then I should see the message "Cleared"
    And the "Id" field should be empty
    And the "First Name" field should be empty
    And the "Last Name" field should be empty
    And the "Email" field should be empty
    And the "Password" field should be empty
    And the "Street" field should be empty
    And the "City" field should be empty
    And the "State" field should be empty
    And the "Country" field should be empty
    And the "Pin Code" field should be empty
    And I should see "True" in the "Active" dropdown
    When I paste the "Id" field
    And I press the "Delete" button
    Then I should see the message "Customer has been Deleted!"
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should not see "Success"
    And the "First Name" field should be empty
    And the "Last Name" field should be empty
    And the "Email" field should be empty
    And the "Password" field should be empty
    And the "Street" field should be empty
    And the "City" field should be empty
    And the "State" field should be empty
    And the "Country" field should be empty
    And the "Pin Code" field should be empty


Scenario: Delete a Customer that Does Not Exist
    When I visit the "Home Page"
    And I press the "Search" button
    And I copy the "Id" field
    And I press the "Clear" button
    Then I should see the message "Cleared"
    And the "Id" field should be empty
    And the "First Name" field should be empty
    And the "Last Name" field should be empty
    And the "Email" field should be empty
    And the "Password" field should be empty
    And the "Street" field should be empty
    And the "City" field should be empty
    And the "State" field should be empty
    And the "Country" field should be empty
    And the "Pin Code" field should be empty
    And I should see "True" in the "Active" dropdown
    When I paste the "Id" field
    And I press the "Delete" button
    Then I should see the message "Customer has been Deleted!"
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should not see "Success"
    And the "First Name" field should be empty
    And the "Last Name" field should be empty
    And the "Email" field should be empty
    And the "Password" field should be empty
    And the "Street" field should be empty
    And the "City" field should be empty
    And the "State" field should be empty
    And the "Country" field should be empty
    And the "Pin Code" field should be empty
    When I paste the "Id" field
    And I press the "Delete" button
    Then I should see the message "Customer has been Deleted!"
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should not see "Success"
    And the "First Name" field should be empty
    And the "Last Name" field should be empty
    And the "Email" field should be empty
    And the "Password" field should be empty
    And the "Street" field should be empty
    And the "City" field should be empty
    And the "State" field should be empty
    And the "Country" field should be empty
    And the "Pin Code" field should be empty




    
