from jose import jwt


payload = {'sub':'1234567890', 'name':'Jhon Dir'}

encode = jwt.encode(payload, 'dcdcd', algorithm='HS256')

print(encode)

decode = jwt.decode(encode, 'dcdcd', algorithms=['HS256'])

print(decode)