from aiogram import Router
from aiogram.types import Message
from lexicon.lexicon import LEXICON
from aiogram.fsm.state import default_state
from aiogram.filters import StateFilter

router: Router = Router()


# Этот хэндлер будет реагировать на любые сообщения пользователя,
# не предусмотренные логикой работы бота
@router.message(StateFilter(default_state))
async def send_echo(message: Message):
    await message.answer(LEXICON['other'])
