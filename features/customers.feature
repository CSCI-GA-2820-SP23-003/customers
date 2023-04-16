Feature: The customers service back-end
    As a Customer Service Manager/ System Admin
    I need the ability to do CRUD operations on customers and addresses
    So that I can maintain customer's records

Background:
    Given the following customers
        |    firstname     |   lastname    |         email         |   password   |   active   |     street         |   city        |  state        |   country         | pincode   |
        | FNU              | Akshama       | akshama@gmail.com     | 123456       | True       |    Casselberry Way |   Monroe      |   New Jersey  |   United States   |   07310   |
        | Ayush            | Jain          | ayush@gmail.com       | 234567       | True       |    Tonnelle Ave    |   Journal Sq  |   New Jersey  |   United States   |   07311   |
        | Marwan           | Aljumiah      | marwan@gmail.com      | 345678       | True       |    Washington Blvd |   Newport     |   New Jersey  |   United States   |   07312   |
        | Sai Himal        | Allu          | saihimal@gmail.com    | 456789       | True       |    Broadway        |   Manhattan   |   New York    |   United States   |   07313   |
        | FNU              | Sreevishnu    | sreevishnu@gmail.com  | 549871       | True       |    Jackson Heights |   Queens      |   New York    |   United States   |   07314   |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Customers RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Retrieve a Customer and corresponding Address
    When I visit the "Home Page"
    And I set the "first_name" to "Bob"
    And I set the "last_name" to "Alice"
    And I set the "email" to "bob@gmail.com"
    And I set the "password" to "test"
    And I set the "street" to "Newport Pkwy"
    And I set the "city" to "Jersey City"
    And I set the "state" to "New Jersey"
    And I set the "country" to "United States"
    And I set the "pin_code" to " 07310"
    And I select "True" in the "active" dropdown
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "first_name" field should be empty
    And the "last_name" field should be empty
    And the "email" field should be empty
    And the "password" field should be empty
    And the "street" field should be empty
    And the "city" field should be empty
    And the "state" field should be empty
    And the "country" field should be empty
    And the "pin_code" field should be empty
    And I should see "True" in the "Active" dropdown
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Bob" in the "first_name" field
    And I should see "Alice" in the "last_name" field
    And I should see "bob@gmail.com" in the "email" field
    And I should see "test" in the "password" field
    And I should see "True" in the "Active" dropdown
    And I should see "Newport Pkwy" in the "street" field
    And I should see "Jersey City" in the "city" field
    And I should see "New Jersey" in the "state" field
    And I should see "United States" in the "country" field
    And I should see "07310" in the "pin_code" field

Scenario: Create a Customer
    When I visit the "Home Page"
    And I set the "first_name" to "John"
    And I set the "last_name" to "Doe"
    And I set the "email" to "johndoe@gmail.com"
    And I set the "password" to "test"
    And I set the "street" to "Newport Pkwy"
    And I set the "city" to "Jersey City"
    And I set the "state" to "New Jersey"
    And I set the "country" to "United States"
    And I set the "pin_code" to " 07310"
    And I select "True" in the "active" dropdown
    And I press the "Create" button
    Then I should see the message "Success"

Scenario: Create a Customer with Bad Email format
    When I visit the "Home Page"
    And I set the "first_name" to "John"
    And I set the "last_name" to "Doe"
    And I set the "email" to "BAD_EMAIL_FORMAT"
    And I set the "password" to "test"
    And I set the "street" to "Newport Pkwy"
    And I set the "city" to "Jersey City"
    And I set the "state" to "New Jersey"
    And I set the "country" to "United States"
    And I set the "pin_code" to " 07310"
    And I select "True" in the "active" dropdown
    And I press the "Create" button
    Then I should see the message "Form Error(s)"
    And I should see "This doesn't appear to be a valid email address" in the "email" error string

Scenario: Create a Customer with Missing First Name
    When I visit the "Home Page"
    And I set the "last_name" to "Doe"
    And I set the "email" to "jd@gmail.com"
    And I set the "password" to "test"
    And I set the "street" to "Newport Pkwy"
    And I set the "city" to "Jersey City"
    And I set the "state" to "New Jersey"
    And I set the "country" to "United States"
    And I set the "pin_code" to " 07310"
    And I select "True" in the "active" dropdown
    And I press the "Create" button
    Then I should see the message "Form Error(s)"
    And I should see "Required field" in the "first_name" error string
    When I set the "first_name" to "John"
    And I press the "Create" button
    Then The "first_name" error string should be gone

Scenario: Create a Customer with Missing Last Name
    When I visit the "Home Page"
    And I set the "first_name" to "John"
    And I set the "email" to "jd@gmail.com"
    And I set the "password" to "test"
    And I set the "street" to "Newport Pkwy"
    And I set the "city" to "Jersey City"
    And I set the "state" to "New Jersey"
    And I set the "country" to "United States"
    And I set the "pin_code" to " 07310"
    And I select "True" in the "active" dropdown
    And I press the "Create" button
    Then I should see the message "Form Error(s)"
    And I should see "Required field" in the "last_name" error string
    When I set the "last_name" to "Doe"
    And I press the "Create" button
    Then The "last_name" error string should be gone

Scenario: Create a Customer with Missing Email
    When I visit the "Home Page"
    And I set the "first_name" to "John"
    And I set the "last_name" to "Doe"
    And I set the "password" to "test"
    And I set the "street" to "Newport Pkwy"
    And I set the "city" to "Jersey City"
    And I set the "state" to "New Jersey"
    And I set the "country" to "United States"
    And I set the "pin_code" to " 07310"
    And I select "True" in the "active" dropdown
    And I press the "Create" button
    Then I should see the message "Form Error(s)"
    And I should see "Required field" in the "email" error string
    When I set the "email" to "jd_@gmail.com"
    And I press the "Create" button
    Then The "email" error string should be gone

Scenario: Create a Customer with Missing Password
    When I visit the "Home Page"
    And I set the "first_name" to "John"
    And I set the "last_name" to "Doe"
    And I set the "email" to "jd@gmail.com"
    And I set the "street" to "Newport Pkwy"
    And I set the "city" to "Jersey City"
    And I set the "state" to "New Jersey"
    And I set the "country" to "United States"
    And I set the "pin_code" to " 07310"
    And I select "True" in the "active" dropdown
    And I press the "Create" button
    Then I should see the message "Form Error(s)"
    And I should see "Required field" in the "password" error string
    When I set the "password" to "test"
    And I press the "Create" button
    Then The "password" error string should be gone