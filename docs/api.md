# API

## Login
### /login
- `?email=`
- will return a 3 word phrase, first part of token
- code will be emailed to the particular email

### /tkn
- `?email=&code=`
- will return a token if token matches

## User
### /user/name
- `?name=` with tkn
- if authorize will change the user's name and return `ok`

## Admin
### /admin/newUser
- `?email=&name=` with tkn
- if authorize will create a new user with the email and name
- return `ok` if valid

### /admin/listUsers
- with admin tkn, will return list of username

## Room
### /rooms
- '?pager=&email='
- dun require authentication
- return all those after `pager`
- if `email` given, return only rooms of that user

### /room/new
- `?name=&vacancy=&weekRange=` with tkn
- create a new room under the logged in user.
- will return `ok` if successful

### /room/edit
- `?rm=&name=&vacancy=&weekRange=` with tkn
- edit details for a specific room if authorized
- will return `ok` if successful

### /room/newImg (POST)
- `?rm=&img=` with tkn, img is formData(file)
- insert picture to room if authorized
- will return `<link> <imgur_id>` if ok

### /room/delImg
- `?rm=&imgId=` with tkn
- remove picture to room if authorized
- will return `ok` if ok
