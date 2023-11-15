import logging as log
from datetime import datetime
from GameClient import GameClient

if __name__ == "__main__":
    logName = datetime.today().strftime('%Y_%m_%d_logging.log')
    log.basicConfig(level=log.INFO, filename=logName, filemode='w',
                    format='%(asctime)s::%(levelname)s >>> %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')
    log.info('Starting main game_client...')
    client = GameClient()
    client.start()
