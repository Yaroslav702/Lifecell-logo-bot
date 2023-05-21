import os
import logging

from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import moviepy.editor as mp
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands='start')
async def start_process(message: types.Message):
    await message.answer("Вітаю!\nНа зв'язку Lifecell😍\nНадсилай будь-яку гіфку - додамо туди своє лого.")


@dp.message_handler(content_types=types.ContentTypes.ANY)
async def get_user_git(message: types.Message):
    if message.content_type != 'animation':
        await message.answer('На жаль, я не умію працювати із таким форматом файлів🥲\nСпробуй надіслати мені <b>GIF</b>.', parse_mode='html')
    else:
        await message.animation.download(f'assets/{message.from_id}.mp4')
        await message.answer('Секундочку...')
        try:
            clip = mp.VideoFileClip(f'assets/{message.from_id}.mp4')
            logo = (mp.ImageClip("assets/logo_lifecell.jpg")
                        .set_duration(clip.duration)
                        .set_pos(("right","bottom"))
                        .resize(height=60)
                    )
            final = mp.CompositeVideoClip([clip, logo])
            final.write_videofile(f'assets/{message.from_id}.mp4')

            await bot.send_animation(message.from_id, open(f'assets/{message.from_id}.mp4', 'rb'))
        except Exception as err:
            logging.exception(err)
            await message.answer('Виникла непередбачувана помилка :(\nСпробуй, будь ласка, ще раз або звернись у підтримку марафону🚀')

        if os.path.exists(f'assets/{message.from_id}.mp4'):
            os.remove(f'assets/{message.from_id}.mp4')


if __name__ == '__main__':
    executor.start_polling(dp)