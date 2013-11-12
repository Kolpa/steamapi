from .core import APIConnection, SteamObject
from .user import SteamUser

__author__ = 'Kolpa'


class SteamUserIsHiddenException(Exception):
    def __init__(self):
        self.message = 'the user has set his steam id to hidden'


class Match(SteamObject):
    _id = 570

    def __init__(self, data):
        self.data = data

    def __getattr__(self, item):
        return self.data[item]

    @property
    def players(self):
        players = []
        for player in self.data.players:
            players.append(Player(player))
        return players


class Player(SteamObject):
    _id = 570

    def __init__(self, data):
        self.data = data

    def __getattr__(self, item):
        return self.data[item]

    @property
    def steam_account(self):
        if self.data.account_id is not None and self.data.account_id != 4294967295:
            return SteamUser('765{0}'.format(str(self.data.account_id + 61197960265728)))
        raise SteamUserIsHiddenException

    @property
    def hero_name(self):
        heroes = APIConnection().call('IEconDOTA2_570', 'GetHeroes', 'V0001', language='en').result.heroes
        for hero in heroes:
            if self.hero_id == hero.id:
                return hero.localized_name

    @property
    def is_radi(self):
        if self.player_slot & 1:
            return True
        return False


class MatchHistory(SteamObject):
    _id = 570

    def __init__(self, **kwargs):
        self.data = APIConnection().call('IDOTA2Match_570', 'GetMatchHistory', 'V001', **kwargs).result

    def get_match_details(self, match):
        return Match(
            APIConnection().call('IDOTA2Match_570',
                                 'GetMatchDetails',
                                 'V001',
                                 match_id=self.data.matches[match].match_id).result)

    def __getitem__(self, item):
        return self.get_match_details(item)

    def __getattr__(self, item):
        return self.data[item]

    @property
    def all_match_details(self):
        details = []
        for match in self.data.matches:
            details.append(
                Match(
                    APIConnection().call('IDOTA2Match_570',
                                         'GetMatchDetails',
                                         'V001',
                                         match_id=match.match_id).result))
        return details