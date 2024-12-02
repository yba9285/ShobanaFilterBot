
<h1 align="center">
  <b>shobana filter bot</b>
</h1>


[![Stars](https://img.shields.io/github/stars/mntg4u/shobanafilterbot?style=flat-square&color=yellow)](https://github.com/mntg4u/shobanafilterbot/stargazers)
[![Forks](https://img.shields.io/github/forks/mntg4u/shobanafilterbot?style=flat-square&color=orange)](https://github.com/mntg4u/shobanafilterbot/fork)
[![Size](https://img.shields.io/github/repo-size/mntg4u/shobanafilterbot?style=flat-square&color=green)](https://github.com/mntg4u/shobanafilterbot)   
[![Open Source Love svg2](https://badges.frapsoft.com/os/v2/open-source.svg?v=103)](https://github.com/mntg4u/shobanafilterbot)   
[![Contributors](https://img.shields.io/github/contributors/mntg4u/shobanafilterbot?style=flat-square&color=green)](https://github.com/mntg4u/shobanafilterbot/graphs/contributors)
[![License](https://img.shields.io/badge/License-AGPL-blue)](https://github.com/mntg4u/shobanafilterbot/blob/main/LICENSE)
[![Sparkline](https://stars.medv.io/mntg4u/shobanafilterbot.svg)](https://github.com/mntg4u/shobanafilterbot)


## Features

- [x] Auto Filter
- [x] Manual Filter
- [x] IMDB
- [x] Admin Commands
- [x] Broadcast
- [x] Index
- [x] IMDB search
- [x] Inline Search
- [x] Random pics
- [x] ids and User info 
- [x] Stats, Users, Chats, Ban, Unban, Leave, Disable, Channel
- [x] Spelling Check Feature
- [x] File Store
- [x] Auto approve feature added
- [x] CARBON
- [x] Echo
- [x]  SHORTNER LINK SUPPORT USING /short
- [x]  Feed back
- [x]  font change using /font
- [x] PROMOTE/DEMOTE
- [x] PINN/UNPIN
- [x]  IMAGE TO LINK SUPPORT
## Variables

Read [this](https://telegram.dog/mnbots) before you start messing up with your edits.

### Required Variables
* `BOT_TOKEN`: Create a bot using [@BotFather](https://telegram.dog/BotFather), and get the Telegram API token.
* `API_ID`: Get this value from [telegram.org](https://my.telegram.org/apps)
* `API_HASH`: Get this value from [telegram.org](https://my.telegram.org/apps)
* `CHANNELS`: Username or ID of channel or group. Separate multiple IDs by space
* `ADMINS`: Username or ID of Admin. Separate multiple Admins by space
* `DATABASE_URI`: [mongoDB](https://www.mongodb.com) URI. Get this value from [mongoDB](https://www.mongodb.com). For more help watch this [video](https://youtu.be/1G1XwEOnxxo)
* `DATABASE_NAME`: Name of the database in [mongoDB](https://www.mongodb.com). For more help watch this [video](https://youtu.be/Miajl2amrKo)
* `LOG_CHANNEL` : A channel to log the activities of bot. Make sure bot is an admin in the channel.
### Optional Variables
* `PICS`: Telegraph links of images to show in start message.( Multiple images can be used separated by space )
* `FILE_STORE_CHANNEL`: Channel from were file store links of posts should be made.Separate multiple IDs by space
* Check [info.py](https://github.com/mntg4u/shobanafilterbot/blob/main/info.py) for more


## Deploy
You can deploy this bot anywhere.

<details><summary>Deploy To Koyeb</summary>
<p>
<br>
<a href="https://app.koyeb.com/deploy?type=git&repository=github.com/Jithins7/MPD_BOT&env[BOT_TOKEN]&env[API_ID]&env[API_HASH]&env[CHANNELS]&env[ADMINS]&env[PICS]&env[LOG_CHANNEL]&env[AUTH_CHANNEL]&env[CUSTOM_FILE_CAPTION]&env[DATABASE_URI]&env[DATABASE_NAME]&env[COLLECTION_NAME]=Telegram_files&env[FILE_CHANNEL]=-1001832732995&env[SUPPORT_CHAT]&env[IMDB]=True&env[IMDB_TEMPLATE]&env[SINGLE_BUTTON]=True&env[AUTH_GROUPS]&env[P_TTI_SHOW_OFF]=True&branch=main&name=telegrambot">
 <img src="https://www.koyeb.com/static/images/deploy/button.svg">
</a>
</p>
</details>

<details><summary>Deploy To VPS</summary>
<p>
<pre>
git clone https://github.com/mntg4u/shobanafilterbot
# Install Packages
pip3 install -U -r requirements.txt
Edit info.py with variables as given below then run bot
python3 bot.py
</pre>
</p>
</details>


## Commands
```
• /logs - to get the rescent errors
• /stats - to get status of files in db.
* /filter - add manual filters
* /filters - view filters
* /connect - connect to PM.
* /disconnect - disconnect from PM
* /del - delete a filter
* /delall - delete all filters
* /deleteall - delete all index(autofilter)
* /delete - delete a specific file from index.
* /info - get user info
* /id - get tg ids.
* /imdb - fetch info from imdb.
• /users - to get list of my users and ids.
• /chats - to get list of the my chats and ids 
• /index  - to add files from a channel
• /leave  - to leave from a chat.
• /disable  -  do disable a chat.
* /enable - re-enable chat.
• /ban  - to ban a user.
• /unban  - to unban a user.
• /channel - to get list of total connected channels
• /broadcast - to broadcast a message to all Eva Maria users
• /batch - to create link for multiple posts
• /link - to create link for one post
```
## Support
[![telegram badge](https://img.shields.io/badge/Telegram-Group-30302f?style=flat&logo=telegram)](https://telegram.dog/mnbots_support)
[![telegram badge](https://img.shields.io/badge/Telegram-Channel-30302f?style=flat&logo=telegram)](https://telegram.dog/mrmntg)



## Thanks to 
 - Thanks To Dan For His Awesome [Library](https://github.com/pyrogram/pyrogram)
 - Thanks To Mahesh  For His Awesome [Media-Search-bot](https://github.com/Mahesh0253/Media-Search-bot)
 - Thanks To [EvamariaTG](https://raw.githubusercontent.com/EvamariaTG) for their awesome [EvaMaria Bot](https://raw.githubusercontent.com/EvamariaTG/EvaMaria)
 - Thanks To [Trojanz](https://github.com/trojanzhex) for Their Awesome [Unlimited Filter Bot](https://github.com/TroJanzHEX/Unlimited-Filter-Bot) And [AutoFilterBoT](https://github.com/trojanzhex/auto-filter-bot)
 - Thanks to Goutham for adding spell check feature ,ping and restart codes
 - Thanks to MN-TG Who Have Edited And Modified This Repo
 - Thanks To All Everyone In This Journey

### Note

[Note To A So Called Dev](https://telegram.dog/mrmntg): 

Kanging this codes and and editing a few lines and releasing a V.x  or an [alpha](https://telegram.dog/mrmntg), beta , gama branches of your repo won't make you a Developer.
Fork the repo and edit as per your needs.

## Disclaimer
[![GNU Affero General Public License 2.0](https://www.gnu.org/graphics/agplv3-155x51.png)](https://www.gnu.org/licenses/agpl-3.0.en.html#header)    
Licensed under [GNU AGPL 2.0.](https://github.com/EvamariaTG/evamaria/blob/master/LICENSE)
Selling The Codes To Other People For Money Is *Strictly Prohibited*.
