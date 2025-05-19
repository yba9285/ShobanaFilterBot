#please give credits https://github.com/MN-BOTS 
from pyrogram import Client, filters
from pyrogram.types import Message
from database.ia_filterdb import get_all_movie_names_grouped, get_all_series_grouped

@Client.on_message(filters.command("movies") & filters.private)
async def movies_list(bot, message: Message):
    movies = await get_all_movie_names_grouped()
    if not movies:
        return await message.reply("No movies found.")

    msg = "<b>🎬 Recently Added Movies:</b>\n\n"
    for name in movies:
        msg += f"• <code>{name}</code>\n"

    await message.reply(msg[:4096], parse_mode="html")

@Client.on_message(filters.command("series") & filters.private)
async def series_list(bot, message: Message):
    series_grouped = await get_all_series_grouped()
    if not series_grouped:
        return await message.reply("No series found.")

    msg = "<b>📺 Recently Added Series:</b>\n\n"
    for series, episodes in series_grouped.items():
        ep_list = ', '.join(str(e) for e in episodes)
        msg += f"• <code>{series} Ep {ep_list}</code>\n"

    await message.reply(msg[:4096], parse_mode="html")
  
