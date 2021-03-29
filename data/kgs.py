import requests
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

    def room_load_game(self, timestamp, channelId):
        data = {"type": "ROOM_LOAD_GAME",
                "timestamp": timestamp,
                "channelId": channelId}
        return self.req(data)

    def parse_top_100(self):
        page = requests.get(TOP100_URL).content
        soup = BeautifulSoup(page, "html.parser")
        return [u.contents[0] for u in soup.find_all("a")[:-1]]

    @staticmethod
    def get_typed(json, type, trigger="type"):
        for m in json:
            if m[trigger] == type:
                return m

    @staticmethod
    def get_players(msg, game_id):
        res = []
        game = msg["games"][game_id]
        players = game["players"]
        for p in players:
            if p == "owner":
                continue
            res.append(players[p]["name"])
        return res

    @staticmethod
    def get_colors(msg, game_id):
        res = []
        game = msg["games"][game_id]
        players = game["players"]
        for p in players:
            if p == "owner":
                continue
            res.append(p)
        return res

    @staticmethod
    def get_score(msg, game_id):
        game = msg["games"][game_id]
        return game["score"]

    @staticmethod
    def get_duration(lobby):
        sgf = lobby["sgfEvents"]
        game_time = sgf[0]["props"][0]["mainTime"]

        last = KGS.get_typed(sgf[::-1], "PROP_GROUP_ADDED")
        sgf.remove(last)
        penult = KGS.get_typed(sgf[::-1], "PROP_GROUP_ADDED")

        last_prop = KGS.get_typed(last["props"], "TIMELEFT", trigger="name")
        penult_prop = KGS.get_typed(penult["props"], "TIMELEFT", trigger="name")

        last_time = last_prop["float"] if last_prop["int"] == 0 else 0
        penult_time = penult_prop["float"] if penult_prop["int"] == 0 else 0

        return (game_time - last_time) + (game_time - penult_time)


