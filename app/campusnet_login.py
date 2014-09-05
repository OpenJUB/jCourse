import requests

_UNIVERSITY_LOGINS = [
    {
        "name": "Jacobs University Bremen",
        "url": 'https://campusnet.jacobs-university.de/scripts/mgrqispi.dll',
        "domain": 'jacobs-university.de',
        "payload": {
            'usrname': "", 
            'pass': "",
            "APPNAME": "CampusNet",
            "PRGNAME": "LOGINCHECK",
            "ARGUMENTS": "clino,usrname,pass,menuno,persno,browser,platform",
            "clino": "000000000000001",
            "menuno": "000084",
            "persno": "00000000",
            "browser": "",
            "platform": ""
        }
    }

]


def login_success(username, password):
    for university in _UNIVERSITY_LOGINS:
        payload = university['payload']
        payload["usrname"] = username
        payload["pass"] = password
        response = requests.post(university['url'], data=payload)

        if response.content.find('Wrong username or password') == -1 and response.content.find('Access denied') == -1:
            return True

    return False
