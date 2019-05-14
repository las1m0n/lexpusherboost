import requests
from datetime import datetime


def _api(url):
    url = "https://api.opendota.com/api/" + url
    return requests.get(url).json()


def ratings(player_id):
    res = _api(f"players/{player_id}/ratings")
    for r in res:
        r['time'] = datetime.strptime(r['time'], "%Y-%m-%dT%H:%M:%S.%fZ")
    return res


def steam_id(inp):
    url = f"https://steamid.xyz/{inp}"
    res = requests.get(url).text
    if "Player Not Found" in res:
        return None
    res = res.split('Steam32 ID')[1]
    res = res.split('value="')[1].split('"')[0]
    return res
