Queries
- [ ] one host or multiple placing

## user stories
### administrative
- login and simple acct management ctrl
- add new users 
- delete users
- alter information of users

### users (searching for vacancies)
- searching and sorting of vacancies
- view monastry info
- leave a message for monastry

### monastry (providing vacancies)
- map location (embed)
- name, duration, num of rooms
- traditions of monks
- add new places & alter information
- upload images of the place
- able to login to alter data from email

### adminstrative authentication
- special fb accts given access
- jwt token authentication
- admins(u_auth TEXT)

### monastry authentication
- email authenticated, sub code will be sent to their emails (maybe mailgun, but require domain)
- subcode submitted will be exchanged for jwt token to be used in API

### portal implementation details
- vue powered SPA frontend
- jwt auth for sessions (logmein)
- REST api backend, authenticated
- image hosting on imgur
