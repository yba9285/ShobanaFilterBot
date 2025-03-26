from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import json
import os
import hashlib

# Dictionary to store MongoDB session URLs with unique short IDs
mongo_sessions = {}

# Dictionary to store transfer requests
transfer_requests = {}

@Client.on_message(filters.command("mongo") & filters.group)
async def mongo(client, message):
    try:
        # Check if the user is an admin or the chat owner
        user = await client.get_chat_member(message.chat.id, message.from_user.id)
        if user.status not in [enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR]:
            await message.reply_text("You don't have permission to use this command.")
            return
    except Exception as error:
        await message.reply_text(f"An error occurred. I may not have permission to check user status. {error}")
        return

    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.reply_text("Usage: /mongo {mongo_url}")
        return

    mongo_url = args[1].strip()

    # Generate a short unique ID for the MongoDB URL
    short_id = hashlib.md5(mongo_url.encode()).hexdigest()[:8]
    mongo_sessions[short_id] = mongo_url  # Store URL with short ID

    try:
        mongo_client = MongoClient(mongo_url, serverSelectionTimeoutMS=5000)
        mongo_client.server_info()
    except ConnectionFailure:
        await message.reply_text("Failed to connect to the MongoDB server. Please check your URL and try again.")
        return
    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")
        return

    db_names = mongo_client.list_database_names()
    if not db_names:
        await message.reply_text("No databases found on the server.")
        return

    db_name = db_names[0]  # Using the first database
    db = mongo_client[db_name]
    collections = db.list_collection_names()

    if not collections:
        await message.reply_text(f"No collections found in the database '{db_name}'.")
        return

    text = f"Database: {db_name}\nCollections:\n" + "\n".join(f" - {coll}" for coll in collections)

    keyboard = []
    for coll in collections:
        keyboard.append([
            InlineKeyboardButton("Download", callback_data=f"download|{db_name}|{coll}|{short_id}"),
            InlineKeyboardButton("Delete", callback_data=f"delete|{db_name}|{coll}|{short_id}"),
            InlineKeyboardButton("Transfer", callback_data=f"transfer|{db_name}|{coll}|{short_id}")
        ])

    # Bulk action buttons
    keyboard.append([
        InlineKeyboardButton("Download All", callback_data=f"bulk_download|{db_name}|{short_id}"),
        InlineKeyboardButton("Delete All", callback_data=f"bulk_delete|{db_name}|{short_id}"),
        InlineKeyboardButton("Transfer All", callback_data=f"bulk_transfer|{db_name}|{short_id}")
    ])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await message.reply_text(text, reply_markup=reply_markup)

@Client.on_callback_query(filters.regex(r"^(download|delete|transfer|bulk_download|bulk_delete|bulk_transfer)\|"))
async def handle_callback_query(client, query: CallbackQuery):
    data = query.data.split("|")
    action = data[0]
    db_name = data[1]
    coll_name = data[2] if len(data) > 2 else None
    short_id = data[-1]  # Retrieve the short ID

    # Get the full MongoDB URL from stored sessions
    mongo_url = mongo_sessions.get(short_id)
    if not mongo_url:
        await query.answer("MongoDB session expired. Please use /mongo again.", show_alert=True)
        return

    try:
        mongo_client = MongoClient(mongo_url, serverSelectionTimeoutMS=5000)
        mongo_client.server_info()
    except ConnectionFailure:
        await query.message.edit_text("Failed to connect to the MongoDB server. Please check the URL and try again.")
        return
    except Exception as e:
        await query.message.edit_text(f"An error occurred: {e}")
        return

    db = mongo_client[db_name]

    if action == "download" and coll_name:
        await download_collection(query, db, coll_name)
    elif action == "delete" and coll_name:
        await delete_collection(query, db, coll_name)
    elif action == "transfer" and coll_name:
        await initiate_transfer(query, db_name, coll_name, mongo_url)
    elif action == "bulk_download":
        await bulk_download_collections(query, db)
    elif action == "bulk_delete":
        await bulk_delete_collections(query, db)
    elif action == "bulk_transfer":
        await initiate_bulk_transfer(query, db_name, mongo_url)

async def download_collection(query, db, coll_name):
    collection = db[coll_name]
    documents = list(collection.find())
    if not documents:
        await query.answer(f"The collection '{coll_name}' is empty.", show_alert=True)
        return

    file_path = f"{coll_name}.json"
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(documents, file, default=str, indent=4)

    await query.message.reply_document(file_path)
    os.remove(file_path)
    await query.answer(f"Downloaded collection '{coll_name}'.")

async def delete_collection(query, db, coll_name):
    collection = db[coll_name]
    collection.drop()
    await query.answer(f"Deleted collection '{coll_name}'.")
    await query.message.edit_text(f"Collection '{coll_name}' has been deleted.")

async def initiate_transfer(query, db_name, coll_name, source_url):
    user_id = query.from_user.id
    transfer_requests[user_id] = {
        "source_url": source_url,
        "db_name": db_name,
        "coll_name": coll_name
    }
    await query.message.reply_text("Please send the target MongoDB URL to transfer the collection.")
    await query.answer()

async def bulk_download_collections(query, db):
    collections = db.list_collection_names()
    all_documents = {}

    for coll in collections:
        collection = db[coll]
        documents = list(collection.find())
        if documents:
            all_documents[coll] = documents

    if not all_documents:
        await query.answer("No documents found in any collection.", show_alert=True)
        return

    file_path = f"{db.name}_all_collections.json"
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(all_documents, file, default=str, indent=4)

    await query.message.reply_document(file_path)
    os.remove(file_path)
    await query.answer("Downloaded all collections.")

async def bulk_delete_collections(query, db):
    collections = db.list_collection_names()
    for coll in collections:
        collection = db[coll]
        collection.drop()
    await query.answer("Deleted all collections.")
    await query.message.edit_text("All collections have been deleted.")

async def initiate_bulk_transfer(query, db_name, source_url):
    user_id = query.from_user.id
    transfer_requests[user_id] = {
        "source_url": source_url
    }
    await query.message.reply_text("Please send the target MongoDB URL to transfer all collections.")
    await query.answer()
