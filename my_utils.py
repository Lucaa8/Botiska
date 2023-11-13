import copy
import requests as r
import json
from collections import defaultdict
from my_settings import Settings
import unicodedata
from datetime import datetime

settings: Settings = Settings()

cards_mapping = dict()

# to sort words "naturally" and not with their ascii code. E.g: Émilie will be put with other "E" names instead of in last position after the "Z"
sort_by_name = lambda x: ''.join(c for c in unicodedata.normalize('NFD', cards_mapping[x].lower()) if unicodedata.category(c) != 'Mn')

BASE_URL = "https://historiska.ch/api"

ROUTES = {
    "login": f"{BASE_URL}/login",
    "logout": f"{BASE_URL}/logout",
    "reward": f"{BASE_URL}/reward/open",
    "categories": f"{BASE_URL}/categories",
    "get_cards": lambda category_id: f"{BASE_URL}/collection/filter/category/{category_id}",
    "get_card": lambda id_card: f"{BASE_URL}/entities/{id_card}",
    "toggle_share": lambda mode, entity_id: f"{BASE_URL}/card/share/{mode}/{entity_id}",# mode is 'enable' or 'disable'
    "activate_card": lambda card_code: f"{BASE_URL}/card/share/activate/{card_code}",# the code sent by toggle_share when mode='enable'
    "discord": lambda d_channel_id, d_message_id: f"https://discord.com/api/{settings.get_discord_version()}/channels/{d_channel_id}/messages/{d_message_id}"
}

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
    "Accept": "*/*",
    "Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin"
}


def add_header(headers: dict[str, str], key: str, value: str) -> dict[str, str]:
    headers = copy.deepcopy(headers)
    headers[key] = value
    return headers


def add_token_header(headers: dict[str, str], token: str) -> dict[str, str]:
    return add_header(headers, "Authorization", token)


def get_response_json(response: r.Response) -> None | dict:
    if (response is None) or (response.headers is None):
        return None
    headers = response.headers
    if ("Content-Type" in headers) and (headers["Content-Type"] == "application/json"):
        return json.loads(response.text)
    return None


def is_response_success(body_json: dict) -> bool:
    return (body_json is not None) and ("success" in body_json) and (body_json["success"] is True)


def get_missing(entities_list: dict[int, list[int]]) -> list[int]:
    missing = list()
    for card in entities_list:
        if len(entities_list[card]) == 0:
            missing.append(card)
    return missing


def get_duplicates(entities_list: dict[int, list[int]]) -> dict[int, list[int]]:
    duplicates = defaultdict(lambda: list())
    for card in entities_list:
        if card in settings.get_excluded_cards():
            continue
        entities = entities_list[card]
        if len(entities) > settings.get_minimum_cards_remaining():
            duplicates[int(card)] = entities[:-settings.get_minimum_cards_remaining()]
    return duplicates


def build_missing_message(missing: list[int]) -> str:
    missing = sorted(missing, key=sort_by_name)
    message = ""
    for card in missing:
        message += f"- {cards_mapping[card]}\n"
    return f"**Il me manque**({len(missing)}):\n{message}"


def build_duplicates_message(duplicates: dict[int, list[int]]) -> str:
    duplicates = {key: duplicates[key] for key in sorted(duplicates.keys(), key=sort_by_name)}
    message = ""
    for dup in duplicates:
        message += f"- {cards_mapping[dup]} ({len(duplicates[dup])}x)\n" if len(duplicates[dup]) > 1 else f"- {cards_mapping[dup]}\n"
    return f"**MES DOUBLES**:\n{message}"


def get_current_day_and_time():
    return f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}]"


def get_current_day_logfile() -> str:
    return f"logs/{datetime.now().strftime('%d.%m.%Y')}.log"

def my_print(txt: str):
    format_txt = f"{get_current_day_and_time()} {txt}"
    print(format_txt)
    with open(get_current_day_logfile(), 'a+') as f:
        f.write(format_txt+'\n')