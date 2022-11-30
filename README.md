# IAM Service

The IAM Service is a means to try and reduce development time and improve security involved in Identity and Access Management.
Offering a running service listening for RESTful Calls and Responding with the neccessary UI and Handle everything else.
** This project is a means to reduce the development time of projects. **

# Description

This project and the time of this writing if currently running on this tech stack:

* Django (Python Framework for building RESTful Endpoints and Serving Web Pages)
* Javascript
* HTML (Django Templating Engine) and CSS
* Google API Client (For Authenticating with Google and Getting User Profiles)
* Facebook Customer API (For Authenticating with facebook)

How this project works is that, you redirect to us (link to be provided after deployment), And we offer your users the UI,
and The processing behind with all the neccessary encryptions (RSA-SHA1) to send and received and ensure data integrity,
Once we are done with all the authentication and authorization, we redirect the users, back to your url with an appended
encrypted userId, that you can decrypt with the private key, you would've received upon registration, and send it back to us (API)
call, and we'll return encrypted user data that you can decrypt and update your application accordingly.

The plan is to also provide a JS utility library, that will handle all the encryption and decription, and should you need to "optimize"
and keep users profiles (We already do) you can do so seamlessly by using the library to capture the userId from the url,
decrypt it, and send it to the service (IAM) and return with data and expose only (decrypted) user data. That's a feature that will be implemented
and deployed with the production ready program.

# Usage

 Setup and "login" link that you would've received from the registration page - corresponding to your project ID.  
  * Wait for response status and data in your program, and handle:  as you please 
      * Failed Authentication - status code only.
      * Successful Authentication will contain and status code and user data.
  * You can offer a retry utility, but to avoid Bruteforce attacks and that kind of stuff, we will limit the number of,
    login requests to 10 and block the "origin" for 8 next hours.


# To Do

* Implement Security Protocols and Data encryption
* Implement Resource Access Permisions (Users can only access data related to them only and nothing else)
* Add Other Social Logins (Facebook requires HTTPS, not easy in development environment ... still thinking about it)
* Build a Helper Python and JS scripts to handle flows on client side and other server side implementations
  

