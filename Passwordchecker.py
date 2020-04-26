import requests
import hashlib
import sys



def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code!=200:
        raise RuntimeError(f'Error fecthing:{res.status_code},check the url and try again')
    return res

def pwned_api_check(password):
    sha1pasword=hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5char,tail=sha1pasword[:5],sha1pasword[5:]
    response=request_api_data(first5char)
    return get_passwordreads(response.text,tail)

def get_passwordreads(hash,hash_to_check):
    list=hash.splitlines()
    for i in range(len(hash.splitlines())):
        data=list[i].split(':')
        password_code=data[0]
        number=data[1]
        if password_code==hash_to_check:
            return number
    return 0

def main(args):
    for password in args:
        count=pwned_api_check(password)
        if count:
            print(f'Your pasword was found {count} times, so Please change password')
        else:
            print("password is good...please proceed")
    return 'done'


if __name__=='__main__':
    sys.exit(main(sys.argv[1:]))