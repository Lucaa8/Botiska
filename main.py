from my_network import *
from apscheduler.schedulers.blocking import BlockingScheduler


def do_action():
    print("Starting day " + get_current_day_and_time() + "...")
    settings.reload()
    print("Reloaded settings!")
    token_main = login(settings.get_main_account())
    if token_main is not None:
        print("Logged in on main account.")
        reward(token_main)
        print("Took reward")
        categories_list = categories(token_main)
        my_missing_cards = get_missing(entities(token_main, categories_list)) # return a list with all card ids that isnt in my collection yet

        print("------------")
        for account in settings.get_others_accounts():
            token = login(account)
            if token is None:
                print("Failed to login with account: " + account["id"])
                continue
            print("Logged in on account " + account["id"])
            duplicates = reward(token)
            print("Took reward")
            for dup in duplicates:
                print(str(dup) + " was a duplicate, starting share...")
                activate_card(token_main, token, dup, my_missing_cards)
                print("Share successful.")
            print("Logout from account\n------------")
            logout(token)

        if settings.is_discord_enabled():
            print("Getting entities...")
            my_entities = entities(token_main, categories_list)
            my_missing_cards = get_missing(my_entities)
            my_duplicates_card = get_duplicates(my_entities)
            print("Editing discord messages with dup and miss...")
            edit_discord_messages(my_missing_cards, my_duplicates_card)

        logout(token_main)
        print("Logged out from main\nEnding day " + get_current_day_and_time() + "...\n------------")


if __name__ == "__main__":
    print(get_current_day_and_time())
    scheduler = BlockingScheduler()
    scheduler.add_job(do_action, 'cron', hour=4)
    scheduler.start()

