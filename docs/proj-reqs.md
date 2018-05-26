## queries
- [ ] one host or multiple placing
- [ ] white-listing / black-listing of time period

## user stories
### administrative
- login and simple acct management ctrl
- add new users 
- delete users
- alter information of users

### users (searching for vacancies)
- searching: search by text
- filtering: traditions allowed
- filtering: monks / nuns
- filtering: duration of stay
- filtering: blocked periods of time
- view monastry info (picture and details)
- leave a message for monastry (email forwarded to them)

### monastry (providing vacancies)
- able to login to alter data from email
- map location (embed)
- name, duration, num of rooms
- traditions of monks + gender
- black-listing of period of stay
- add new places & alter information
- upload images of the place

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
- email handling by mailgun (require domain)
