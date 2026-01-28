import os
import re
import sys
import m3u8
import json
import time
import pytz
import asyncio
import requests
import subprocess
import urllib
import urllib.parse
import yt_dlp
import tgcrypto
import cloudscraper
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64encode, b64decode
from logs import logging
from bs4 import BeautifulSoup
import gadhvi as helper
from utils import progress_bar
from vars import API_ID, API_HASH, BOT_TOKEN
from aiohttp import ClientSession
from subprocess import getstatusoutput
from pytube import YouTube
from aiohttp import web
import random
from pyromod import listen
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import aiohttp
import aiofiles
import zipfile
import shutil
import ffmpeg
import database
from config import ADMIN_IDS

# Define admin IDs
ADMIN_IDS = [7793257011]  # Add your admin IDs here

# Helper function to decrypt files
def decrypt_file_txt(file_path: str) -> str:
    """Decrypt helper txt files if needed"""
    try:
        # Add your decryption logic here if needed
        return file_path
    except Exception as e:
        print(f"Decryption error: {e}")
        return file_path

# Initialize the bot
bot = Client(
    "botxgadhvi",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

cookies_file_path = os.getenv("cookies_file_path", "youtube_cookies.txt")
api_url = "http://master-api-v3.vercel.app/"
api_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNzkxOTMzNDE5NSIsInRnX3VzZXJuYW1lIjoi4p61IFtvZmZsaW5lXSIsImlhdCI6MTczODY5MjA3N30.SXzZ1MZcvMp5sGESj0hBKSghhxJ3k1GTWoBUbivUe1I"
token_cp ='eyJjb3Vyc2VJZCI6IjQ1NjY4NyIsInR1dG9ySWQiOm51bGwsIm9yZ0lkIjo0ODA2MTksImNhdGVnb3J5SWQiOm51bGx9r'
adda_token = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJkcGthNTQ3MEBnbWFpbC5jb20iLCJhdWQiOiIxNzg2OTYwNSIsImlhdCI6MTc0NDk0NDQ2NCwiaXNzIjoiYWRkYTI0Ny5jb20iLCJuYW1lIjoiZHBrYSIsImVtYWlsIjoiZHBrYTU0NzBAZ21haWwuY29tIiwicGhvbmUiOiI3MzUyNDA0MTc2IiwidXNlcklkIjoiYWRkYS52MS41NzMyNmRmODVkZDkxZDRiNDkxN2FiZDExN2IwN2ZjOCIsImxvZ2luQXBpVmVyc2lvbiI6MX0.0QOuYFMkCEdVmwMVIPeETa6Kxr70zEslWOIAfC_ylhbku76nDcaBoNVvqN4HivWNwlyT0jkUKjWxZ8AbdorMLg"
photologo = 'https://files.catbox.moe/1w7a78.jpg' #https://envs.sh/GV0.jpg
photoyt = 'https://tinypic.host/images/2025/03/18/YouTube-Logo.wine.png' #https://envs.sh/GVi.jpg
photocp = 'https://tinypic.host/images/2025/03/28/IMG_20250328_133126.jpg'
photozip = 'https://envs.sh/cD_.jpg'

async def show_random_emojis(message):
    emojis = ['🐼', '🐶', '🐅', '⚡️', '🚀', '✨', '💥', '☠️', '🥂', '🍾', '📬', '👻', '👀', '🌹', '💀', '🐇', '⏳', '🔮', '🦔', '📖', '🦁', '🐱', '🐻‍❄️', '☁️', '🚹', '🚺', '🐠', '🦋']
    emoji_message = await message.reply_text(' '.join(random.choices(emojis, k=1)))
    return emoji_message

# Inline keyboard for start command
BUTTONSCONTACT = InlineKeyboardMarkup([[InlineKeyboardButton(text="👨‍💻 Owner", url="https://t.me/mrfrontman001")]])
keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="⌯ FʀᴏɴᴛMᴀɴ | ×͜× |", url="https://t.me/Mrfrontman001"),
        ],
        [
            InlineKeyboardButton(text="🪔", callback_data="help_command"),
            InlineKeyboardButton(text="🦋", callback_data="featuress"),
        ],
    ]
)

async def show_loading_animation(message):
    # Simplified loading animation frames
    loading_frames = [
        "╭──────────────╮\n│ ⬢ □ □ □ □ │\n╰──────────────╯",
        "╭──────────────╮\n│ ⬢ ⬢ □ □ □ │\n╰──────────────╯",
        "╭──────────────╮\n│ ⬢ ⬢ ⬢ □ □ │\n╰──────────────╯",
        "╭──────────────╮\n│ ⬢ ⬢ ⬢ ⬢ □ │\n╰──────────────╯",
        "╭──────────────╮\n│ ⬢ ⬢ ⬢ ⬢ ⬢ │\n╰──────────────╯"
    ]
    
    loading_text = "𝐋𝐨𝐚𝐝𝐢𝐧𝐠..."
    loading_msg = await message.reply_text("╭──────────────╮\n│ □ □ □ □ □ │\n╰──────────────╯")
    
    for frame in loading_frames:
        await loading_msg.edit_text(
            f"{frame}\n"
            f"┣⪼ {loading_text}"
        )
        await asyncio.sleep(0.2)
    
    await loading_msg.delete()

@bot.on_message(filters.command("cookies") & filters.private)
async def cookies_handler(client: Client, m: Message):
    await m.reply_text(
        "Please upload the cookies file (.txt format).",
        quote=True
    )

    try:
        # Wait for the user to send the cookies file
        input_message: Message = await client.listen(m.chat.id)

        # Validate the uploaded file
        if not input_message.document or not input_message.document.file_name.endswith(".txt"):
            await m.reply_text("Invalid file type. Please upload a .txt file.")
            return

        # Download the cookies file
        downloaded_path = await input_message.download()

        # Read the content of the uploaded file
        with open(downloaded_path, "r") as uploaded_file:
            cookies_content = uploaded_file.read()

        # Replace the content of the target cookies file
        with open(cookies_file_path, "w") as target_file:
            target_file.write(cookies_content)

        await input_message.reply_text(
            "✅ Cookies updated successfully.\n📂 Saved in `youtube_cookies.txt`."
        )

    except Exception as e:
        await m.reply_text(f"⚠️ An error occurred: {str(e)}")

@bot.on_message(filters.command(["t2t"]))
async def text_to_txt(client, message: Message):
    user_id = str(message.from_user.id)
    # Inform the user to send the text data and its desired file name
    editable = await message.reply_text(f"<blockquote>Welcome to the Text to .txt Converter!\nSend the **text** for convert into a `.txt` file.</blockquote>")
    input_message: Message = await bot.listen(message.chat.id)
    if not input_message.text:
        await message.reply_text("🚨 **error**: Send valid text data")
        return

    text_data = input_message.text.strip()
    await input_message.delete()  # Corrected here
    
    await editable.edit("**🔄 Send file name or send /d for filename**")
    inputn: Message = await bot.listen(message.chat.id)
    raw_textn = inputn.text
    await inputn.delete()  # Corrected here
    await editable.delete()

    if raw_textn == '/d':
        custom_file_name = 'txt_file'
    else:
        custom_file_name = raw_textn

    txt_file = os.path.join("downloads", f'{custom_file_name}.txt')
    os.makedirs(os.path.dirname(txt_file), exist_ok=True)  # Ensure the directory exists
    with open(txt_file, 'w') as f:
        f.write(text_data)
        
    await message.reply_document(document=txt_file, caption=f"`{custom_file_name}.txt`\n\nYou can now download your content! 📥")
    os.remove(txt_file)

# Define paths for uploaded file and processed file
UPLOAD_FOLDER = '/path/to/upload/folder'
EDITED_FILE_PATH = '/path/to/save/edited_output.txt'

@bot.on_message(filters.command(["y2t"]))
async def youtube_to_txt(client, message: Message):
    user_id = str(message.from_user.id)
    
    editable = await message.reply_text(
        f"Send YouTube Website/Playlist link for convert in .txt file"
    )

    input_message: Message = await bot.listen(message.chat.id)
    youtube_link = input_message.text.strip()
    await input_message.delete(True)
    await editable.delete(True)

    # Fetch the YouTube information using yt-dlp with cookies
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'skip_download': True,
        'force_generic_extractor': True,
        'forcejson': True,
        'cookies': 'youtube_cookies.txt'  # Specify the cookies file
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            result = ydl.extract_info(youtube_link, download=False)
            if 'entries' in result:
                title = result.get('title', 'youtube_playlist')
            else:
                title = result.get('title', 'youtube_video')
        except yt_dlp.utils.DownloadError as e:
            await message.reply_text(
                f"<pre><code>🚨 Error occurred {str(e)}</code></pre>"
            )
            return

    # Extract the YouTube links
    videos = []
    if 'entries' in result:
        for entry in result['entries']:
            video_title = entry.get('title', 'No title')
            url = entry['url']
            videos.append(f"{video_title}: {url}")
    else:
        video_title = result.get('title', 'No title')
        url = result['url']
        videos.append(f"{video_title}: {url}")

    # Create and save the .txt file with the custom name
    txt_file = os.path.join("downloads", f'{title}.txt')
    os.makedirs(os.path.dirname(txt_file), exist_ok=True)  # Ensure the directory exists
    with open(txt_file, 'w') as f:
        f.write('\n'.join(videos))

    # Send the generated text file to the user with a pretty caption
    await message.reply_document(
        document=txt_file,
        caption=f'<a href="{youtube_link}">__**Click Here to Open Link**__</a>\n<pre><code>{title}.txt</code></pre>\n'
    )

    # Remove the temporary text file after sending
    os.remove(txt_file)


m_file_path= "main.py"
@bot.on_message(filters.command("getcookies") & filters.private)
async def getcookies_handler(client: Client, m: Message):
    try:
        # Send the cookies file to the user
        await client.send_document(
            chat_id=m.chat.id,
            document=cookies_file_path,
            caption="Here is the `youtube_cookies.txt` file."
        )
    except Exception as e:
        await m.reply_text(f"⚠️ An error occurred: {str(e)}")     
@bot.on_message(filters.command("mfile") & filters.private)
async def getcookies_handler(client: Client, m: Message):
    try:
        await client.send_document(
            chat_id=m.chat.id,
            document=m_file_path,
            caption="Here is the `main.py` file."
        )
    except Exception as e:
        await m.reply_text(f"⚠️ An error occurred: {str(e)}")

@bot.on_message(filters.command(["stop"]) )
async def restart_handler(_, m):
    await m.reply_text("𝑺𝑻𝑶𝑷𝑷𝑬𝑫 😒", True)
    os.execl(sys.executable, sys.executable, *sys.argv)
        
async def get_random_waifu_image():
    """Get a random waifu image from the API"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.waifu.pics/sfw/wafu") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get("url")
    except Exception as e:
        print(f"Error fetching waifu image: {e}")
        return None
        
@bot.on_callback_query(filters.regex("help_command"))
async def help_button(client, callback_query):
    # Chhota alert message
    await callback_query.answer(
        "➜ ꜱᴇɴᴅ ᴍᴇ /ᴅʀᴍ ғɪʀꜱᴛ\n➜ ꜱᴇɴᴅ ᴍᴇ .ᴛxᴛ ꜰɪʟᴇ \n➜ ᴄʜᴏᴏꜱᴇ Qᴜᴀʟɪᴛʏ & ᴇɴᴊᴏʏ!",
        show_alert=True
    )


@bot.on_callback_query(filters.regex("featuress"))
async def features_button(client, callback_query):
    # Bot DRM Services
    await callback_query.answer(
        "╭━━━━━━━✦✧✦━━━━━━━╮\n   🔻 sᴇʀᴠɪᴄᴇ mᴇɴᴜ: 🔻\n\n ➥  📚 ᴀᴘᴘx ᴢɪᴘ v1, (v2 ᴘᴅғ)\n ➥  🎓 ᴄʟᴀssᴘʟᴜs dʀᴍ + nᴅʀᴍ\n ➥  🧑‍🏫 ᴘʜʏsɪᴄsᴡᴀʟʟᴀʜ (ᴘᴀᴜsᴇᴅ)\n ➥  📚 ᴄᴀʀᴇᴇʀᴡɪʟʟ + ᴘᴅғ\n ➥  🗞️ ᴋʜᴀɴ ɢs\n ➥  🎓 sᴛᴜᴅʏ ɪQ dʀᴍ\n ➥  🚀 ᴀᴘᴘx + ᴀᴘᴘx dᴇᴄ ᴘᴅғ\n ➥  📚 vɪᴍᴇᴏ ᴘʀᴏᴛᴇᴄᴛɪᴏɴ\n ➥  📙 bʀɪɢʜtcᴏvᴇ ᴘʀᴏᴛᴇᴄᴛɪᴏɴ\n ➥  🗞️ vɪsɪᴏɴɪᴀs ᴘʀᴏᴛᴇᴄᴛɪᴏɴ\n ➥  📝 ᴢᴏᴏᴍ vɪᴅᴇᴏ\n ➥  📙 ᴀʟʟ nᴏɴ dʀᴍ + dᴇᴄ dʀᴍ\n╰────────⊰◆⊱────────╯",
        show_alert=True
    )


@bot.on_message(filters.command(["start"]))
async def start_command(bot: Client, message: Message):
    # Show loading animation first
    await show_loading_animation(message)
    
    # Get random waifu image
    image_url = await get_random_waifu_image()
    if not image_url:
        image_url = photologo
    
    caption = (
    f"╭━━━━━━━━━━━━━━━━━━━╮\n"
    f"┃ ✨ ʜᴇʏ {message.from_user.mention} ❤️\n"
    f"┃ 🦎 ɪ'ᴍ ʏᴏᴜʀ ᴅʀᴍ ᴡɪᴢᴀʀᴅ!\n"
    f"╰━━━━━━━━━━━━━━━━━━━━╯\n\n"
    f"<blockquote expandable>💎 **ꜰᴇᴀᴛᴜʀᴇꜱ ʏᴏᴜ'ʟʟ ʟᴏᴠᴇ:\n\n ➜ 🔓 • ᴀᴜᴛᴏ ᴅʀᴍ ᴅᴇᴄʀʏᴘᴛɪᴏɴ\n ➜ ⚡ • ᴘʀᴇᴍɪᴜᴍ Qᴜᴀʟɪᴛʏ\n ➜ 📚 • ʙᴀᴛᴄʜ ꜱᴜᴘᴘᴏʀᴛ\n ➜ 🚀 • ᴜʟᴛʀᴀ-ꜰᴀꜱᴛ ꜱᴘᴇᴇᴅ**</blockquote> "
    f" **💰 ₹400 / Week** for Personal Downloader\n\n"
)

    
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=image_url,
        caption=caption,
        reply_markup=keyboard
    )

@bot.on_message(filters.command(["id"]))
async def id_command(client, message: Message):
    chat_id = message.chat.id
    await message.reply_text(f"<blockquote>The ID of this chat id is:</blockquote>\n`{chat_id}`")

@bot.on_message(filters.private & filters.command(["info"]))
async def info(bot: Client, update: Message):
    
    text = (
        f"╭────────────────╮\n"
        f"│✨ **__Your Telegram Info__**✨ \n"
        f"├────────────────\n"
        f"├🔹**Name :** `{update.from_user.first_name} {update.from_user.last_name if update.from_user.last_name else 'None'}`\n"
        f"├🔹**User ID :** @{update.from_user.username}\n"
        f"├🔹**TG ID :** `{update.from_user.id}`\n"
        f"├🔹**Profile :** {update.from_user.mention}\n"
        "╰────────────────╯"
    )
    
    await update.reply_text(        
        text=text,
        disable_web_page_preview=True,
        reply_markup=BUTTONSCONTACT
    )

@bot.on_message(filters.command(["helper"]))
async def txt_handler(client: Client, m: Message):
    await bot.send_message(m.chat.id, text=(
    f"**╭─────────⊰◆⊱─────────╮**\n" 
    f" ➥ /start – **ʙᴏᴛ ꜱᴛᴀᴛᴜꜱ ᴄʜᴇᴄᴋ**\n"
    f" ➥ /drm – **ᴇxᴛʀᴀᴄᴛ ꜰʀᴏᴍ .ᴛxᴛ (ᴀᴜᴛᴏ)**\n"
    f" ➥ /y2t – **ʏᴏᴜᴛᴜʙᴇ → .ᴛxᴛ ᴄᴏɴᴠᴇʀᴛᴇʀ**\n"  
    f" ➥ /t2t – **ᴛᴇxᴛ → .ᴛxᴛ ɢᴇɴᴇʀᴀᴛᴏʀ**\n" 
    f" ➥ /stop – **ᴄᴀɴᴄᴇʟ ʀᴜɴɴɪɴɢ ᴛᴀꜱᴋ**\n"
    f" ➥ /id – **ɢᴇᴛ ᴄʜᴀᴛ/ᴜꜱᴇʀ ɪᴅ**\n"  
    f" ➥ /info – **ᴜꜱᴇʀ ᴅᴇᴛᴀɪʟꜱ**\n"  
    f" ➥ /logs – **ᴠɪᴇᴡ ʙᴏᴛ ᴀᴄᴛɪᴠɪᴛʏ**\n"
    f" ➥ /add_chat <chat_id> – **ᴀᴅᴅ ᴄʜᴀɴɴᴇʟ/ɢʀᴏᴜᴘ**\n"
    f" ➥ /remove_chat <chat_id> – **ʀᴇᴍᴏᴠᴇ ᴄʜᴀᴛ**\n"
    f" ➥ /list_chats – **ʟɪꜱᴛ ʏᴏᴜʀ ᴄʜᴀᴛꜱ**\n"
    f" ➥ /myplan <user_id> – **ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴘʟᴀɴ ᴅᴇᴛᴀɪʟꜱ**\n"
    f"**╰─────────⊰◆⊱─────────╯**\n"
    )
    )


@bot.on_message(filters.command(["logs"]))
async def send_logs(client: Client, m: Message):  # Correct parameter name
    try:
        with open("logs.txt", "rb") as file:
            sent = await m.reply_text("**📤 Sending you ....**")
            await m.reply_document(document=file)
            await sent.delete()
    except Exception as e:
        await m.reply_text(f"Error sending logs: {e}")

async def check_subscription(message):
    """Show subscription checking animation and verify user's access"""
    loading_frames = [
        "╭──────────────╮\n│ ⬢ □ □ □ □ │\n╰──────────────╯",
        "╭──────────────╮\n│ ⬢ ⬢ □ □ □ │\n╰──────────────╯",
        "╭──────────────╮\n│ ⬢ ⬢ ⬢ □ □ │\n╰──────────────╯",
        "╭──────────────╮\n│ ⬢ ⬢ ⬢ ⬢ □ │\n╰──────────────╯",
        "╭──────────────╮\n│ ⬢ ⬢ ⬢ ⬢ ⬢ │\n╰──────────────╯"
    ]
    
    msg = await message.reply_text(
        "╭──────────────╮\n│ □ □ □ □ □ │\n╰──────────────╯\n"
        "┣⪼ 𝐂𝐡𝐞𝐜𝐤𝐢𝐧𝐠 𝐒𝐮𝐛𝐬𝐜𝐫𝐢𝐩𝐭𝐢𝐨𝐧..."
    )
    
    for frame in loading_frames:
        await msg.edit_text(
            f"{frame}\n"
            f"┣⪼ 𝐂𝐡𝐞𝐜𝐤𝐢𝐧𝐠 𝐒𝐮𝐛𝐬𝐜𝐫𝐢𝐩𝐭𝐢𝐨𝐧..."
        )
        await asyncio.sleep(0.2)
    
    try:
        # Check if message is from a user
        if message.from_user:
            # First check if user is admin
            if message.from_user.id in ADMIN_IDS:
                await msg.delete()
                return True

            # Check user authorization
            is_auth = await database.is_user_authorized(message.from_user.id)
            logging.info(f"Authorization check for user {message.from_user.id}: {is_auth}")
            
            if is_auth:
                await msg.delete()
                return True
                
            # If not authorized, get subscription status for detailed message
            status = await database.get_subscription_status(message.from_user.id)
            await msg.delete()
            
            if not status["is_subscribed"]:
                await message.reply_text(
                    "╭━━━━━━━━━━━━━━━━━╮\n"
                    "┣⪼ ❌ 𝐍𝐨𝐭 𝐒𝐮𝐛𝐬𝐜𝐫𝐢𝐛𝐞𝐝\n"
                    "╰━━━━━━━━━━━━━━━━━╯\n\n"
                    "╭─────────────────\n"
                    "┣⪼ **📌 𝐏𝐥𝐞𝐚𝐬𝐞 𝐜𝐨𝐧𝐭𝐚𝐜𝐭**\n"
                    "┣⪼ **👤 @MrFrontMan001**\n"
                    "┣⪼ **💫 𝐅𝐨𝐫 𝐒𝐮𝐛𝐬𝐜𝐫𝐢𝐩𝐭𝐢𝐨𝐧**\n"
                    "╰─────────────────"
                )
                return False
        else:
            # If no user, then it's a channel message
            chat_id = message.chat.id
            logging.info(f"Checking authorization for channel {chat_id}")
            
            # Check if the chat is authorized
            is_chat_auth = await database.is_chat_authorized(chat_id)
            logging.info(f"Channel {chat_id} authorization status: {is_chat_auth}")
            
            if is_chat_auth:
                await msg.delete()
                return True
            else:
                await msg.delete()
                await message.reply_text(
                    "╭━━━━━━━━━━━━━━━━━╮\n"
                    "┣⪼ ❌ 𝐔𝐧𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝 𝐂𝐡𝐚𝐭\n"
                    "╰━━━━━━━━━━━━━━━━━╯\n\n"
                    "╭─────────────────\n"
                    "┣⪼ **📌 𝐏𝐥𝐞𝐚𝐬𝐞 𝐜𝐨𝐧𝐭𝐚𝐜𝐭**\n"
                    "┣⪼ **👤 @MrFrontMan001**\n"
                    "┣⪼ **💫 𝐅𝐨𝐫 𝐀𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐚𝐭𝐢𝐨𝐧**\n"
                    "╰─────────────────"
                )
                return False
            
    except Exception as e:
        logging.error(f"Error in check_subscription: {e}")
        await msg.delete()
        await message.reply_text(
            "╭━━━━━━━━━━━━━━━━━╮\n"
            "┣⪼ ⚠️ 𝐄𝐫𝐫𝐨𝐫 𝐜𝐡𝐞𝐜𝐤𝐢𝐧𝐠 𝐬𝐮𝐛𝐬𝐜𝐫𝐢𝐩𝐭𝐢𝐨𝐧\n"
            "╰━━━━━━━━━━━━━━━━━╯\n\n"
            "╭─────────────────\n"
            "┣⪼ **📌 𝐏𝐥𝐞𝐚𝐬𝐞 𝐜𝐨𝐧𝐭𝐚𝐜𝐭**\n"
            "┣⪼ **👤 @MrFrontMan001**\n"
            "┣⪼ **💫 𝐅𝐨𝐫 𝐬𝐮𝐩𝐩𝐨𝐫𝐭**\n"
            "╰─────────────────"
        )
        return False

@bot.on_message(filters.command(["drm"]))
async def txt_handler(bot: Client, m: Message):
    # First check subscription
    if not await check_subscription(m):
        return
        
    editable = await m.reply_text(
    "╭━〔 📬 𝗗𝗥𝗠 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱𝗲𝗿 〕━╮\n"
    "┃\n"
    "┃ ⪼ 📤 **sᴇɴᴅ ʏᴏᴜʀ ᴛᴇxᴛ ꜰɪʟᴇ**\n"
    "┃ ⪼ 📝 **ɪ'ʟʟ ᴘʀᴏᴄᴇꜱꜱ ɪᴛ ꜰᴏʀ ʏᴏᴜ**\n"
    "╰━━━━━━━━━━━━━━━━━━━━╯"
)

    
    try:
        input_message = await bot.listen(editable.chat.id)
        
        if not input_message.document or not input_message.document.file_name.endswith('.txt'):
            await editable.edit("🔹Please send a valid .txt file.")
            return
            
        y = await input_message.download()
        await input_message.delete(True)
        
        file_name, ext = os.path.splitext(os.path.basename(y))  # Extract filename & extension

        if file_name.endswith("_helper"):  # ✅ Check if filename ends with "_helper"
            x = decrypt_file_txt(y)  # Decrypt the file
        else:
            x = y 

        path = f"./downloads/{m.chat.id}"
        
        try:    
            with open(x, "r", encoding='utf-8') as f:
                content = f.read()
            content = content.split("\n")
            
            links = []
            for i in content:
                if i.strip():  # Skip empty lines
                    if "://" in i:
                        url = i.split("://", 1)[1]
                        links.append(i.split("://", 1))
            
            if not links:
                await editable.edit("🔹No valid links found in the text file.")
                os.remove(x)
                return
                    
            pdf_count = sum(1 for link in links if ".pdf" in link[1].lower())
            img_count = sum(1 for link in links if any(ext in link[1].lower() for ext in [".jpg", ".jpeg", ".png"]))
            zip_count = sum(1 for link in links if ".zip" in link[1].lower())
            other_count = len(links) - (pdf_count + img_count + zip_count)    
            
            await editable.edit(
    f"╭───『 🔍 𝐋𝐈𝐍𝐊𝐒 𝐃𝐄𝐓𝐄𝐂𝐓𝐄𝐃 』───╮\n"
    f"│ 🔗 **ᴛᴏᴛᴀʟ ʟɪɴᴋs ꜰᴏᴜɴᴅ**: {len(links)}\n\n"
    f"│ 🖼️ **ɪᴍᴀɢᴇs** : {img_count}\n"
    f"│ 📄 **ᴘᴅꜰs**    : {pdf_count}\n"
    f"│ 🗜️ **ᴢɪᴘs**    : {zip_count}\n"
    f"│ 📁 **ᴏᴛʜᴇʀs** : {other_count}\n\n"
    f"╰➤ **sᴇɴᴅ ᴛʜᴇ sᴛᴀʀᴛɪɴɢ ɴᴜᴍʙᴇʀ ᴛᴏ ʙᴇɢɪɴ ᴅᴏᴡɴʟᴏᴀᴅ.**"
)

            
        except Exception as e:
            await editable.edit(f"<pre><code>🔹Error reading file: {str(e)}</code></pre>")
            if os.path.exists(x):
                os.remove(x)
            return
            
    except Exception as e:
        await editable.edit(f"<pre><code>🔹Error processing file: {str(e)}</code></pre>")
        return

    # Rest of your code continues here...
    input0: Message = await bot.listen(editable.chat.id)
    raw_text = input0.text
    await input0.delete(True)
           
    await editable.edit(
    "╭───〔 🔹 ʙᴀᴛᴄʜ sᴇᴛᴜᴘ 〕───╮\n"
    "│ 🔹 ᴇɴᴛᴇʀ ʏᴏᴜʀ ʙᴀᴛᴄʜ ɴᴀᴍᴇ\n"
    "│ 🔹 sᴇɴᴅ `1` ᴛᴏ ᴜsᴇ ᴅᴇꜰᴀᴜʟᴛ\n"
    "╰──────────╯"
)
    input1: Message = await bot.listen(editable.chat.id)
    raw_text0 = input1.text
    await input1.delete(True)
    if raw_text0 == '1':
        b_name = file_name.replace('_', ' ')
    else:
        b_name = raw_text0

    await editable.edit(
    "**╭━━━『 💿 Choose Your Resolution 』━━━╮**\n"
    "**┃ 🔻**  `144`  \n"
    "**┃ 🔻**  `240`  \n"
    "**┃ 🔻**  `360`  \n"
    "**┃ 🔻**  `480`  \n"
    "**┃ 🔻**  `720`  \n"
    "**┃ 🔻** `1080`  \n"
    "**╰━━━⌈ 🤖 By 🂾 ⌯ FʀᴏɴᴛMᴀɴ ⌋━━━╯**"
)

    input2: Message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text
    quality = f"{raw_text2}p"
    await input2.delete(True)
    try:
        if raw_text2 == "144":
            res = "256x144"
        elif raw_text2 == "240":
            res = "426x240"
        elif raw_text2 == "360":
            res = "640x360"
        elif raw_text2 == "480":
            res = "854x480"
        elif raw_text2 == "720":
            res = "1280x720"
        elif raw_text2 == "1080":
            res = "1920x1080" 
        else: 
            res = "UN"
    except Exception:
            res = "UN"

    await editable.edit(
    "╭───『 𝗘𝗻𝘁𝗲𝗿 𝗬𝗼𝘂𝗿 𝗡𝗮𝗺𝗲 』───╮\n"
    "│ ✏️ Type your name to continue\n"
    "│ ➊  Send 1 to use default name\n"
    "╰──────────╯"
)
    input3: Message = await bot.listen(editable.chat.id)
    raw_text3 = input3.text
    await input3.delete(True)
    if raw_text3 == '1':
        CR = '[ ⌯ FʀᴏɴᴛMᴀɴ | ×͜× |](https://t.me/Mrfrontman001)'
    else:
        CR = raw_text3

    await editable.edit("🔹Enter Your PW Token For 𝐌𝐏𝐃 𝐔𝐑𝐋\n🔹Send /d for use default")
    input4: Message = await bot.listen(editable.chat.id)
    raw_text4 = input4.text
    await input4.delete(True)

    await editable.edit(f"🔹Send the Video Thumb URL\n🔹Send /d for use default\n\n🔹You can direct upload thumbnail")
    input6 = message = await bot.listen(editable.chat.id)
    raw_text6 = input6.text
    await input6.delete(True)

    if input6.photo:
        thumb = await input6.download()  # Use the photo sent by the user
    elif raw_text6.startswith("http://") or raw_text6.startswith("https://"):
        # If a URL is provided, download thumbnail from the URL
        getstatusoutput(f"wget '{raw_text6}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    else:
        thumb = raw_text6
    await editable.delete()

    # Add delay before sending batch message
    await asyncio.sleep(2)
    try:
        target_batch_message = await m.reply_text(f"__**🎯Target Batch : {b_name}**__")
        try:
            await target_batch_message.pin()
        except Exception:
            # Silently handle any pinning errors (private chat, permissions, etc)
            pass
    except FloodWait as e:
        await asyncio.sleep(e.value)
        target_batch_message = await m.reply_text(f"__**🎯Target Batch : {b_name}**__")
        try:
            await target_batch_message.pin()
        except Exception:
            # Silently handle any pinning errors (private chat, permissions, etc)
            pass

    failed_count = 0
    count = int(raw_text)    
    arg = int(raw_text)
    try:
        for i in range(arg-1, len(links)):
            # Add delay between processing each link
            await asyncio.sleep(2)
            
            Vxy = links[i][1].replace("file/d/","uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing","")
            url = "https://" + Vxy
            link0 = "https://" + Vxy

            name1 = links[i][0].replace("(", "[").replace(")", "]").replace("_", "").replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
            name = f'{name1[:60]}'
            
            if "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Referer': 'http://www.visionias.in/', 'Sec-Fetch-Dest': 'iframe', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'cross-site', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Linux; Android 12; RMX2121) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36', 'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"', 'sec-ch-ua-mobile': '?1', 'sec-ch-ua-platform': '"Android"',}) as resp:
                        text = await resp.text()
                        url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)

            if "acecwply" in url:
                    cmd = f'yt-dlp -o "{name}.%(ext)s" -f "bestvideo[height<={raw_text2}][ext=mp4]/bv[height<={raw_text2}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]" --hls-prefer-ffmpeg --no-keep-video --remux-video mkv --no-warning "{url}"'

            elif "https://cpvod.testbook.com/" in url or "classplusapp.com/drm/" in url:
                url = url.replace("https://cpvod.testbook.com/","https://media-cdn.classplusapp.com/drm/")
                url = f"https://covercel.vercel.app/extract_keys?url={url}@bots_updatee&user_id=7793257011"
                #url = f"https://scammer-keys.vercel.app/api?url={url}&token={cptoken}&auth=@scammer_botxz1"
                mpd, keys = helper.get_mps_and_keys(url)
                url = mpd
                keys_string = " ".join([f"--key {key}" for key in keys])

            elif "classplusapp" in url:
                signed_api = f"https://covercel.vercel.app/extract_keys?url={url}@bots_updatee&user_id=7793257011"
                response = requests.get(signed_api, timeout=20)
                url = response.text.strip()
                url = response.json()['url']  
                
            elif "tencdn.classplusapp" in url:
                headers = {'host': 'api.classplusapp.com', 'x-access-token': f'{cptoken}', 'accept-language': 'EN', 'api-version': '18', 'app-version': '1.4.73.2', 'build-number': '35', 'connection': 'Keep-Alive', 'content-type': 'application/json', 'device-details': 'Xiaomi_Redmi 7_SDK-32', 'device-id': 'c28d3cb16bbdac01', 'region': 'IN', 'user-agent': 'Mobile-Android', 'webengage-luid': '00000187-6fe4-5d41-a530-26186858be4c', 'accept-encoding': 'gzip'}
                params = {"url": f"{url}"}
                response = requests.get('https://api.classplusapp.com/cams/uploader/video/jw-signed-url', headers=headers, params=params)
                url = response.json()['url']  
           
            elif 'videos.classplusapp' in url:
                url = requests.get(f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}', headers={'x-access-token': f'{token_cp}'}).json()['url']
            
            elif 'media-cdn.classplusapp.com' in url or 'media-cdn-alisg.classplusapp.com' in url or 'media-cdn-a.classplusapp.com' in url: 
                headers = {'host': 'api.classplusapp.com', 'x-access-token': f'{token_cp}', 'accept-language': 'EN', 'api-version': '18', 'app-version': '1.4.73.2', 'build-number': '35', 'connection': 'Keep-Alive', 'content-type': 'application/json', 'device-details': 'Xiaomi_Redmi 7_SDK-32', 'device-id': 'c28d3cb16bbdac01', 'region': 'IN', 'user-agent': 'Mobile-Android', 'webengage-luid': '00000187-6fe4-5d41-a530-26186858be4c', 'accept-encoding': 'gzip'}
                params = {"url": f"{url}"}
                response = requests.get('https://api.classplusapp.com/cams/uploader/video/jw-signed-url', headers=headers, params=params)
                url   = response.json()['url']
                
            #elif "d1d34p8vz63oiq" in url or "sec1.pw.live" in url:
            elif "childId" in url and "parentId" in url:
                url = f"https://anonymouspwplayer-0e5a3f512dec.herokuapp.com/pw?url={url}&token={raw_text4}"
                #url =  f"{api_url}pw-dl?url={url}&token={raw_text4}&authorization={api_token}&q={raw_text2}"
            
            #elif '/master.mpd' in url:    
                #headers = {"Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3NDYyODQwNTYuOTIsImRhdGEiOnsiX2lkIjoiNjdlYTcyYjZmODdlNTNjMWZlNzI5MTRlIiwidXNlcm5hbWUiOiI4MzQ5MjUwMTg1IiwiZmlyc3ROYW1lIjoiSGFycnkiLCJvcmdhbml6YXRpb24iOnsiX2lkIjoiNWViMzkzZWU5NWZhYjc0NjhhNzlkMTg5Iiwid2Vic2l0ZSI6InBoeXNpY3N3YWxsYWguY29tIiwibmFtZSI6IlBoeXNpY3N3YWxsYWgifSwicm9sZXMiOlsiNWIyN2JkOTY1ODQyZjk1MGE3NzhjNmVmIl0sImNvdW50cnlHcm91cCI6IklOIiwidHlwZSI6IlVTRVIifSwiaWF0IjoxNzQ1Njc5MjU2fQ.6WMjQPLUPW-fMCViXERGSqhpFZ-FyX-Vjig7L531Q6U", "client-type": "WEB", "randomId": "142d9660-50df-41c0-8fcb-060609777b03"}
                #id =  url.split("/")[-2] 
                #policy = requests.post('https://api.penpencil.xyz/v1/files/get-signed-cookie', headers=headers, json={'url': f"https://d1d34p8vz63oiq.cloudfront.net/" + id + "/master.mpd"}).json()['data']
                #url = "https://sr-get-video-quality.selav29696.workers.dev/?Vurl=" + "https://d1d34p8vz63oiq.cloudfront.net/" + id + f"/hls/{raw_text2}/main.m3u8" + policy
                #print(url)

            if ".pdf*" in url:
                url = f"https://dragoapi.vercel.app/pdf/{url}"
            if ".zip" in url:
                url = f"https://video.pablocoder.eu.org/appx-zip?url={url}"
                
            elif 'encrypted.m' in url:
                appxkey = url.split('*')[1]
                url = url.split('*')[0]

            if "youtu" in url:
                ytf = f"b[height<={raw_text2}][ext=mp4]/bv[height<={raw_text2}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
            elif "embed" in url:
                ytf = f"bestvideo[height<={raw_text2}]+bestaudio/best[height<={raw_text2}]"
            else:
                ytf = f"b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b/bv+ba"
           
            if "jw-prod" in url:
                cmd = f'yt-dlp -o "{name}.mp4" "{url}"'
            elif "webvideos.classplusapp." in url:
               cmd = f'yt-dlp --add-header "referer:https://web.classplusapp.com/" --add-header "x-cdn-tag:empty" -f "{ytf}" "{url}" -o "{name}.mp4"'
            elif "youtube.com" in url or "youtu.be" in url:
                cmd = f'yt-dlp --cookies youtube_cookies.txt -f "{ytf}" "{url}" -o "{name}".mp4'
            else:
                cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'

            try:
                cc = f'╭━━━━━━━━━━━╮\n**🎥 VIDEO ID :** {str(count).zfill(3)}.\n╰━━━━━━━━━━━╯\n\n' \
        f'**📄 Title : {name1}** ᴍʀꜱᴛʀᴀɴɢᴇʀ™.mkv\n\n' \
        f'**🔖 Batch :** `{b_name}`\n\n' \
        f'**📥 Extracted By : {CR}**\n'
                cc1 = f'╭━━━━━━━━━━━╮\n**🎥 FILE ID :** {str(count).zfill(3)}.\n╰━━━━━━━━━━━╯\n\n' \
        f'**📄 Title : {name1}** ᴍʀꜱᴛʀᴀɴɢᴇʀ™.pdf\n\n' \
        f'**🔖 Batch :** `{b_name}`\n\n' \
        f'**📥 Extracted By : {CR}**\n'
                cczip = f'[——— ✦ {str(count).zfill(3)} ✦ ———]({link0})\n\n' \
        f'**🆔 𝑍𝐼𝑃 𝑰𝑑 :** `{count}`\n' \
        f'**📁 𝑇𝑖𝑡𝑙𝑒 :** `{name1}`\n' \
        f'**├── 𝑅𝑒𝑠𝑜𝑙𝑢𝑡𝑖𝑜𝑛 :** [{res}]\n\n' \
        f'**📚 𝐶𝑜𝑢𝑟𝑠𝑒 :** {b_name}\n\n' \
        f'**🌟 𝐸𝑥𝑡𝑟𝑎𝑐𝑡𝑒𝑑 𝐵𝑦 :** {CR}'
                ccimg = f'**🏷️ Fɪʟᴇ ID :**  {str(count).zfill(3)}\n\n' \
        f'**🖼️ Tɪᴛʟᴇ :** `{name1}`\n\n' \
        f'<pre>📚 𝗕ᴀᴛᴄʜ : {b_name}</pre>\n\n' \
        f'**🎓 Exᴛʀᴀᴄᴛ Bʏ : {CR}**\n'
                ccm = f'**🏷️ Fɪʟᴇ ID :**  {str(count).zfill(3)}\n\n**🎞️ Tɪᴛʟᴇ :** `{name1} [{res}p] .mkv`\n\n<blockquote><b>📚 𝗕ᴀᴛᴄʜ :</b> {b_name}</blockquote>\n\n**🎓 Exᴛʀᴀᴄᴛ Bʏ : {CR}**\n'
                cchtml = f'[——— ✦ {str(count).zfill(3)} ✦ ———]({link0})\n\n' \
         f'**🆔 𝐻𝑇𝑀𝐿 𝑰𝑑 :** `{count}`\n' \
         f'**🌐 𝑇𝑖𝑡𝑙𝑒 :** `{name1}`\n' \
         f'**├── 𝑅𝑒𝑠𝑜𝑙𝑢𝑡𝑖𝑜𝑛 :** [{res}]\n\n' \
         f'**📚 𝐶𝑜𝑢𝑟𝑠𝑒 :** {b_name}\n\n' \
         f'**🌟 𝐸𝑥𝑡𝑟𝑎𝑐𝑡𝑒𝑑 𝐵𝑦 :** {CR}'

                if "drive" in url:
                    try:
                        ka = await helper.download(url, name)
                        copy = await bot.send_document(chat_id=m.chat.id,document=ka, caption=cc1)
                        count+=1
                        os.remove(ka)
                    except FloodWait as e:
                        await asyncio.sleep(e.value)
                        ka = await helper.download(url, name)
                        copy = await bot.send_document(chat_id=m.chat.id,document=ka, caption=cc1)
                        count+=1
                        os.remove(ka)
                    except Exception as e:
                        await m.reply_text(f"Error downloading from drive: {str(e)}")
                        continue

                elif ".pdf" in url:
                    if "cwmediabkt99" in url:
                        max_retries = 15  # Define the maximum number of retries
                        retry_delay = 4  # Delay between retries in seconds
                        success = False  # To track whether the download was successful
                        failure_msgs = []  # To keep track of failure messages
                        
                        for attempt in range(max_retries):
                            try:
                                await asyncio.sleep(retry_delay)
                                url = url.replace(" ", "%20")
                                scraper = cloudscraper.create_scraper()
                                response = scraper.get(url)

                                if response.status_code == 200:
                                    with open(f'{name}.pdf', 'wb') as file:
                                        file.write(response.content)
                                    await asyncio.sleep(retry_delay)  # Optional, to prevent spamming
                                    copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1)
                                    count += 1
                                    os.remove(f'{name}.pdf')
                                    success = True
                                    break  # Exit the retry loop if successful
                                else:
                                    failure_msg = await m.reply_text(f"Attempt {attempt + 1}/{max_retries} failed: {response.status_code} {response.reason}")
                                    failure_msgs.append(failure_msg)
                                    
                            except Exception as e:
                                failure_msg = await m.reply_text(f"Attempt {attempt + 1}/{max_retries} failed: {str(e)}")
                                failure_msgs.append(failure_msg)
                                await asyncio.sleep(retry_delay)
                                continue  # Retry the next attempt if an exception occurs

                        # Delete all failure messages if the PDF is successfully downloaded
                        for msg in failure_msgs:
                            await msg.delete()
                            
                        if not success:
                            # Send the final failure message if all retries fail
                                await m.reply_text(f"Failed to download PDF after {max_retries} attempts.\n⚠️**Downloading Failed**⚠️\n**Name** =>> {str(count).zfill(3)} {name1}\n**Url** =>> {link0}", disable_web_page_preview) # type: ignore
                            
            
                    else:
                        try:
                            cmd = f'yt-dlp -o "{name}.pdf" "{url}"'
                            download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                            os.system(download_cmd)
                            copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1)
                            count += 1
                            os.remove(f'{name}.pdf')
                        except FloodWait as e:
                            await asyncio.sleep(e.value)
                            continue    

                elif ".ws" in url and  url.endswith(".ws"):
                    try:
                        await helper.pdf_download(f"{api_url}utkash-ws?url={url}&authorization={api_token}",f"{name}.html")
                        time.sleep(1)
                        await bot.send_document(chat_id=m.chat.id, document=f"{name}.html", caption=cchtml)
                        os.remove(f'{name}.html')
                        count += 1
                    except FloodWait as e:
                        await asyncio.sleep(e.value)
                        continue    

                elif ".zip" in url:
                    try:
                        BUTTONSZIP= InlineKeyboardMarkup([[InlineKeyboardButton(text="🎥 ZIP STREAM IN PLAYER", url=f"{url}")]])
                        await bot.send_photo(chat_id=m.chat.id, photo=photozip, caption=cczip, reply_markup=BUTTONSZIP)
                        count +=1
                        time.sleep(1)
                    except FloodWait as e:
                        await asyncio.sleep(e.value)
                        continue    

                elif any(ext in url for ext in [".jpg", ".jpeg", ".png"]):
                    try:
                        ext = url.split('.')[-1]
                        cmd = f'yt-dlp -o "{name}.{ext}" "{url}"'
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                        os.system(download_cmd)
                        copy = await bot.send_photo(chat_id=m.chat.d, photo=f'{name}.{ext}', caption=ccimg)
                        count += 1
                        os.remove(f'{name}.{ext}')
                    except FloodWait as e:
                        await asyncio.sleep(e.value)
                        continue    

                elif any(ext in url for ext in [".mp3", ".wav", ".m4a"]):
                    try:
                        ext = url.split('.')[-1]
                        cmd = f'yt-dlp -o "{name}.{ext}" "{url}"'
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                        os.system(download_cmd)
                        copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.{ext}', caption=ccm)
                        count += 1
                        os.remove(f'{name}.{ext}')
                    except FloodWait as e:
                        await asyncio.sleep(e.value)
                        continue    
                    
                elif 'encrypted.m' in url:    
                    remaining_links = len(links) - count
                    progress = (count / len(links)) * 100
                    emoji_message = await show_random_emojis(message)
                    Show = f"╭━━━━━━━━━━━━━━━━━━━━━━━\n" \
                           f"┃ 🚀 **ᴘʀᴏɢʀᴇss**: {progress:.2f}%\n" \
                           f"┃ ────────────────────\n" \
                           f"┃ 🔗 **ɪɴᴅᴇx**: {count}/{len(links)}\n" \
                           f"┃ 🖇️ **ʀᴇᴍᴀɪɴɪɴɢ ʟɪɴᴋs**: {remaining_links}\n" \
                           f"╰━━━━━━━━━━━━━━━━━━━━━━━\n\n" \
                           f"**⚡ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴇɴᴄʀʏᴘᴛᴇᴅ ғɪʟᴇ...⏳**\n" \
                           f"━━━━━━━━━━━━━━━━━━━━━━━\n" \
                           f"┃ 💃 **ᴄʀᴇᴅɪᴛᴇᴅ ᴛᴏ**: {CR}\n" \
                           f"┃ 📚 **ʙᴀᴛᴄʜ ɴᴀᴍᴇ**: {b_name}\n" \
                           f"━━━━━━━━━━━━━━━━━━━━━━━\n" \
                           f"┃ 📚 **ᴛɪᴛʟᴇ**: {name}\n" \
                           f"┃ 🍁 **Qᴜᴀʟɪᴛʏ**: {quality}\n" \
                           f"┃ 🔗 **ʟɪɴᴋ**: <a href='{link0}'>ᴏʀɪɢɪɴᴀʟ ʟɪɴᴋ</a>\n" \
                           f"┃ 🖇️ **ᴀᴘɪ ᴜʀʟ**: <a href='{url}'>ᴀᴘɪ ʟɪɴᴋ</a>\n" \
                           f"━━━━━━━━━━━━━━━━━━━━━━━\n" \
                           f"🛑 **sᴇɴᴅ** /stop **ᴛᴏ ᴄᴀɴᴄᴇʟ**\n\n" \
                           f"╰━━━━━ ✦ 𝐵𝑜𝓉 𝓂𝒶𝒹𝑒 𝒷𝓎 ✦ @MrFrontMan001"

                    prog = await m.reply_text(Show, disable_web_page_preview=True)
                    try:
                        res_file = await helper.download_and_decrypt_video(url, cmd, name, appxkey)  
                        filename = res_file
                        await emoji_message.delete()
                        await prog.delete(True)
                        if os.path.exists(filename) and os.path.getsize(filename) > 0:
                            nirvana_base_url = await database.get_nirvana_api()
                            nirvana_url = f"{nirvana_base_url}/?videoUrl={link0}"
                            # BUTTONS = InlineKeyboardMarkup([[InlineKeyboardButton(text="🎥 Watch Online ", url=nirvana_url)]])
                            await helper.send_vid(bot, m, cc, filename, thumb, name, prog)
                            count += 1
                            await asyncio.sleep(1)
                        else:
                            await m.reply_text(f"⚠️**Download Failed**⚠️\n**Name** =>> `{str(count).zfill(3)} {name1}`\n**Url** =>> {link0}", disable_web_page_preview=True)
                            failed_count += 1
                            count += 1
                    except Exception as e:
                        await m.reply_text(f"⚠️**Download Failed**⚠️\n**Name** =>> `{str(count).zfill(3)} {name1}`\n**Url** =>> {link0}\n**Error**: {str(e)}", disable_web_page_preview=True)
                        failed_count += 1
                        count += 1
                        continue

                elif 'drmcdni' in url or 'drm/wv' in url:
                    remaining_links = len(links) - count
                    progress = (count / len(links)) * 100
                    emoji_message = await show_random_emojis(message)
                    Show = f"╭━━━━━━━━━━━━━━━━━━━━━━━\n" \
                           f"┃ 🚀 **ᴘʀᴏɢʀᴇss**: {progress:.2f}%\n" \
                           f"┃ ────────────────────\n" \
                           f"┃ 🔗 **ɪɴᴅᴇx**: {count}/{len(links)}\n" \
                           f"┃ 🖇️ **ʀᴇᴍᴀɪɴɪɴɢ ʟɪɴᴋs**: {remaining_links}\n" \
                           f"╰━━━━━━━━━━━━━━━━━━━━━━━\n\n" \
                           f"**⚡ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴅʀᴍ sᴛᴀʀᴛᴇᴅ...⏳**\n" \
                           f"━━━━━━━━━━━━━━━━━━━━━━━\n" \
                           f"┃ 💃 **ᴄʀᴇᴅɪᴛᴇᴅ ᴛᴏ**: {CR}\n" \
                           f"┃ 📚 **ʙᴀᴛᴄʜ ɴᴀᴍᴇ**: {b_name}\n" \
                           f"━━━━━━━━━━━━━━━━━━━━━━━\n" \
                           f"┃ 📚 **ᴛɪᴛʟᴇ**: {name}\n" \
                           f"┃ 🍁 **Qᴜᴀʟɪᴛʏ**: {quality}\n" \
                           f"┃ 🔗 **ʟɪɴᴋ**: <a href='{link0}'>ᴏʀɪɢɪɴᴀʟ ʟɪɴᴋ</a>\n" \
                           f"┃ 🖇️ **ᴀᴘɪ ᴜʀʟ**: <a href='{url}'>ᴀᴘɪ ʟɪɴᴋ</a>\n" \
                           f"━━━━━━━━━━━━━━━━━━━━━━━\n" \
                           f"🛑 **sᴇɴᴅ** /stop **ᴛᴏ ᴄᴀɴᴄᴇʟ**\n\n" \
                           f"**╰━━━━━ ✦ 𝐵𝑜𝓉 𝓂𝒶𝒹𝑒 𝒷𝓎 ✦ @MrFrontMan001**"

                    prog = await m.reply_text(Show, disable_web_page_preview=True)
                    try:
                        res_file = await helper.decrypt_and_merge_video(mpd, keys_string, path, name, raw_text2)
                        filename = res_file
                        await emoji_message.delete()
                        await prog.delete(True)
                        if os.path.exists(filename) and os.path.getsize(filename) > 0:
                            nirvana_base_url = await database.get_nirvana_api()
                            nirvana_url = f"{nirvana_base_url}/?videoUrl={link0}"
                            # BUTTONS = InlineKeyboardMarkup([[InlineKeyboardButton(text="🎥 Watch Online ", url=nirvana_url)]])
                            await helper.send_vid(bot, m, cc, filename, thumb, name, prog)
                            count += 1
                            await asyncio.sleep(1)
                        else:
                            await m.reply_text(f"⚠️**Download Failed**⚠️\n**Name** =>> `{str(count).zfill(3)} {name1}`\n**Url** =>> {link0}", disable_web_page_preview=True)
                            failed_count += 1
                            count += 1
                    except Exception as e:
                        await m.reply_text(f"⚠️**Download Failed**⚠️\n**Name** =>> `{str(count).zfill(3)} {name1}`\n**Url** =>> {link0}\n**Error**: {str(e)}", disable_web_page_preview=True)
                        failed_count += 1
                        count += 1
                        continue
     
                else:
                    remaining_links = len(links) - count
                    progress = (count / len(links)) * 100
                    emoji_message = await show_random_emojis(message)
                    Show = f"╭━━━━━━━━━━━━━━━━━━━━━━━\n" \
                           f"┃ 🚀 **ᴘʀᴏɢʀᴇss**: {progress:.2f}%\n" \
                           f"┃ ────────────────────\n" \
                           f"┃ 🔗 **ɪɴᴅᴇx**: {count}/{len(links)}\n" \
                           f"┃ 🖇️ **ʀᴇᴍᴀɪɴɪɴɢ ʟɪɴᴋs**: {remaining_links}\n" \
                           f"╰━━━━━━━━━━━━━━━━━━━━━━━\n\n" \
                           f"**⚡ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ sᴛᴀʀᴛᴇᴅ...⏳**\n" \
                           f"━━━━━━━━━━━━━━━━━━━━━━━\n" \
                           f"┃ 💃 **ᴄʀᴇᴅɪᴛᴇᴅ ᴛᴏ**: {CR}\n" \
                           f"┃ 📚 **ʙᴀᴛᴄʜ ɴᴀᴍᴇ**: {b_name}\n" \
                           f"━━━━━━━━━━━━━━━━━━━━━━━\n" \
                           f"┃ 📚 **ᴛɪᴛʟᴇ**: {name}\n" \
                           f"┃ 🍁 **Qᴜᴀʟɪᴛʏ**: {quality}\n" \
                           f"┃ 🔗 **ʟɪɴᴋ**: <a href='{link0}'>ᴏʀɪɢɪɴᴀʟ ʟɪɴᴋ</a>\n" \
                           f"┃ 🖇️ **ᴀᴘɪ ᴜʀʟ**: <a href='{url}'>ᴀᴘɪ ʟɪɴᴋ</a>\n" \
                           f"━━━━━━━━━━━━━━━━━━━━━━━\n" \
                           f"🛑 **sᴇɴᴅ** /stop **ᴛᴏ ᴄᴀɴᴄᴇʟ**\n\n" \
                           f"╰━━━━━ ✦ 𝐵𝑜𝓉 𝓂𝒶𝒹𝑒 𝒷𝓎 ✦ @MrFrontMan001"
                    
                    prog = await m.reply_text(Show, disable_web_page_preview=True)
                    try:
                        res_file = await helper.download_video(url, cmd, name)
                        filename = res_file
                        await emoji_message.delete()
                        await prog.delete(True)
                        nirvana_base_url = await database.get_nirvana_api()
                        nirvana_url = f"{nirvana_base_url}/?videoUrl={link0}"
                        # BUTTONS = InlineKeyboardMarkup([[InlineKeyboardButton(text="🎥 Watch Online ", url=nirvana_url)]])
                        if os.path.exists(filename) and os.path.getsize(filename) > 0:
                            await helper.send_vid(bot, m, cc, filename, thumb, name, prog)
                            count += 1
                            await asyncio.sleep(1)
                        else:
                            await m.reply_text(f"⚠️**Download Failed**⚠️\n**Name** =>> `{str(count).zfill(3)} {name1}`\n**Url** =>> {link0}", disable_web_page_preview=True)
                            failed_count += 1
                            count += 1
                    except Exception as e:
                        await m.reply_text(f"⚠️**Download Failed**⚠️\n**Name** =>> `{str(count).zfill(3)} {name1}`\n**Url** =>> {link0}\n**Error**: {str(e)}", disable_web_page_preview=True)
                        failed_count += 1
                        count += 1
                        continue

            except Exception as e:
                await m.reply_text(f'⚠️**Downloading Failed**⚠️\n**Name** =>> `{str(count).zfill(3)} {name1}`\n**Url** =>> {link0}', disable_web_page_preview=True)
                count += 1
                failed_count += 1
                continue

    except Exception as e:
            await editable.edit(f"<pre><code>🔹An error occurred: {str(e)}</code></pre>")
            logging.error(f"Error in txt_handler: {str(e)}")
            return

    except Exception as e:
        await editable.edit(f"<pre><code>🔹An error occurred: {str(e)}</code></pre>")
        logging.error(f"Error in txt_handler: {str(e)}")
        return

    await m.reply_text(f"⋅ ─ Total failed links is {failed_count} ─ ⋅")

    await m.reply_text(f"⋅ ─ list index ({raw_text}-{len(links)}) out of range ─ ⋅\n\n✨ **BATCH** » {b_name}✨\n\n⋅ ─ DOWNLOADING ✩ COMPLETED ─ ⋅")
             
@bot.on_message(filters.command(["adduser", "removeuser", "checkuser"]) & filters.private)
async def manage_users_cmd(bot: Client, message: Message):
    # Check if sender is admin
    if message.from_user.id not in ADMIN_IDS:
        await message.reply_text(
            "╭━━━━━━━━━━━━━━━━━╮\n"
            "┣⪼ ⚠️ 𝐀𝐜𝐜𝐞𝐬𝐬 𝐃𝐞𝐧𝐢𝐞𝐝\n"
            "╰━━━━━━━━━━━━━━━━━╯",
            disable_web_page_preview=True
        )
        return

    command = message.command[0].lower()
    
    try:
        if command == "adduser":
            # Format: /adduser user_id days
            if len(message.command) != 3:
                await message.reply_text(
                    "╭━━━━━━━━━━━━━━━━━╮\n"
                    "┣⪼ ℹ️ 𝐂𝐨𝐫𝐫𝐞𝐜𝐭 𝐅𝐨𝐫𝐦𝐚𝐭:\n"
                    "┣⪼ /adduser user_id days\n"
                    "╰━━━━━━━━━━━━━━━━━╯",
                    disable_web_page_preview=True
                )
                return

            user_id = int(message.command[1])
            days = int(message.command[2])
            
            await database.add_user(user_id, days)
            status = await database.get_subscription_status(user_id)
            
            await message.reply_text(
                "╭━━━━━━━━━━━━━━━━━╮\n"
                f"┣⪼ ✅ 𝐔𝐬𝐞𝐫 𝐀𝐝𝐝𝐞𝐝\n"
                "╰━━━━━━━━━━━━━━━━━╯\n\n"
                "╭─────────────────\n"
                f"┣⪼ 👤 𝐔𝐬𝐞𝐫 𝐈𝐃: {user_id}\n"
                f"┣⪼ ⏳ 𝐃𝐚𝐲𝐬: {days}\n"
                f"┣⪼ 📅 𝐄𝐱𝐩𝐢𝐫𝐞𝐬: {status['expiry_date'].strftime('%Y-%m-%d %H:%M:%S')}\n"
                "╰─────────────────",
                disable_web_page_preview=True
            )
        elif command == "removeuser":
            # Format: /removeuser user_id
            if len(message.command) != 2:
                await message.reply_text(
                    "╭━━━━━━━━━━━━━━━━━╮\n"
                    "┣⪼ ℹ️ 𝐂𝐨𝐫𝐫𝐞𝐜𝐭 𝐅𝐨𝐫𝐦𝐚𝐭:\n"
                    "┣⪼ /removeuser user_id\n"
                    "╰━━━━━━━━━━━━━━━━━╯",
                    disable_web_page_preview=True
                )
                return

            user_id = int(message.command[1])
            await database.remove_user(user_id)
            
            await message.reply_text(
                "╭━━━━━━━━━━━━━━━━━╮\n"
                f"┣⪼ ❌ 𝐔𝐬𝐞𝐫 𝐑𝐞𝐦𝐨𝐯𝐞𝐝\n"
                "╰━━━━━━━━━━━━━━━━━╯\n\n"
                "╭─────────────────\n"
                f"┣⪼ 👤 𝐔𝐬𝐞𝐫 𝐈𝐃: {user_id}\n"
                "╰─────────────────",
                disable_web_page_preview=True
            )

        elif command == "checkuser":
            # Format: /checkuser user_id
            if len(message.command) != 2:
                await message.reply_text(
                    "╭━━━━━━━━━━━━━━━━━╮\n"
                    "┣⪼ ℹ️ 𝐂𝐨𝐫𝐫𝐞𝐜𝐭 𝐅𝐨𝐫𝐦𝐚𝐭:\n"
                    "┣⪼ /checkuser user_id\n"
                    "╰━━━━━━━━━━━━━━━━━╯",
                    disable_web_page_preview=True
                )
                return

            user_id = int(message.command[1])
            status = await database.get_subscription_status(user_id)
            
            if status["is_subscribed"]:
                await message.reply_text(
                    "╭━━━━━━━━━━━━━━━━━╮\n"
                    f"┣⪼ ✅ 𝐀𝐜𝐭𝐢𝐯𝐞 𝐒𝐮𝐛𝐬𝐜𝐫𝐢𝐩𝐭𝐢𝐨𝐧\n"
                    "╰━━━━━━━━━━━━━━━━━╯\n\n"
                    "╭─────────────────\n"
                    f"┣⪼ 👤 𝐔𝐬𝐞𝐫 𝐈𝐃: {user_id}\n"
                    f"┣⪼ ⏳ 𝐃𝐚𝐲𝐬 𝐋𝐞𝐟𝐭: {status['days_left']}\n"
                    f"┣⪼ 📅 𝐄𝐱𝐩𝐢𝐫𝐞𝐬: {status['expiry_date'].strftime('%Y-%m-%d %H:%M:%S')}\n"
                    "╰─────────────────",
                    disable_web_page_preview=True
                )
            else:
                await message.reply_text(
                    "╭━━━━━━━━━━━━━━━━━╮\n"
                    f"┣⪼ ❌ 𝐍𝐨 𝐀𝐜𝐭𝐢𝐯𝐞 𝐒𝐮𝐛𝐬𝐜𝐫𝐢𝐩𝐭𝐢𝐨𝐧\n"
                    "╰━━━━━━━━━━━━━━━━━╯\n\n"
                    "╭─────────────────\n"
                    f"┣⪼ 👤 𝐔𝐬𝐞𝐫 𝐈𝐃: {user_id}\n"
                    "╰─────────────────",
                    disable_web_page_preview=True
                )
                
    except ValueError:
        await message.reply_text(
            "╭━━━━━━━━━━━━━━━━━╮\n"
            "┣⪼ ⚠️ 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐈𝐧𝐩𝐮𝐭\n"
            "╰━━━━━━━━━━━━━━━━━╯\n\n"
            "╭─────────────────\n"
            "┣⪼ 𝐏𝐥𝐞𝐚𝐬𝐞 𝐩𝐫𝐨𝐯𝐢𝐝𝐞 𝐯𝐚𝐥𝐮𝐞:\n"
            "┣⪼ • 𝐔𝐬𝐞𝐫 𝐈𝐃 (𝐧𝐮𝐦𝐛𝐞𝐫)\n"
            "┣⪼ • 𝐃𝐚𝐲𝐬 (𝐧𝐮𝐦𝐛𝐞𝐫)\n"
            "╰─────────────────",
            disable_web_page_preview=True
        )
    except Exception as e:
        await message.reply_text(
            "╭━━━━━━━━━━━━━━━━━╮\n"
            f"┣⪼ ⚠️ 𝐄𝐫𝐫𝐨𝐫: {str(e)}\n"
            "╰━━━━━━━━━━━━━━━━━╯",
            disable_web_page_preview=True
        )

@bot.on_message(filters.command(["users"]) & filters.private)
async def list_users_cmd(bot: Client, message: Message):
    # Check if sender is admin
    if message.from_user.id not in ADMIN_IDS:
        await message.reply_text(
            "╭━━━━━━━━━━━━━━━━━╮\n"
            "┣⪼ ⚠️ 𝐀𝐜𝐜𝐞𝐬𝐬 𝐃𝐞𝐧𝐢𝐞𝐝\n"
            "╰━━━━━━━━━━━━━━━━━╯",
            disable_web_page_preview=True
        )
        return

    try:
        users = await database.get_all_users()
        if not users:
            await message.reply_text(
                "╭━━━━━━━━━━━━━━━━━╮\n"
                "┣⪼ ℹ️ 𝐍𝐨 𝐔𝐬𝐞𝐫𝐬 𝐅𝐨𝐮𝐧𝐝\n"
                "╰━━━━━━━━━━━━━━━━━╯",
                disable_web_page_preview=True
            )
            return

        response = "╭━━━━━━━━━━━━━━━━━╮\n"
        response += "┣⪼ 📋 𝐒𝐮𝐛𝐬𝐜𝐫𝐢𝐛𝐞𝐫 𝐋𝐢𝐬𝐭\n"
        response += "╰━━━━━━━━━━━━━━━━━╯\n\n"

        for user in users:
            expiry = user['expiry_date'].strftime('%Y-%m-%d %H:%M:%S') if user.get('expiry_date') else 'No expiry'
            response += "╭─────────────────\n"
            response += f"┣⪼ 👤 𝐔𝐬𝐞𝐫 𝐈𝐃: {user['user_id']}\n"
            response += f"┣⪼ 📅 𝐄𝐱𝐩𝐢𝐫𝐞𝐬: {expiry}\n"
            response += "╰─────────────────\n"

        await message.reply_text(response, disable_web_page_preview=True)

    except Exception as e:
        await message.reply_text(
            "╭━━━━━━━━━━━━━━━━━╮\n"
            f"┣⪼ ⚠️ 𝐄𝐫𝐫𝐨𝐫: {str(e)}\n"
            "╰━━━━━━━━━━━━━━━━━╯",
            disable_web_page_preview=True
        )
             
@bot.on_message(filters.command(["add_chat"]))
async def add_chat_cmd(bot: Client, message: Message):
    try:
        # First check if user is authorized
        is_auth = await database.is_user_authorized(message.from_user.id)
        if not is_auth:
            await message.reply_text(
                "╭━━━━━━━━━━━━━━━━━╮\n"
                "┣⪼ ⚠️ 𝐔𝐧𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝 𝐀𝐜𝐜𝐞𝐬𝐬\n"
                "╰━━━━━━━━━━━━━━━━━╯\n\n"
                "╭─────────────────\n"
                "┣⪼ 📌 𝐏𝐥𝐞𝐚𝐬𝐞 𝐜𝐨𝐧𝐭𝐚𝐜𝐭\n"
                "┣⪼ 👤 @Dhruv10081\n"
                "┣⪼ 💫 𝐅𝐨𝐫 𝐒𝐮𝐛𝐬𝐜𝐫𝐢𝐩𝐭𝐢𝐨𝐧\n"
                "╰─────────────────"
            )
            return

        # Check command format
        if len(message.command) != 2:
            await message.reply_text(
                "╭━━━━━━━━━━━━━━━━━╮\n"
                "┣⪼ ℹ️ 𝐂𝐨𝐫𝐫𝐞𝐜𝐭 𝐅𝐨𝐫𝐦𝐚𝐭:\n"
                "┣⪼ /add_chat chat_id\n"
                "╰━━━━━━━━━━━━━━━━━╯"
            )
            return

        try:
            chat_id = int(message.command[1])
        except ValueError:
            await message.reply_text(
                "╭━━━━━━━━━━━━━━━━━╮\n"
                "┣⪼ ⚠️ 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐂𝐡𝐚𝐭 𝐈𝐃\n"
                "┣⪼ 𝐏𝐥𝐞𝐚𝐬𝐞 𝐞𝐧𝐭𝐞𝐫 𝐚 𝐯𝐚𝐥𝐢𝐝 𝐧𝐮𝐦𝐛𝐞𝐫\n"
                "╰━━━━━━━━━━━━━━━━━╯"
            )
            return

        # Try to get chat info to verify it exists and bot has access
        try:
            chat = await bot.get_chat(chat_id)
            
            # Check if bot is admin in the chat
            bot_member = await chat.get_member(bot.me.id)
            if not bot_member.privileges:
                await message.reply_text(
                    "╭━━━━━━━━━━━━━━━━━╮\n"
                    "┣⪼ ⚠️ 𝐁𝐨𝐭 𝐍𝐨𝐭 𝐀𝐝𝐦𝐢𝐧\n"
                    "┣⪼ 𝐌𝐚𝐤𝐞 𝐛𝐨𝐭 𝐚𝐝𝐦𝐢𝐧 𝐟𝐢𝐫𝐬𝐭\n"
                    "╰━━━━━━━━━━━━━━━━━╯"
                )
                return

            # Add the chat
            await database.add_chat(message.from_user.id, chat_id)
            
            await message.reply_text(
                "╭━━━━━━━━━━━━━━━━━╮\n"
                "┣⪼ ✅ 𝐂𝐡𝐚𝐭 𝐀𝐝𝐝𝐞𝐝\n"
                "╰━━━━━━━━━━━━━━━━━╯\n\n"
                "╭─────────────────\n"
                f"┣⪼ 💭 𝐂𝐡𝐚𝐭 𝐈𝐃: {chat_id}\n"
                f"┣⪼ 📝 𝐓𝐲𝐩𝐞: {chat.type}\n"
                f"┣⪼ 📌 𝐓𝐢𝐭𝐥𝐞: {chat.title}\n"
                "╰─────────────────"
            )

        except Exception as e:
            await message.reply_text(
                "╭━━━━━━━━━━━━━━━━━╮\n"
                "┣⪼ ⚠️ 𝐄𝐫𝐫𝐨𝐫 𝐀𝐜𝐜𝐞𝐬𝐬𝐢𝐧𝐠 𝐂𝐡𝐚𝐭\n"
                "┣⪼ 𝐌𝐚𝐤𝐞 𝐬𝐮𝐫𝐞:\n"
                "┣⪼ • 𝐁𝐨𝐭 𝐢𝐬 𝐚𝐝𝐝𝐞𝐝 𝐭𝐨 𝐜𝐡𝐚𝐭\n"
                "┣⪼ • 𝐁𝐨𝐭 𝐢𝐬 𝐚𝐝𝐦𝐢𝐧\n"
                "┣⪼ • 𝐂𝐡𝐚𝐭 𝐈𝐃 𝐢𝐬 𝐜𝐨𝐫𝐫𝐞𝐜𝐭\n"
                "╰━━━━━━━━━━━━━━━━━╯"
            )
            return

    except Exception as e:
        await message.reply_text(
            "╭━━━━━━━━━━━━━━━━━╮\n"
            f"┣⪼ ⚠️ 𝐄𝐫𝐫𝐨𝐫: {str(e)}\n"
            "╰━━━━━━━━━━━━━━━━━╯"
        )

@bot.on_message(filters.command(["remove_chat"]))
async def remove_chat_cmd(bot: Client, message: Message):
    try:
        # First check if user is authorized
        is_auth = await database.is_user_authorized(message.from_user.id)
        if not is_auth:
            await message.reply_text(
                "╭━━━━━━━━━━━━━━━━━╮\n"
                "┣⪼ ⚠️ 𝐔𝐧𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝 𝐀𝐜𝐜𝐞𝐬𝐬\n"
                "╰━━━━━━━━━━━━━━━━━╯"
            )
            return

        # Check command format
        if len(message.command) != 2:
            await message.reply_text(
                "╭━━━━━━━━━━━━━━━━━╮\n"
                "┣⪼ ℹ️ 𝐂𝐨𝐫𝐫𝐞𝐜𝐭 𝐅𝐨𝐫𝐦𝐚𝐭:\n"
                "┣⪼ /remove_chat chat_id\n"
                "╰━━━━━━━━━━━━━━━━━╯"
            )
            return

        chat_id = int(message.command[1])
        
        # Remove the chat
        await database.remove_chat(message.from_user.id, chat_id)
        
        await message.reply_text(
            "╭━━━━━━━━━━━━━━━━━╮\n"
            "┣⪼ ✅ 𝐂𝐡𝐚𝐭 𝐑𝐞𝐦𝐨𝐯𝐞𝐝\n"
            "╰━━━━━━━━━━━━━━━━━╯\n\n"
            "╭─────────────────\n"
            f"┣⪼ 💭 𝐂𝐡𝐚𝐭 𝐈𝐃: {chat_id}\n"
            "╰─────────────────"
        )

    except ValueError:
        await message.reply_text(
            "╭━━━━━━━━━━━━━━━━━╮\n"
            "┣⪼ ⚠️ 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐂𝐡𝐚𝐭 𝐈𝐃\n"
            "╰━━━━━━━━━━━━━━━━━╯"
        )
    except Exception as e:
        await message.reply_text(
            "╭━━━━━━━━━━━━━━━━━╮\n"
            f"┣⪼ ⚠️ 𝐄𝐫𝐫𝐨𝐫: {str(e)}\n"
            "╰━━━━━━━━━━━━━━━━━╯"
        )

@bot.on_message(filters.command(["list_chats"]))
async def list_chats_cmd(bot: Client, message: Message):
    try:
        # First check if user is authorized
        is_auth = await database.is_user_authorized(message.from_user.id)
        if not is_auth:
            await message.reply_text(
                "╭━━━━━━━━━━━━━━━━━╮\n"
                "┣⪼ ⚠️ 𝐔𝐧𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝 𝐀𝐜𝐜𝐞𝐬𝐬\n"
                "╰━━━━━━━━━━━━━━━━━╯"
            )
            return

        chats = await database.get_user_chats(message.from_user.id)
        
        if not chats:
            await message.reply_text(
                "╭━━━━━━━━━━━━━━━━━╮\n"
                "┣⪼ ℹ️ 𝐍𝐨 𝐂𝐡𝐚𝐭𝐬 𝐀𝐝𝐝𝐞𝐝\n"
                "╰━━━━━━━━━━━━━━━━━╯"
            )
            return

        response = "╭━━━━━━━━━━━━━━━━━╮\n"
        response += "┣⪼ 📋 𝐘𝐨𝐮𝐫 𝐀𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝 𝐂𝐡𝐚𝐭𝐬\n"
        response += "╰━━━━━━━━━━━━━━━━━╯\n\n"

        for chat_id in chats:
            try:
                chat = await bot.get_chat(chat_id)
                response += "╭─────────────────\n"
                response += f"┣⪼ 💭 𝐂𝐡𝐚𝐭 𝐈𝐃: {chat_id}\n"
                response += f"┣⪼ 📝 𝐓𝐲𝐩𝐞: {chat.type}\n"
                response += f"┣⪼ 📌 𝐓𝐢𝐭𝐥𝐞: {chat.title}\n"
                response += "╰─────────────────\n"
            except:
                response += "╭─────────────────\n"
                response += f"┣⪼ 💭 𝐂𝐡𝐚𝐭 𝐈𝐃: {chat_id}\n"
                response += "┣⪼ ⚠️ 𝐍𝐨𝐭 𝐀𝐜𝐜𝐞𝐬𝐬𝐢𝐛𝐥𝐞\n"
                response += "╰─────────────────\n"

        await message.reply_text(response)

    except Exception as e:
        await message.reply_text(
            "╭━━━━━━━━━━━━━━━━━╮\n"
            f"┣⪼ ⚠️ 𝐄𝐫𝐫𝐨𝐫: {str(e)}\n"
            "╰━━━━━━━━━━━━━━━━━╯"
        )

@bot.on_message(filters.command(["diagnose"]) & filters.private)
async def diagnose_cmd(bot: Client, message: Message):
    """Diagnose authorization issues for a user"""
    try:
        # If no user_id provided, use the sender's ID
        user_id = message.from_user.id
        if len(message.command) > 1:
            try:
                user_id = int(message.command[1])
            except ValueError:
                await message.reply_text(
                    "╭━━━━━━━━━━━━━━━━━╮\n"
                    "┣⪼ ⚠️ Invalid user ID\n"
                    "╰━━━━━━━━━━━━━━━━━╯"
                )
                return

        # Get diagnostic info
        result = await database.diagnose_authorization(user_id)
        
        # Format the response
        response = [
            "╭━━━━━━━━━━━━━━━━━╮",
            f"┣⪼ 🔍 Authorization Diagnosis",
            "╰━━━━━━━━━━━━━━━━━╯\n",
            "╭─────────────────",
            f"┣⪼ 👤 User ID: {user_id}",
            f"┣⪼ ✅ Overall Status: {'Authorized' if result['overall_authorized'] else '❌ Not Authorized'}"
        ]

        # MongoDB status
        if result["mongodb_status"]:
            if result["mongodb_status"]["found"]:
                response.extend([
                    "┣⪼ 📊 MongoDB Status:",
                    f"┣⪼ • Valid: {'✅' if result['mongodb_status'].get('is_valid') else '❌'}",
                    f"┣⪼ • Expires: {result['mongodb_status'].get('expiry_date', 'N/A')}"
                ])
            else:
                response.append("┣⪼ 📊 MongoDB: User not found")

        # JSON status
        if result["json_status"]:
            if result["json_status"].get("file_exists") is False:
                response.append("┣⪼ 📄 JSON: File not found")
            elif result["json_status"]["found"]:
                if "error" in result["json_status"]:
                    response.extend([
                        "┣⪼ 📄 JSON Status:",
                        f"┣⪼ • Error: {result['json_status']['error']}"
                    ])
                else:
                    response.extend([
                        "┣⪼ 📄 JSON Status:",
                        f"┣⪼ • Valid: {'✅' if result['json_status'].get('is_valid') else '❌'}",
                        f"┣⪼ • Expires: {result['json_status'].get('expiry_date', 'N/A')}"
                    ])
            else:
                response.append("┣⪼ 📄 JSON: User not found")

        # Admin status
        response.append(f"┣⪼ 👑 Admin: {'✅' if result['is_admin'] else '❌'}")

        if result["error"]:
            response.extend([
                "┣⪼ ⚠️ Error occurred:",
                f"┣⪼ {result['error']}"
            ])

        response.append("╰─────────────────")

        await message.reply_text("\n".join(response))

    except Exception as e:
        await message.reply_text(
            "╭━━━━━━━━━━━━━━━━━╮\n"
            f"┣⪼ ⚠️ Error: {str(e)}\n"
            "╰━━━━━━━━━━━━━━━━━╯"
        )

@bot.on_message(filters.command(["dbstatus"]) & filters.private)
async def db_status_cmd(bot: Client, message: Message):
    """Check MongoDB connection status"""
    try:
        # First check if user is admin
        if message.from_user.id not in ADMIN_IDS:
            await message.reply_text(
                "╭━━━━━━━━━━━━━━━━━╮\n"
                "┣⪼ ⚠️ Admin access required\n"
                "╰━━━━━━━━━━━━━━━━━╯"
            )
            return

        # Show testing message
        status_msg = await message.reply_text(
            "╭━━━━━━━━━━━━━━━━━╮\n"
            "┣⪼ 🔍 Testing MongoDB...\n"
            "╰━━━━━━━━━━━━━━━━━╯"
        )

        # Test connection
        result = await database.test_mongodb_connection()
        
        # Format response
        response = [
            "╭━━━━━━━━━━━━━━━━━╮",
            "┣⪼ 📊 MongoDB Status",
            "╰━━━━━━━━━━━━━━━━━╯\n",
            "╭─────────────────",
            f"┣⪼ Available: {'✅' if result['mongodb_available'] else '❌'}",
            f"┣⪼ Connected: {'✅' if result['client_connected'] else '❌'}",
            f"┣⪼ DB Access: {'✅' if result['db_accessible'] else '❌'}",
            f"┣⪼ Collection: {'✅' if result['collection_writable'] else '❌'}"
        ]

        if result["error"]:
            response.extend([
                "┣⪼ ⚠️ Error:",
                f"┣⪼ {result['error']}"
            ])

        response.append("╰─────────────────")

        # Update message
        await status_msg.edit_text("\n".join(response))

        # If there are issues, try to reconnect
        if not all([result['mongodb_available'], result['client_connected'], 
                   result['db_accessible'], result['collection_writable']]):
            reconnect_msg = await message.reply_text(
                "╭━━━━━━━━━━━━━━━━━╮\n"
                "┣⪼ 🔄 Attempting to reconnect...\n"
                "╰━━━━━━━━━━━━━━━━━╯"
            )
            
            success = await database.reconnect_mongodb()
            
            if success:
                await reconnect_msg.edit_text(
                    "╭━━━━━━━━━━━━━━━━━╮\n"
                    "┣⪼ ✅ Reconnected successfully\n"
                    "╰━━━━━━━━━━━━━━━━━╯"
                )
            else:
                await reconnect_msg.edit_text(
                    "╭━━━━━━━━━━━━━━━━━╮\n"
                    "┣⪼ ❌ Reconnection failed\n"
                    "╰━━━━━━━━━━━━━━━━━╯"
                )

    except Exception as e:
        await message.reply_text(
            "╭━━━━━━━━━━━━━━━━━╮\n"
            f"┣⪼ ⚠️ Error: {str(e)}\n"
            "╰━━━━━━━━━━━━━━━━━╯"
        )

bot.run()

