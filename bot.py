import os, logging, asyncio
from telethon import Button
from telethon import TelegramClient, events
from telethon.tl.types import ChannelParticipantsAdmins

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

api_id = int(os.environ.get("APP_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("TOKEN")
bot_username = os.environ.get("BOT_USERNAME")
channel_updates = os.environ.get("CHANNEL_UPDATES")
group_support = os.environ.get("GROUP_SUPPORT")
bot_name = os.environ.get("BOT_NAME")
owner_bot = os.environ.get("OWNER_BOT")
client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
  await event.reply(f"__👋🏻 Hallo {usr.first_name}\n**Saya adalah {bot_name} Bot**, Saya dapat menyebutkan hampir semua anggota di grup atau chanel \nKlik **/help** untuk informasi lebih lanjut__\n\n 👩‍💻 Bot ini dikelola oleh @{owner_bot}",
                    buttons=(
                      [Button.url('➕ Tambahkan saya ke Grup Anda ➕', url=f'https://t.me/{bot_username}?startgroup=true')],
                      [Button.url('📣 Chanel', url=f'https://t.me/{channel_updates}'),
                      Button.url('💬 Grup', url=f'https://t.me/{group_support}')]
                    ),
                    link_preview=False
                   )
@client.on(events.NewMessage(pattern="^/help$"))
async def help(event):
  helptext = f"**Menu Bantuan dari {bot_name} Bot**\n\nCMD: /mentionall\n__Anda dapat menggunakan perintah ini dengan teks apa yang ingin Anda sebutkan orang lain.__\n`Contoh: /mentionall Apakabar Semuanya!`\n__Anda dapat memberikan perintah ini sebagai balasan untuk pesan apa pun. Bot akan menandai pengguna ke pesan balasan itu__.\n\n 👩‍💻 Bot ini dikelola oleh @{owner_bot}"
  await event.reply(helptext,
                    buttons=(
                      [Button.url('➕ Tambahkan saya ke Grup Anda ➕', url=f'https://t.me/{bot_username}?startgroup=true')],
                      [Button.url('📣 Chanel', url=f'https://t.me/{channel_updates}'),
                      Button.url('💬 Grup', url=f'https://t.me/{group_support}')]
                    ),
                    link_preview=False
                   )
  
@client.on(events.NewMessage(pattern="^/mentionall ?(.*)"))
async def mentionall(event):
  if event.is_private:
    return await event.respond("__Perintah ini dapat digunakan dalam grup dan chanel!__")
  
  admins = []
  async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.respond("__Hanya admin yang boleh mention semua!__")
  
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.respond("__Saya tidak bisa menyebut anggota untuk pesan lama! (pesan yang dikirim sebelum saya ditambahkan ke grup)__")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("__Beri aku satu argumen!__")
  else:
    return await event.respond("__Membalas pesan atau memberi saya beberapa teks untuk menyebutkan orang lain!__")
  
  if mode == "text_on_cmd":
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if usrnum == 5:
        await client.send_message(event.chat_id, f"{usrtxt}\n\n{msg}")
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""
        
  if mode == "text_on_reply":
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if usrnum == 5:
        await client.send_message(event.chat_id, usrtxt, reply_to=msg)
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""
        
print(">> BOT STARTED <<")
client.run_until_disconnected()
