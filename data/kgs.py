import requestsa
from bs4 import BeautifulSoup

API_URL = "https://www.gokgs.com/json/access"
TOP100_URL = "https://gokgs.com/top100.jsp"


class KGS:
    def __init__(self, login, password, loc):
        self.cookie = None

        self.login(login, password, loc)

    def login(self, login, password, loc):
        data = {"type": "LOGIN",
                "name": login,
                "password": password,
                "locale": loc}
        self.cookie = requests.post(API_URL, json=data).cookies

        response = requests.get(API_URL, cookies=self.cookie).json()
        # if response['messages'][1]['type'] == 'LOGIN_FAILED_BAD_PASSWORD':
        #     raise ValueError
        # return response

    def req(self, data):
        requests.post(API_URL, json=data, cookies=self.cookie)

        return requests.get(API_URL, cookies=self.cookie).json()

    def join_archive_request(self, name):
        data = {"type": "JOIN_ARCHIVE_REQUEST",
                "name": name}
        return self.req(data)

    def details_join_request(self, name):
        data = {"type": "DETAILS_JOIN_REQUEST",
                "name": name}
        return self.req(data)

    def room_load_game(self, timestamp, channelId):
        data = {"type": "ROOM_LOAD_GAME",
                "timestamp": timestamp,
                "channelId": channelId}
        return self.req(data)

    def get_users_games(self, user):
        self.details_join_request(user)
        # to be continued...
        return

    def parse_top_100(self):
        page = requests.get(TOP100_URL).content
        soup = BeautifulSoup(page, "html.parser")
        return [u.contents[0] for u in soup.find_all("a")[:-1]]

    @staticmethod
    def get_typed(json, type):
        for m in json["messages"]:
            if m["type"] == type:
                return m
