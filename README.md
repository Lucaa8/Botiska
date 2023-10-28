# Botiska
Botiska is a Python bot to help you complete your card collection on [Historiska](https://historiska.ch/)!
The script will each time a day;
- Connect to your main account and collect your 4 cards
- Connect to each second account you have and collect their 4 cards
- Give to your main account each duplicate card a second account may receive
- Warn you if you got a new card in your main collection!
- Update your Discord messages (Researched and missing cards) on the Historiska [Discord](https://discord.gg/Q8jtnYv9dE) (Optionnal)
- Logout, wait 24h and do-it again.

## Requirements
You can run this script either on Windows (tested: Windows 10) or Linux (tested: Debian 12 Bookworm) with Python 3.10 or later.

## How to run
### Linux and Windows
- Clone this repository with `git clone https://github.com/Lucaa8/Botiska.git`
- Open a CMD in the repository folder
- Create a Python virtual environnement with `python -m venv venv`
- Activate the virtual environnement with `.\venv\Scripts\activate` on Windows or `source venv/bin/activate` on Linux
- Install the Python requirements with `python -m pip install -r requirements.txt`
- Start the program with `python main.py` (You cant before the [Configuration](https://github.com/Lucaa8/Botiska#how-to-configure) step)

### Linux
If you want to run this script on a Linux server you can use `screen`
- You will need to install it with `sudo apt-get install screen`
- Create a script e.g `start.sh` and put the following line inside it `screen -S historiska -d -m bash -c "source venv/bin/activate; python main.py"`
- Give the script the execute permision with `sudo chmod 744 start.sh`
- Run the script with `./start.sh` (You cant before the [Configuration](https://github.com/Lucaa8/Botiska#how-to-configure) step)
- Now you can attach to the screen with `screen -r historiska` and detach from it (when inside) with `ctrl+a+d`

## How to configure
**Kill the script if running to continue in this step** \
In this step we will configure the bot to tell the script which Historiska account you want to use and which Discord account the bot will use.
- Rename the `config_Example.json` file to `config.json`
- Set your main account (the account you will get the cards on) credentials. `id` can be either your mail or username
```json
"main": {
  "id": "luca",
  "password": "mysecretpassword"
}
```
- Set all your second accounts (those accounts will give their duplicates to your main account). You can give as many accounts as you want
```json
"others": [
  {
    "id": "luca2",
    "password": "mysecretpassword2"
  },
  {
    "id": "luca3",
    "password": "mysecretpassword3"
  }
]
```
- ~~Set your trade restrictions~~ (Only if you are using the Discord feature). It's an advanced setting, you wont need it
- Set your Discord information if you set `enabled: true`
  - `api_version`: Leave it as it is
  - `token`: Your Discord authorization token, you can find it in API requests headers while reading the `Network` tab of Firefox or Google Chrome
  - `missing.message_id`: Your Discord message's id inside the `#cartes-recherchées` channel in the Historiska Discord.
  ![image](https://github.com/Lucaa8/Botiska/assets/47627900/d718754d-66f1-456f-baf4-0ad9847df2fb)
  ![image](https://github.com/Lucaa8/Botiska/assets/47627900/9e625968-064b-4746-b3e0-c03328a3b712)

  - `duplicates.message_id`: Same as `missing.message_id` but for the `#cartes-à-doubles` channel
