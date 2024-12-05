from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import Message


class MessageFilter(BaseFilter):
    def __init__(self, message_text: Union[str, list]):
        self.message_text = message_text

    async def __call__(self, message: Message) -> bool:
        if isinstance(self.message_text, str):
            return message.text.split()[0] == self.message_text
        else:
            return message.text.split()[0] in self.message_text