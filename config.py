from config_reader import config

TOKEN_API = config.bot_token.get_secret_value()

wellcome_text = """
Приветствую в боте для розыгрышей! (Исходный код части бота с розыгрышами - https://github.com/nicksttar/GiveAwayTgBot) 🎉

В нашем боте ты можешь создать розыгрыш! 🚀"""

about_text = """The Giveaway Bot, created by @nicksttar using Aiogram 3, is a versatile and user-friendly tool designed for managing giveaways in Telegram groups. ⚙️

With a focus on simplicity and functionality, the bot offers two distinctive giveaway modes:

<b>Classic Giveaway Mode</b>: In this mode, users can participate in a traditional giveaway using photo description and so on.

<b>Random Generation Mode</b>: you just use to make fast random number in your objective."""

how_to_use_text = """Just tap into <b>Start Giveaway</b> button to see options and how it works.

❗You have to take bot administrators rights to have opportunity send some gives to group."""

mode1 = """<b>Classic Mode</b> ✅

A classic giveaway involves setting a list of the settings like:

Audience, participants, winners, duration, image and description.

Once the predetermined number of participants is reached or the giveaway host initiates the drawing, the giveaway process begins. 

Participants eagerly await the results as the system randomly selects a winner from the pool of entrants."""

mode2 = """<b>Generator Mode</b> 🎲

Generator Mode is a straightforward randomization feature that provides a random value within a specified range. 

This mode operates as a simple yet effective tool for generating unpredictable outcomes, making it useful in scenarios where randomness or chance is desired. 

Whether you need a random number for a game, simulation, or any other application, Generator Mode delivers by offering a seamless and effortless way to obtain diverse and unpredictable results within the defined numerical boundaries."""

modes_list = [mode1, mode2]

default_text = "It's new Giveaway!!!\nWait untill admin starts give!"
