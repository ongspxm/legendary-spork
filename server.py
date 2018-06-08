import bottle

def user_logIn(req, res):
    # check email & user exist
    # generate code
    # return part1 of code
    pass

def user_verify(req, res):
    # check email & code exist
    # check ok
    # generate jwt token from ext
    pass

def user_updateName(req, res):
    # verify jwt
    # chg name
    pass
