# developer guide

## api backend
### .env
setup the environmemt for the production server, mainly includes the encryption key, the api keys for the external services, etc

### schema.sql
schema for the application database. also includes template, messages and data that is required to maintain across deployment.

### package.json
configuration to run the application on the machine.

### requirements.txt
python modules required

## utils modules
### tkn.py
A token generation module adapted from the JWT standard. used for logins into the portal through a email verification.

token payload includes user email and their admin status.

expiration of token is also defined here where an expired token will result in a invalid read from the token.

### util.py
Consist of miscellenous functions and application or library based exceptions, used to consolidate all these one place for consistency.

### dbase.py
wrapper for sqlite to perform basic database function, select, insert, delete and update.

### server.py
basic routing rules for the web application. main bulk of the business logic is in here, called using the main modules.

## external services
### imgur.py
using the environment defined imgur client id, upload images and return the id to be stored in the database. also supports deletion of the images using the delete hash.

### mailgun.py
using the environment defined api key and secret, mail is sent using the mailgun service. 

## application mods 
### user.py
each user is tied to a unique email address, which is used for the verification process by sending over a 2 part verification code.

authenticated users will be given a token in exchange, which can be used to complete user actions like updating of user details

### room.py
each room is tied to a user, and each user can have multiple rooms. basic details for each room can be given.

each room can be tagged to multiple images, which can be added and removed from each room given the right authentication.

todo: add get rooms

### admin.py
admin features, basically allows admins (as defined in the admins table) to add new users. admin's view room feature returns all rooms, and frontend router will allow in all users.
