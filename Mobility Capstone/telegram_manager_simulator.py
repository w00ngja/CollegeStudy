#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

import logging

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from pyevsim import SystemSimulator, BehaviorModelExecutor, SysMessage
from pyevsim.definition import *


from telegram_model import TelegramModel
from telegram_manager import TelegramManager

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


YOUR_TOKEN = "6076808748:AAF9c9YEEK1bHhig8bIIE4IQvYe6q-SDGmQ"
YOUR_CHAT_ID = -1

def main() -> None:
    tm = TelegramManager(YOUR_TOKEN,5906594124)

if __name__ == '__main__':
    main()