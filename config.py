from config_reader import config

TOKEN_API = config.bot_token.get_secret_value()

wellcome_text = """
Приветствую в боте для розыгрышей! (Исходный код части бота с розыгрышами - https://github.com/nicksttar/GiveAwayTgBot) 🎉

В нашем боте ты можешь создать розыгрыш! 🚀"""

about_text = """Нажми на кнопку Создать розыгрыш!"""

how_to_use_text = """Ты должен иметь права админа в группе!"""

mode = """Чтобы завершить розыгрыш, нажни Завершить под розыгрышем, чтобы участвовать - Участвую!"""

modes_list = [mode]

default_text = "Розыгрыш начат!"
