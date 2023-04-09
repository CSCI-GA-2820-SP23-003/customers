Feature: The customers service back-end
    As a Customer Service Manager/ System Admin
    I need the ability to do CRUD operations on customers
    So that I can maintain customer's records

Background:
    Given the following customers
        |    first_name    |   last_name   |         email         |   password   |   active   |   addresses                   |
        | FNU              | Akshama       | akshama@gmail.com     | 123456       | True       | FAstr,FActy,FAst,FAcntry,FApc |
        | Ayush            | Jain          | ayush@gmail.com       | 234567       | True       | AJstr,AJcty,AJst,AJcntry,AJpc |
        | Marwan           | Aljumiah      | marwan@gmail.com      | 345678       | True       | MAstr,MActy,MAst,MAcntry,MApc |
        | Sai Himal        | Allu          | saihimal@gmail.com    | 456789       | True       | SAstr,SActy,SAst,SAcntry,SApc |
        | FNU              | Sreevishnu    | sreevishnu@gmail.com  | 549871       | True       | FSstr,FScty,FSst,FScntry,FSpc |
