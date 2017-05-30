from telepot.helper import ChatContext

from skybeard.beards import BeardChatHandler
from skybeard.decorators import onerror
from skybeard.utils import get_beard_config
from skybeard.bearddbtable import BeardInstanceDBTable

import random

CONFIG = get_beard_config()


class BeardedDuck(BeardChatHandler):

    __userhelp__ = """I am a duck for you to speak to."""

    __commands__ = [
        ("explain", 'explain', 'Gives the opportunity for you to explain yourself.'),
    ]

    _timeout = 10

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.explain_table = BeardInstanceDBTable(self, 'explain')

    @onerror()
    async def explain(self, msg):
        global _explain
        await _explain(self, msg)


async def _create_bot(beard_instance):
    bot = ChatContext(beard_instance.bot, beard_instance.chat_id)
    bot.listener.capture([{'chat': {'id': bot.chat_id}}])

    return bot


async def _explain(beard_instance, msg):
    # Get a bot
    bot = await _create_bot(beard_instance)

    await bot.sender.sendMessage("Explain yourself! Type 'I'm done.' to finish.")
    while True:
        resp = await bot.listener.wait()
        # TODO figure out how to store the responses in the self.explain_table
        # for regurgitation
        if 'I\'m done.' == resp['text']:
            await bot.sender.sendMessage("Happy to help :)")
            return
        else:
            await bot.sender.sendMessage(random.choice(CONFIG['agreement_phrases']))

