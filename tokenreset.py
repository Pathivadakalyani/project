from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
def token(rollno,seconds):
    s=Serializer('KS@917_PATHIVADA038',300)
    return s.dumps({'user':rollno}).decode('utf-8')
