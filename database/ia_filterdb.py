import logging
from struct import pack
import re
import base64
from pyrogram.file_id import FileId
from pymongo.errors import DuplicateKeyError
from umongo import Instance, Document, fields
from motor.motor_asyncio import AsyncIOMotorClient
from marshmallow.exceptions import ValidationError
from info import DATABASE_URI, DATABASE_NAME, COLLECTION_NAME, USE_CAPTION_FILTER

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


client = AsyncIOMotorClient(DATABASE_URI)
db = client[DATABASE_NAME]
instance = Instance.from_db(db)

@instance.register
class Media(Document):
    file_id = fields.StrField(attribute='_id')
    file_ref = fields.StrField(allow_none=True)
    file_name = fields.StrField(required=True)
    file_size = fields.IntField(required=True)
    file_type = fields.StrField(allow_none=True)
    mime_type = fields.StrField(allow_none=True)
    caption = fields.StrField(allow_none=True)

    class Meta:
        indexes = ('$file_name', )
        collection_name = COLLECTION_NAME


async def save_file(media):
    """Save file in database"""

    # TODO: Find better way to get same file_id for same media to avoid duplicates
    file_id, file_ref = unpack_new_file_id(media.file_id)
    file_name = re.sub(r"(_|\-|\.|\+)", " ", str(media.file_name))
    try:
        file = Media(
            file_id=file_id,
            file_ref=file_ref,
            file_name=file_name,
            file_size=media.file_size,
            file_type=media.file_type,
            mime_type=media.mime_type,
            caption=media.caption.html if media.caption else None,
        )
    except ValidationError:
        logger.exception('Error occurred while saving file in database')
        return False, 2
    else:
        try:
            await file.commit()
        except DuplicateKeyError:      
            logger.warning(
                f'{getattr(media, "file_name", "NO_FILE")} is already saved in database'
            )

            return False, 0
        else:
            logger.info(f'{getattr(media, "file_name", "NO_FILE")} is saved to database')
            return True, 1



async def get_search_results(query, file_type=None, max_results=10, offset=0, filter=False):
    """For given query return (results, next_offset)"""

    query = query.strip()
    #if filter:
        #better ?
        #query = query.replace(' ', r'(\s|\.|\+|\-|_)')
        #raw_pattern = r'(\s|_|\-|\.|\+)' + query + r'(\s|_|\-|\.|\+)'
    if not query:
        raw_pattern = '.'
    elif ' ' not in query:
        raw_pattern = r'(\b|[\.\+\-_])' + query + r'(\b|[\.\+\-_])'
    else:
        raw_pattern = query.replace(' ', r'.*[\s\.\+\-_]')
    
    try:
        regex = re.compile(raw_pattern, flags=re.IGNORECASE)
    except:
        return []

    if USE_CAPTION_FILTER:
        filter = {'$or': [{'file_name': regex}, {'caption': regex}]}
    else:
        filter = {'file_name': regex}

    if file_type:
        filter['file_type'] = file_type

    total_results = await Media.count_documents(filter)
    next_offset = offset + max_results

    if next_offset > total_results:
        next_offset = ''

    cursor = Media.find(filter)
    # Sort by recent
    cursor.sort('$natural', -1)
    # Slice files according to offset and max results
    cursor.skip(offset).limit(max_results)
    # Get list of files
    files = await cursor.to_list(length=max_results)

    return files, next_offset, total_results



async def get_file_details(query):
    filter = {'file_id': query}
    cursor = Media.find(filter)
    filedetails = await cursor.to_list(length=1)
    return filedetails


def encode_file_id(s: bytes) -> str:
    r = b""
    n = 0

    for i in s + bytes([22]) + bytes([4]):
        if i == 0:
            n += 1
        else:
            if n:
                r += b"\x00" + bytes([n])
                n = 0

            r += bytes([i])

    return base64.urlsafe_b64encode(r).decode().rstrip("=")


def encode_file_ref(file_ref: bytes) -> str:
    return base64.urlsafe_b64encode(file_ref).decode().rstrip("=")


def unpack_new_file_id(new_file_id):
    """Return file_id, file_ref"""
    decoded = FileId.decode(new_file_id)
    file_id = encode_file_id(
        pack(
            "<iiqq",
            int(decoded.file_type),
            decoded.dc_id,
            decoded.media_id,
            decoded.access_hash
        )
    )
    file_ref = encode_file_ref(decoded.file_reference)
    return file_id, file_ref

import re
from collections import defaultdict

def clean_movie_title(name):
    # Remove brackets and extensions
    name = re.sub(r"\[.*?\]|\(.*?\)", "", name)
    name = re.sub(r"\.mkv|\.mp4|\.avi", "", name, flags=re.I)

    # Match up to the year (1900–2099)
    match = re.search(r"^(.*?\b(19|20)\d{2})\b", name)
    if match:
        title = match.group(1)
    else:
        title = name

    title = re.sub(r"\s+", " ", title)  # normalize whitespace
    return title.strip().title()

def extract_quality(name):
    match = re.search(r"\b(2160p|1080p|720p|480p|360p)\b", name, re.I)
    return match.group(1) if match else "Unknown"

def is_series_file(name):
    return bool(re.search(r"\b(s\d{1,2}e\d{1,2}|e\d{1,2}|season\s*\d+|episode\s*\d+)\b", name, re.I))

async def get_movie_list(limit=20):
    cursor = Media.find().sort("$natural", -1).limit(100)
    files = await cursor.to_list(length=100)
    results = []

    for file in files:
        name = getattr(file, "file_name", "")
        if not is_series_file(name):
            results.append(name)
        if len(results) >= limit:
            break
    return results

async def get_movies_grouped(limit=30):
    cursor = Media.find().sort("$natural", -1).limit(200)
    files = await cursor.to_list(length=200)
    grouped = defaultdict(set)

    for file in files:
        name = getattr(file, "file_name", "")
        if is_series_file(name):
            continue  # Skip series

        title = clean_movie_title(name)
        quality = extract_quality(name)
        grouped[title].add(quality)

    return {
        title: sorted(list(qualities), reverse=True)
        for title, qualities in grouped.items() if qualities
    }

def clean_series_title(name):
    name = re.sub(r"\[.*?\]|\(.*?\)", "", name)
    name = re.sub(r"\.mkv|\.mp4|\.avi", "", name, flags=re.I)
    name = name.lower()

    # Remove tags at beginning like s01e02, e12, ep23, s01
    name = re.sub(r"^(s\d{1,2}e\d{1,2}|e\d{1,2}|ep\d{1,2}|s\d{1,2})\s*", "", name, flags=re.I)

    # Remove extra tags (lang, quality)
    name = re.sub(r"\b(malayalam|tamil|hindi|telugu|english|720p|1080p|480p|x264|x265|web[-\. ]?dl|hdrip|brrip|bluray|dvdrip)\b", "", name, flags=re.I)
    name = re.sub(r"\s+", " ", name)
    return name.strip().title()

def extract_season_episode(name):
    name = name.lower()

    match = re.search(r"s(\d{1,2})e(\d{1,2})", name)
    if match:
        return int(match.group(1)), int(match.group(2))

    match = re.search(r"(?:ep|e)(\d{1,2})", name)
    if match:
        return None, int(match.group(1))

    match = re.search(r"s(\d{1,2})", name)
    if match:
        return int(match.group(1)), None

    return None, None

async def get_series_grouped(limit=30):
    cursor = Media.find().sort("$natural", -1).limit(200)
    files = await cursor.to_list(length=200)

    grouped = defaultdict(lambda: {"episodes": set(), "seasons": defaultdict(set)})

    for file in files:
        name = getattr(file, "file_name", "")
        season, episode = extract_season_episode(name)
        title = clean_series_title(name)

        if season and episode:
            grouped[title]["seasons"][season].add(episode)
        elif episode:
            grouped[title]["episodes"].add(episode)
        elif season:
            grouped[title]["seasons"][season]  # Just mark season

    result = {}

    for title, data in grouped.items():
        parts = []
        if data["episodes"]:
            ep_list = ", ".join(str(e) for e in sorted(data["episodes"]))
            parts.append(f"Episodes {ep_list}")

        for season, eps in sorted(data["seasons"].items()):
            if eps:
                ep_list = ", ".join(str(e) for e in sorted(eps))
                parts.append(f"Season {season} Episodes {ep_list}")
            else:
                parts.append(f"Season {season}")

        result[title] = parts[:5]  # Limit to 5 entries per title

    return result
