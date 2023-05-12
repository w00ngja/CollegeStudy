# Packages
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler,MessageHandler, Filters, CallbackContext
from pyevsim import SystemSimulator, BehaviorModelExecutor, SysMessage
from pyevsim.definition import *
import datetime

class TelegramModel(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name, bot, chatid):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        self.init_state("Wait")
        self.insert_state("Wait", Infinite)
        self.insert_state("Generate", 2)
        self.insert_input_port("start")
        self.insert_input_port("stop")

        self.telegram_bot = bot
        self.chatid = chatid
    def ext_trans(self,port, msg):
        if port == "start":
            print(f"[Gen][IN][START]: {datetime.datetime.now()}")
            self._cur_state = "Generate"
        if port == "stop":
            print(f"[Gen][IN][STOP]: {datetime.datetime.now()}")
            self._cur_state = "Wait"
    def output(self):
        msg = None
        self.telegram_bot.send_message(self.chatid,f"[Gen][OUT]: {datetime.datetime.now()}")
        return msg
    def int_trans(self):
        if self._cur_state == "Generate":
            self._cur_state = "Generate"