# please give credits https://github.com/MN-BOTS
from pyrogram.enums import ParseMode
from pyrogram import Client, filters
from pyrogram.types import Message
from database.ia_filterdb import get_movie_list, get_series_grouped, get_movies_grouped

@Client.on_message(filters.private & filters.command("movies"))
async def list_movies(bot: Client, message: Message):
    movies_data = await get_movies_grouped()
    if not movies_data:
        return await message.reply("❌ No recent movies found.")
    
    msg = "<b>🎬 Latest Movies:</b>\n\n"
    for title, qualities in movies_data.items():
        quality_str = ", ".join(qualities)
        msg += f"✅ <b>{title}</b> - {quality_str}\n"

    await message.reply(msg[:4096], parse_mode=ParseMode.HTML)

@Client.on_message(filters.private & filters.command("series"))
async def list_series(bot: Client, message: Message):
    series_data = await get_series_grouped()
    if not series_data:
        return await message.reply("❌ No recent series episodes found.")
    
    msg = "<b>📺 Latest Series:</b>\n\n"
    for title, parts in series_data.items():
        for p in parts:
            msg += f"✅ <b>{title}</b> - {p}\n"

    await message.reply(msg[:4096], parse_mode=ParseMode.HTML)
