from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
def stoken(sid,seconds):
    s=Serializer('KS@917_PATHIVADA038',seconds)
    return s.dumps({'sid':sid}).decode('utf-8')
