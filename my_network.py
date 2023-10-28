from my_utils import *


def login(acc: dict) -> str | None:
    response = r.post(ROUTES["login"], headers=add_header(DEFAULT_HEADERS, "Content-Type", "application/json"), json=acc)
    if response.status_code == 200:
        return get_response_json(response)["content"]["token"]
    return None


def logout(tk: str):
    r.post(ROUTES["logout"], headers=add_token_header(DEFAULT_HEADERS, tk))


def reward(tk: str) -> list[int]:
    response = get_response_json(r.post(ROUTES["reward"], headers=add_token_header(DEFAULT_HEADERS, tk)))
    duplicates = list()
    if is_response_success(response):
        content = response["content"]
        for card in content:
            if not card["is_new"] and not card["is_gold"]: #its a duplicate
                duplicates.append(card["id"])
    return duplicates


def categories(tk: str) -> list[tuple[int, int]] | None:
    response = get_response_json(r.get(ROUTES["categories"], headers=add_token_header(DEFAULT_HEADERS, tk)))
    if is_response_success(response):
        categories_ids = list()
        for category in response["content"]:
            categories_ids.append((category["id"], category["owned_qty"]))
        return categories_ids
    return None


def entities(tk: str, categories_list: list[tuple[int, int]]) -> dict[int, list[int]]:
    all_entities = defaultdict(lambda: list())
    if categories_list is None:
        return all_entities
    cards_mapping.clear()
    for category in categories_list:
        response = get_response_json(r.get(ROUTES["get_cards"](category[0]), headers=add_token_header(DEFAULT_HEADERS, tk)))
        if is_response_success(response):
            for card in response["content"]["cards"]:
                if card["is_gold"]:
                    continue
                card_id = str(card["id"])
                cards_mapping[int(card_id)] = card["name"]
                card_entities = all_entities[int(card_id)]
                if card_id in response["content"]["entities"]:
                    for entity in response["content"]["entities"][card_id]:
                        if not entity["is_gold"]:
                            card_entities.append(entity["entity_id"])
        else:
            break
    return all_entities


def toggle_card(tk: str, card: int) -> str | None:
    response = get_response_json(r.get(ROUTES["get_card"](card), headers=add_token_header(DEFAULT_HEADERS, tk)))
    if is_response_success(response):
        entity = response["content"][0]["entity_id"]
        response = get_response_json(r.post(ROUTES["toggle_share"]("enable", str(entity)), headers=add_token_header(DEFAULT_HEADERS, tk)))
        if is_response_success(response):
            return response["content"]["code"]
    return None


def activate_card(tk_main: str, tk_dup: str, card: int, missing_cards: list[int]):
    code = toggle_card(tk_dup, card)
    if code is not None:
        response = get_response_json(r.post(ROUTES["activate_card"](code), headers=add_token_header(DEFAULT_HEADERS, tk_main)))
        if is_response_success(response) and card in missing_cards:
            print("Got a new card! ("+response["content"]["name"]+")")


def edit_discord_messages(list_missing: list[int], list_duplicates: dict[int, list[int]]):
    d_dup_info = settings.get_discord_duplicates_info()
    d_miss_info = settings.get_discord_missing_info()
    d_header = {"Authorization": settings.get_discord_token()}
    r.patch(ROUTES["discord"](d_dup_info["channel_id"], d_dup_info["message_id"]), headers=d_header, json={"content": build_duplicates_message(list_duplicates)})
    r.patch(ROUTES["discord"](d_miss_info["channel_id"], d_miss_info["message_id"]), headers=d_header, json={"content": build_missing_message(list_missing)})

