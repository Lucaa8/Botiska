import json


class Settings:
    def __init__(self):
        self.settings = None
        self.reload()

    def reload(self):
        with open("config.json", "r") as config:
            self.settings = json.loads(config.read())

    def get_main_account(self):
        return self.settings["accounts"]["main"]

    def get_others_accounts(self):
        return self.settings["accounts"]["others"]

    def get_excluded_cards(self):
        return self.settings["trade_settings"]["excluded_cards"]

    def get_minimum_cards_remaining(self):
        return self.settings["trade_settings"]["minimum_remaining"]

    def get_discord_version(self):
        return self.settings["discord"]["api_version"]

    def get_discord_token(self):
        return self.settings["discord"]["token"]

    def get_discord_missing_info(self):
        return self.settings["discord"]["missing"]

    def get_discord_duplicates_info(self):
        return self.settings["discord"]["duplicates"]
