def serch_fromMail(mail):
    if mail == "takayasu1j202h19@gmail.com":
        w = ((mail,"takayasu777","free",""),)
    elif mail == "takayasu.y.aa@m.titech.ac.jp":
        w = ((mail,"takayasu777","pro",""),)
    else:
        w = (())
    return w

def insert(mail,pwd,meta):
    return True

def delete(mail):
    return

def upgrade(mail):
    return True

def search(tag,mail):
    if mail=="takayasu1j202h19@gmail.com":
        w = ((mail,"takayasu777","pro",""),)
    else:
        w = ((mail,"takayasu777","free",""),)
    return w

flask_key =  b'oppython3'
stripe_key = 'oppython3'
PUBLISHABLE_KEY = 'pk_test_51HsSwBKTMlPLG6E8Whlb3sxsje4z0CWOezFm1PtLRwMcLBnPhopCuUh1kC9vVMb1VMG7NSWg4HjC3yj0PtNSjnZE00xk7jknQp'
SECRET_KEY = 'sk_test_51HsSwBKTMlPLG6E8ndIBNV5OjMFmwJIZZ4lGTUSOLMUoMQX8DHyMUNHI0jA7bGAEeW4SebPi4yaYqFKuYphQS04f00t4FpoZmR'
mail_pass = "oppython3"
