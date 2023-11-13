from my_network import *
from apscheduler.schedulers.blocking import BlockingScheduler
import os
import time
from threading import Thread


def console():
    time.sleep(0.5)
    print("Type 'quit' to end the script")
    while scheduler.running:
        cmd = str(input(""))
        if cmd == 'quit':
            scheduler.shutdown()


def do_action():
    my_print("Starting day...")
    settings.reload()
    my_print("Reloaded settings!")
    token_main = login(settings.get_main_account())
    if token_main is not None:
        my_print("Logged in on main account.")
        reward(token_main)
        my_print("Took reward")
        categories_list = categories(token_main)
        my_missing_cards = get_missing(entities(token_main, categories_list)) # return a list with all card ids that isnt in my collection yet

        my_print("------------")
        for account in settings.get_others_accounts():
            token = login(account)
            if token is None:
                my_print("Failed to login with account: " + account["id"])
                continue
            my_print("Logged in on account " + account["id"])
            duplicates = reward(token)
            my_print("Took reward")
            for dup in duplicates:
                my_print(str(dup) + " was a duplicate, starting share...")
                activate_card(token_main, token, dup, my_missing_cards)
                my_print("Share successful.")
            my_print("Logout from account\n------------")
            logout(token)

        if settings.is_discord_enabled():
            my_print("Getting entities...")
            my_entities = entities(token_main, categories_list)
            my_missing_cards = get_missing(my_entities)
            my_duplicates_card = get_duplicates(my_entities)
            my_print("Editing discord messages with dup and miss...")
            edit_discord_messages(my_missing_cards, my_duplicates_card)

        logout(token_main)
        my_print("Logged out from main\nEnding day...\n------------")


if __name__ == "__main__":

    if not os.path.exists('logs'):
        os.mkdir('logs')

    #configure the scheduler to run my task at 4am but not running it yet
    scheduler = BlockingScheduler()
    scheduler.add_job(do_action, 'cron', hour=4)

    Thread(target=console, daemon=True).start()

    my_print('Program started')
    scheduler.start()
