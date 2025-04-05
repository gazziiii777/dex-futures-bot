from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from app.bot.services import parse_crypto


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(text='sdfsdf!')



@router.message(Command("parse"))
async def parse(message: Message):
    zxc = await parse_crypto()
    print(zxc)
    await message.answer(text=f"{zxc}")
    