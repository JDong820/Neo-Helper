def encrypt(msg, key):
    output = []
    for c in msg:
        output.append(int(ord(c))*int(key))
    return output

def decrypt(code, key):
    output = ''
    for c in code:
        output += chr(int(c)/int(key))
    return output
