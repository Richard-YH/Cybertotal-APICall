import requests
import re
from api_table import RESTful_API


TOKEN = 'Token'
CYBERTOTAL_URL = "https://cybertotal.cycarrier.com"


def determine_ioc_type(ioc):
    patterns = {
        "ip": r"(\d+\.\d+\.\d+\.\d+\Z)",
        "email": r"^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$",
        "domain": r"^([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}$",
        "hash": r"^(((([a-z,1-9]+)|[0-9,A-Z]+))([^a-z\.]))*",
        "url": r"((http|https)://)(www.)?[a-zA-Z0-9@:%._\\+~#?&//=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%._\\+~#?&//=]*)"
    }

    for ioc_type, pattern in patterns.items():
        if re.fullmatch(pattern, ioc):
            return ioc_type
    return None


def api_call(ioc, parameter):
    ioc_type = determine_ioc_type(ioc)
    if ioc_type is None:
        print("Invalid IOC")
        return

    restful_api = CYBERTOTAL_URL + RESTful_API(ioc_type, parameter) + ioc
    headers = {'Authorization': TOKEN}

    try:
        response = requests.get(restful_api, headers=headers)
        if response.status_code == 200:
            result = {f"{ioc}_{parameter}": response.json()}
            print(result)
        else:
            print("Status Error")
            print(f"{response.status_code} Error with your request")
    except requests.exceptions.RequestException:
        print("Error")


def main():
    while True:
        print("Please enter IOC and parameter:")
        try:
            ioc, parameter = input('').split(' -')
            api_call(ioc, parameter)
        except ValueError:
            print("Input Error")


if __name__ == '__main__':
    main()
