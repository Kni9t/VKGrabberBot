# VKGrabberBot v 1.4.0

# Introduction
This is a simple telegram bot that is used to transfer posts from the VK social network. The bot was written purely for my own needs, but I thought it might be useful to someone.

Briefly, this bot goes through the list of specified groups and copies the 5 latest publications from each of them to the specified channel in the telegram. The bot does this strictly every 30 minutes. Explanations, every time the time is a multiple of 30 minutes, the bot will start copying. For example, the bot will copy posts at 10:00, then at 10:30, then at 11:00, and so on throughout the day.

When transferring posts, the bot creates a special hash by which it understands which post has been moved and which has not yet been moved, so that the bot will not duplicate posts. However, if you edit a post in VK, the bot will transfer it as a new one, since it has no way to change the post in the telegram channel.

# Preparing for start
In order to use this bot, you need to follow several steps:
1) You need to create a bot in telegram. You can use this guide [here](https://core.telegram.org/bots/features#creating-a-new-bot). During the creation process, you will receive a bot token, do not lose it!
2) The next step is to create a telegram channel and grant administrator rights to your bot.
3) Next, you need to get the application's **Service app token** from VK. This is a somewhat confusing process, but remember that you need a **Service app token** (Сервисный токен приложения). You can read the guide to getting it [here](https://id.vk.com/about/business/go/docs/ru/vkid/latest/vk-id/connection/tokens/about).
4) The last step is to clone the repository and add all previously obtained keys to the parameters. The following section of the readme is dedicated to this.
# How to set up a bot
You can use the file requirements.txt to install all necessary dependencies. I used **Python 3.12.0** and **pip 25.0.1** for this project, but I didn't run any tests for earlier versions of Python. But I think everything will be fine.

To install dependencies, go to the project's cluster directory and run the command below:
```cmd
pip install -r requirements.txt
```

Just in case, I used the following Python libraries:
1) [py-vkontakte](https://pypi.org/project/py-vkontakte/)
2) [pyTelegramBotAPI](https://pypi.org/project/pyTelegramBotAPI/)
3) [requests](https://pypi.org/project/requests/)
4) [vk](https://pypi.org/project/vk/)

Let's move on to configuring the files with the parameters. This project uses two files with settings: **parameters.json** and **group_list.json**. They are both stored in the '**params**' directory.

The **group_list file.json** contains a list of strings, each of which is the ID of the VK group from which posts should be taken. An example of filling in the file is given below:
```json
[
    "VK_group_ID1",
    "VK_group_ID2",
]
```

The **parameters file.json** contains all the tokens and keys used to connect to the API. You need to change the following values, separated by the ":" symbol for the following parameters:
1) "botKey" - Here you need the key of your telegram bot, which you received when creating it in **paragraph 1** in the chapter **Preparing for start**.
2) "VKToken"  - Here you need to specify your **Service app token**, obtained from **paragraph 3** of chapter **Preparing for start**. **It is important that the token is required in its full form, along with the version value at the end (for example &v=5.199)**
3) "channelUsername"  - Here you just specify your @id_telegram_channel

The **hashFileName**, **groupListFileName** and **adminID** parameters only indicate the path to files with a hash of already sent posts and a file with a list of VK groups. They do not need to be changed

Example of settings **parameters file.the json** is shown below:
```json
{
    "botKey": "00000000:ADADAADGGEVEEVEVEVEEV",
    "VKToken": "we8er58bn5feb5wv2wdc8qdq9w9sdqdqd95q9w59g29bt9j9y9r&v=5.199",
    "channelUsername": "@someTelegramChannelID",
    "hashFileName": "params/sent_posts.json",
    "groupListFileName": "params/group_list.json"
}
```

# How to start a bot
To launch the bot, simply run the following command:
```cmd
python main.py
```
During the work, the bot will create a file with a log, which will be located in the same name directory - **logs**.
Files like: **Running_logs-<datetime_now>.log** are created there. In them, you can learn more about what the bot is doing. Also, critical errors will be duplicated in the shell where the bot is running.

By default, the bot checks the last 5 posts for all specified groups in the **group_list file.json** every 30 minutes for an hour. (For example, the bot will check posts at 12:00, then at 12:30, and then at 13:00, and so on). So far, these settings cannot be changed.

It is important that the bot does not have a stop button, so disable it via ^C (Ctrl + C or any other way)