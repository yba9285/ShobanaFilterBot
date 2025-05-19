#please give credits https://github.com/MN-BOTS
from pyrogram.enums import ParseMode
from pyrogram import Client, filters
from pyrogram.types import Message
from database.ia_filterdb import get_movies_grouped, get_series_grouped

@Client.on_message(filters.private & filters.command("movies"))
async def list_movies(bot: Client, message: Message):
    movies = await get_movies_grouped()
    if not movies:
        return await message.reply("❌ No recent movies found.")
    
    msg = "<b>🎬 Latest Movies:</b>\n\n"
    for title, qualities in movies.items():
        q_list = ", ".join(qualities)
        msg += f"✅ <b>{title}</b> - {q_list}\n"

    await message.reply(msg[:4096], parse_mode=ParseMode.HTML)

@Client.on_message(filters.private & filters.command("series"))
async def list_series(bot: Client, message: Message):
    series_data = await get_series_grouped()
    if not series_data:
        return await message.reply("❌ No recent series episodes found.")
    
    msg = "<b>📺 Latest Series:</b>\n\n"
    for title, episodes in series_data.items():
        ep_list = ", ".join(f"S{season}E{ep}" if season else f"E{ep}" for season, ep in episodes)
        msg += f"✅ <b>{title}</b> - {ep_list}\n"

    await message.reply(msg[:4096], parse_mode=ParseMode.HTML)
