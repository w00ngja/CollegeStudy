# Packages
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler,MessageHandler, Filters, CallbackContext
from pyevsim import SystemSimulator, BehaviorModelExecutor, SysMessage
from pyevsim.definition import *
from telegram_model import TelegramModel

class TelegramManager:
    def __init__(self, token,chatid):
        self.updater = Updater(token)
# Get the dispatcher to register handlers
        dispatcher = self.updater.dispatcher
# on different commands - answer in Telegram
        dispatcher.add_handler(CommandHandler("start", self.start))
        dispatcher.add_handler(CommandHandler("stop", self.stop))
# Start the Bot
        self.updater.start_polling()
# initialize simulation engine
# System Simulator Initialization
        self.ss = SystemSimulator()
        self.ss.register_engine("simple", "REAL_TIME", 1)
        self.ss.get_engine("simple").insert_input_port("start")
        self.ss.get_engine("simple").insert_input_port("stop")

        tm = TelegramModel(0, Infinite, "TM", "simple", self.updater.bot, chatid)
        self.ss.get_engine("simple").register_entity(tm)
        self.ss.get_engine("simple").coupling_relation(None, "start", tm, "start")
        self.ss.get_engine("simple").coupling_relation(None, "stop", tm, "stop")
        self.ss.get_engine("simple").simulate()

    def start(self, update: Update, context: CallbackContext) -> None:
        self.ss.get_engine("simple").insert_external_event("start", "None")
    def stop(self, update: Update, context: CallbackContext) -> None:
        self.ss.get_engine("simple").insert_external_event("stop", "None")