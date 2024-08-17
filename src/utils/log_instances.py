from src.utils.logger import CustomLogger


bot_logger: CustomLogger = CustomLogger.get_logger("bot")
game_logger: CustomLogger = CustomLogger.get_logger("game")
player_logger: CustomLogger = CustomLogger.get_logger("player")
gameboard_logger: CustomLogger = CustomLogger.get_logger("gameboard")
ray_logger: CustomLogger = CustomLogger.get_logger("ray")
gameloop_logger: CustomLogger = CustomLogger.get_logger("gameloop")
atom_logger: CustomLogger = CustomLogger.get_logger("atom")
