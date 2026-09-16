import sys
sys.path.insert(0, 'discord.py-self')
import discord
import platform
import requests
import asyncio
import json
import re
import datetime
import urllib
import pickle
import os
import psutil
import instaloader
import aiohttp
import time
from colour import Color
from dateutil import parser
from discord.ext import commands, tasks
from datetime import datetime, timezone, timedelta
from pytz import timezone
from concurrent.futures import ThreadPoolExecutor
from discord import Embed
import urllib.parse
import random
import math
import itertools

try:
    with open('config/config.json') as f:
        config = json.load(f)
except FileNotFoundError:
    print("\033[1;31m[!] Khong tim thay config/config.json!\033[0m")
    print("\033[1;33m  -> Tao file config/config.json voi noi dung: {\"token\": \"...\", \"prefix\": \".\", \"sniper_webhook\": \"...\"}\033[0m")
    sys.exit(1)

token = config.get('token', '')
prefix = config.get('prefix', '.')
WEBHOOK_URL = config.get('sniper_webhook', '')

if not token:
    print("\033[1;31m[!] Token trong config.json trong!\033[0m")
    sys.exit(1)

HEADERS = {
    "Authorization": token,
    "Content-Type": "application/json"
}

active_features = {
    'cyclestatus': False,
    'auto_react': False,
    'spam': False,
    'nhay': False,
    'ngon': False,
    'webhook': False,
    'tokenspam': False,
    'tokenvc': False,
    'vcspam': False,
    'forcedisconnect': False,
    'nuke': False,
    'overnuke': False
}

bot = commands.Bot(command_prefix=prefix, self_bot=True)
bot.remove_command('help')
vietnam_tz = timezone('Asia/Ho_Chi_Minh')
spamming_nhay_task = None
spamming_ngon_task = None
spamming_task = None
webhook_task = None
spam_voice = None
spam_task = None
nuke_task = None
overnuke_task = None
nuke_semaphore = None
spam_count = {'spam': 0, 'nhay': 0, 'ngon': 0, 'webhook': 0, 'tokenspam': 0, 'tokenvc': 0, 'vcspam': 0, 'nuke': 0, 'overnuke': 0}
cycleStatus = False
force_disconnect_user = None
disconnecting = False
threads = []
statuses = []
current_status = 0
afk_users = {}
afk_reason = None
SPECIFIC_USER_ID = 973110180382404630
status_changing = False
spamming = False
vc_join_tasks = {}
greeting_settings = {}
fonts_folder = "fonts"
fonts = {}
usedcodes = []
auto_react_enabled = True
status_file = "trash/status_lines.txt"
nitro_sniper = True
onalt = False
sound_notification = False
webhooknotification = True
changing_time = 10
status_tag = discord.Status.online
version = '1.0.0'
__NAME__ = 'VVNK'
executor = ThreadPoolExecutor(max_workers=10)
message_file_global = None

def NitroInfo(elapsed, code):
    print(f"Elapsed Time: {elapsed} seconds\nNitro Code: {code}")

def mainHeader():
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US',
        'Content-Type': 'application/json',
        'authorization': token,
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'x-debug-options': 'bugReporterEnabled',
        'x-discord-locale': 'en-US',
        'x-discord-timezone': 'America/Chicago',
        'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJwdGIiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC4xMDcyIiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDQiLCJvc19hcmNoIjoieDY0IiwiYXBwX2FyY2giOiJpYTMyIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV09XNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIGRpc2NvcmQvMS4wLjEwNzIgQ2hyb21lLzEyMC4wLjYwOTkuMjkxIEVsZWN0cm9uLzI4LjIuMTAgU2FmYXJpLzUzNy4zNiIsImJyb3dzZXJfdmVyc2lvbiI6IjI4LjIuMTAiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjoyOTM5NTksIm5hdGl2ZV9idWlsZF9udW1iZXIiOjQ3Njk3LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsLCJkZXNpZ25faWQiOjB9'
    }
    return headers

proxy_list = []
proxy_cycle = None
proxy_file = "config/proxies.txt"
last_proxy_time = 0
last_proxy_refresh = 0
PROXY_ROTATE_MIN = 0
PROXY_ROTATE_MAX = 2
PROXY_REFRESH_INTERVAL = 300

PROXY_API_URLS = [
    "https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=protocolipport&format=text",
    "https://cdn.jsdelivr.net/gh/officialputuid/KangProxy@main/xResults/Proxies.txt",
    "https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/protocols/http/data.txt",
    "https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/protocols/socks5/data.txt",
    "https://raw.githubusercontent.com/VPSLabCloud/VPSLab-Free-Proxy-List/main/http_elite.txt",
    "https://raw.githubusercontent.com/VPSLabCloud/VPSLab-Free-Proxy-List/main/socks5_all.txt",
]

def load_proxies():
    global proxy_list, proxy_cycle, last_proxy_refresh
    if os.path.exists(proxy_file):
        with open(proxy_file, 'r') as f:
            proxy_list = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        if proxy_list:
            proxy_cycle = itertools.cycle(proxy_list)
            last_proxy_refresh = time.time()
            print(f"\033[1;32m[PROXY] Loaded {len(proxy_list)} proxies from file\033[0m")
        else:
            print(f"\033[1;33m[PROXY] No proxies found in file\033[0m")
    else:
        print(f"\033[1;33m[PROXY] {proxy_file} not found\033[0m")

async def fetch_proxies_from_api():
    global proxy_list, proxy_cycle, last_proxy_refresh
    new_proxies = []
    for url in PROXY_API_URLS:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                    if resp.status == 200:
                        text = await resp.text()
                        lines = [line.strip() for line in text.splitlines() if line.strip()]
                        valid = [l for l in lines if l.startswith(('http://', 'https://', 'socks4://', 'socks5://'))]
                        new_proxies.extend(valid)
                        print(f"\033[1;32m[PROXY] Fetched {len(valid)} from {url.split('/')[2]}\033[0m")
        except Exception as e:
            print(f"\033[1;33m[PROXY] Failed to fetch from {url.split('/')[2]}: {e}\033[0m")
    if new_proxies:
        unique = list(set(new_proxies))
        proxy_list = unique
        proxy_cycle = itertools.cycle(proxy_list)
        last_proxy_refresh = time.time()
        print(f"\033[1;32m[PROXY] Updated: {len(proxy_list)} proxies total\033[0m")
        with open(proxy_file, 'w') as f:
            f.write(f"# Auto-refreshed proxies\n")
            for p in proxy_list:
                f.write(f"{p}\n")
    else:
        print(f"\033[1;33m[PROXY] No new proxies fetched\033[0m")

def check_proxy_refresh():
    if time.time() - last_proxy_refresh >= PROXY_REFRESH_INTERVAL:
        asyncio.ensure_future(fetch_proxies_from_api())

def get_next_proxy():
    global proxy_cycle, last_proxy_time
    if proxy_cycle:
        last_proxy_time = time.time()
        return next(proxy_cycle)
    return None

def get_random_proxy():
    global last_proxy_time
    if proxy_list:
        last_proxy_time = time.time()
        return random.choice(proxy_list)
    return None

def should_rotate_proxy():
    if not proxy_list:
        return False
    elapsed = time.time() - last_proxy_time
    return elapsed >= random.uniform(PROXY_ROTATE_MIN, PROXY_ROTATE_MAX)

def get_proxy_dict():
    proxy = get_next_proxy()
    if proxy:
        return {"http": proxy, "https": proxy}
    return None

async def fetch_with_proxy(url, method="GET", headers=None, data=None):
    for attempt in range(len(proxy_list) + 1):
        proxy_url = get_random_proxy() if proxy_list else None
        try:
            async with aiohttp.ClientSession() as session:
                kwargs = {"headers": headers}
                if proxy_url:
                    kwargs["proxy"] = proxy_url
                if data:
                    kwargs["data"] = data
                async with getattr(session, method.lower())(url, **kwargs) as response:
                    if response.status == 429:
                        retry_after = float(response.headers.get("retry-after", 2))
                        rotate_delay = random.uniform(PROXY_ROTATE_MIN, PROXY_ROTATE_MAX)
                        print(f"\033[1;33m[RATELIMIT] Proxy {proxy_url} limited, rotating in {rotate_delay:.1f}s...\033[0m")
                        await asyncio.sleep(rotate_delay)
                        continue
                    return response
        except Exception as e:
            print(f"\033[1;31m[PROXY ERROR] {proxy_url}: {e}\033[0m")
            await asyncio.sleep(random.uniform(0.1, 0.5))
            continue
    return None

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        syntax_map = {
            "spam": ".spam [delay] [channel_id] [nội_dung] (bỏ trong channel = kênh hiện tại)",
            "nhay": ".nhay [delay] [channel_id] [@user] (bỏ qua = kênh hiện tại, không tag)",
            "webhook": ".webhook [url] [nội_dung]",
            "nuke": ".nuke [server] [amount] - xóa kênh + tạo kênh + spam nhay.txt (mặc định: sv hiện tại, 300 dòng)",
            "overnuke": ".overnuke [server] [amount] - xả nhay.txt + @everyone tất cả kênh (mặc định: sv hiện tại, 150 dòng)",
            "tokenspam": ".tokenspam [delay] [file/nội_dung]",
            "massreact": ".massreact [số] [emoji]",
            "kick": ".kick [@user]",
            "ban": ".ban [@user]",
            "unban": ".unban [user_id]",
            "clear": ".clear [số_lượng]",
            "afk": ".afk [lý_do]",
            "setstatus": ".setstatus [text]",
            "addstatus": ".addstatus [text]",
            "cloneemoji": ".cloneemoji [emoji]",
            "clone_channels": ".clone_channels [id_cũ] [id_mới]",
            "clone_roles": ".clone_roles [id_cũ] [id_mới]",
            "tokencheck": ".tokencheck [token]",
            "checkpromo": ".checkpromo [link]",
            "iplookup": ".iplookup [ip]",
            "insta": ".insta [tên]",
            "math": ".math [phép_tính]",
            "phc": ".phc [@user] [text]",
            "rpc": ".rpc [type] [tên]",
            "nsfw": ".nsfw [loại]",
            "rizz": ".rizz [@user]",
            "roast": ".roast [@user]",
            "forcedisconnect": ".forcedisconnect [@user]",
            "tokenvc": ".tokenvc [voice_id]",
            "vcspam": ".vcspam [voice_id]",
            "vcjoin": ".vcjoin [voice_id] [Y/N] [Y/N] [Y/N]",
            "xanhac": ".xanhac [voice_id] [tên_file]",
        }
        cmd = ctx.command.name
        syntax = syntax_map.get(cmd, f".{cmd} [tham_so]")
        await ctx.send(f"```\n[CU PHAP] {syntax}\n```")
    elif isinstance(error, commands.CommandNotFound):
        pass
    else:
        print(f"\033[1;31m[ERROR] {ctx.command}: {error}\033[0m")

@bot.event
async def on_message(message):
    if message.author == bot.user and auto_react_enabled:
        reactions = {
            'ngu': '🤣',
            'oc cac': '🤣',
        }
        for word, emoji in reactions.items():
            if message.content.lower() == word:
                await message.add_reaction(emoji)
        if message.content.endswith('?'):
            await message.add_reaction('❓')

    if not message.author.bot:
        if isinstance(message.channel, discord.DMChannel):
            if afk_reason is not None:
                await message.author.send(f"afk: {afk_reason}.")
        else:
            if bot.user in message.mentions:
                if afk_reason is not None:
                    await message.channel.send(f"**{message.author.name}**autorep: {afk_reason}.")

    if nitro_sniper and re.search(r"(?:discord\.gift/|discord(?:app)?\.com/gifts/)(\w+)", message.content):
        start = datetime.now()
        codes = re.findall(r"(?:discord\.gift/|discord(?:app)?\.com/gifts/)(\w+)", message.content)
        async with aiohttp.ClientSession() as session:
            for code in codes:
                if len(code) in [16, 24] and code not in usedcodes:
                    usedcodes.append(code)
                    headers = {"Authorization": token}
                    async with session.post(
                        f"https://discordapp.com/api/v6/entitlements/gift-codes/{code}/redeem",
                        headers=headers
                    ) as r:
                        elapsed = datetime.now() - start
                        elapsed = f"{elapsed.seconds}.{elapsed.microseconds}"
                        time = datetime.now().strftime("%H:%M")
                        text = await r.text()
                        if "This gift has been redeemed already." in text:
                            print(f"\n{time} - Nitro is Already Redeemed")
                            NitroInfo(elapsed, code)
                        elif "subscription_plan" in text:
                            print(f"\n{time} - Nitro Successfully Claimed!")
                            NitroInfo(elapsed, code)
                            if webhooknotification:
                                data = {
                                    "content": f"# __{__NAME__}__\n`??` **Congrats!!** your nitro GIFT LINK has been claimed.\n||@everyone|| ||@here||"
                                }
                                await session.post(WEBHOOK_URL, json=data)
                        elif "Unknown Gift Code" in text:
                            print(f"\n{time} - Unknown Nitro Gift Code")
                            NitroInfo(elapsed, code)

    await bot.process_commands(message)
    
class Embed:
    def __init__(self, title: str, **kwargs):
        description = kwargs.get("description", "")
        colour = kwargs.get("colour", "") or kwargs.get("color", "") or "000000"
        url = kwargs.get("url", "")
        if isinstance(colour, int):
            colour = str(hex(colour)[2:])
        elif isinstance(colour, str):
            if colour.startswith("#"):
                colour = colour[1:]
            elif colour.startswith("0x"):
                colour = colour[2:]
        self.base_url = "https://benny.fun/api/embed?"
        self.params = {
            "title": title,
            "description": description,
            "color": colour,
            "url": url
        }

    def __str__(self):
        return self.generate_url(hide_url=True)

    def set_title(self, title: str):
        self.params["title"] = title

    def set_description(self, description: str):
        self.params["description"] = description

    def set_colour(self, colour: str):
        self.params["colour"] = colour

    def set_author(self, name: str, *, url: str = ""):
        self.params["author_name"] = name
        if url:
            self.params["author_url"] = url

    def set_provider(self, name: str, *, url: str = ""):
        self.params["provider_name"] = name
        if url:
            self.params["provider_url"] = url

    def set_image(self, url: str, big: bool = False):
        self.params["image"] = url
        self.params["big_image"] = big

    def set_video(self, url: str):
        self.params["video"] = url

    def generate_url(self, *, hide_url: bool = False, shorten_url: bool = False, shortener=None):
        for key in list(self.params.keys()):
            if self.params[key] == "" or self.params[key] is None:
                del self.params[key]
        url = self.base_url + urllib.parse.urlencode(self.params)
        if shorten_url and shortener:
            url = shortener.shorten(url)
        return f"[᲼]({url})" if hide_url else url

@bot.command()
async def menu(ctx):
    try:
        await ctx.message.delete()
        panel = f"""    ✨ VVNK ✨  
--- Lệnh Chính ---

.botinfo  : Xem thông tin chi tiết về bot
.tienich  : Danh sách các tiện ích hữu ích
.troll  : Chế độ giải trí, đùa vui
.shutdown  : Tắt bot 
.restart  : Khởi động lại bot 
.raid  : Hiển thị bộ lệnh đú trend
.quanly  : Danh sách lệnh quản lý server

>>>  Thông Tin Bot 
🔑 𝘼𝙘𝙘𝙤𝙪𝙣𝙩𝙨: {bot.user.name}
🆔 ID: {bot.user.id}
👑 Author: QU4N.TH3.D3V"""
        gif_url = "https://cdn.discordapp.com/attachments/1376174995230949446/1520297142709784626/From_Klickpin.com-_Printable_Wall_Art_Ideas_That_Make_Everyday_Better_29506-pin-id-730779477063900866.gif?ex=6a7a07cc&is=6a78b64c&hm=725cd5f9cdc5cf06d1725742ca9b26064d8b6052afc1ce75877caa28a6606885&"
        await ctx.send(f"```yaml\n{panel}\n```")
        await ctx.send(gif_url)
    except Exception as e:
        await ctx.send(f"❌ Lỗi: {str(e)}\n[Panel GIF]: {gif_url}")
        
@bot.command()
async def raid(ctx):
    await ctx.message.delete()
    raid_message = """```yaml
Raid

--- Lệnh Spam ---
.spam [delay] [channel_id] [noi_dung]  : Spam nội dung với độ trễ
.nhay [delay] [channel_id] [@user]     : Spam từ file nhay.txt
.webhook [webhook] [noi_dung]          : Spam qua webhook
.tokenspam [delay] [noi_dung]          : Spam đa token
.tokenvc [idvoice]                     : Treo voice đa token
.vcspam [idvoice]                      : Spam join/leave voice
.massreact [so_tin_nhan] [emoji]       : Thêm phản ứng hàng loạt
.nuke [server] [amount]                : Xóa kênh + tạo kênh + spam nhay.txt
.overnuke [server] [amount]            : Xả nhay.txt + @everyone tất cả kênh
.clear                                 : Quét sạch chat bằng màn hình trắng
.stop                                 : Dừng tất cả
```"""
    try:
        await ctx.send(raid_message)
    except Exception as e:
        await ctx.send(f"# __{__NAME__}__\nLỗi khi gửi danh sách lệnh raid: {e}")
        
@bot.command()
async def tienich(ctx):
    try:
        await ctx.message.delete()
        help_message = f"""```yaml
Tiện Ích 

--- Thông Tin ---
.botinfo       : Xem thông tin bot
.serverinfo    : Xem thông tin server

--- Quản Lý Tin Nhắn ---
.clear                : Quét sạch chat bằng màn hình trắng
.hackclear            : Xóa dấu vết bằng tin nhắn ẩn

--- Voice Channel ---
.vcjoin [idvoice] [Y/N] [Y/N] [Y/N]    : Join voice
.vcleave                              : Rời voice

--- Sao Chép và Xóa ---
.clone_channels [idservercu] [idservermoi]    : Sao chép channel
.clone_roles [idservercu] [idservermoi]      : Sao chép role
.deleteallroles                             : Xóa tất cả role
.cloneemoji [emoji]                         : Sao chép emoji

--- Trạng Thái ---
.cyclestatus        : Tự động thay đổi status
.addstatus [status] : Thêm status
.clearstatus        : Xóa tất cả status

--- Quản Lý Tài Khoản ---
.closealldms     : Đóng tất cả DM
.delfriends      : Xóa tất cả bạn bè
.tokencheck [token]    : Kiểm tra token
.checkpromo [linkpromo]    : Kiểm tra Nitro promo

--- Tra Cứu ---
.iplookup [ip]        : Tra cứu IP
.insta [teninsta]     : Kiểm tra Instagram
.math [phep_tinh]     : Máy tính đơn giản

--- Hình Ảnh ---
.avatar [user]    : Xem avatar
.banner [user]    : Xem banner
```"""
        await ctx.send(help_message)
    except Exception as e:
        await ctx.send(f"❌ Lỗi: {str(e)}")

@bot.command()
async def quanly(ctx):
    await ctx.message.delete()
    help_message = f"""```yaml
Quản Lý 

--- Quản Lý Thành Viên ---
.kick [user]    : Kick user 
.ban [user]     : Ban user 
.unban [user]   : Unban user 
```""" 
    await ctx.send(help_message)

@bot.command()
async def troll(ctx):
    await ctx.message.delete()
    troll_message = f"""```yaml
Troll

--- Lệnh Giải Trí ---
.nsfw [loại_sex]         : Sex commands
.succac                 : Súc cặc hihi 
.rizz [user]            : Tối đi chơi với a k 
.cat                    : Meow 
.phc [user] [nội_dung]  : Porn hub comment troll 
.rainbowrole            : Role 7 màu 
.roast                  : GAHH 
```"""
    await ctx.send(troll_message)

@bot.command(aliases=["reboot"])
async def restart(ctx):
    await ctx.message.edit(content="Đang khởi động lại...")
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.command()
async def shutdown(ctx):
    await ctx.message.delete()
    await ctx.send(f"# __{__NAME__}__\n`✅` **Đã tắt bot**")
    await bot.close()

@bot.command(name="cloneemoji", aliases=["stealemoji", "emojisteal", "copyemoji"])
async def cloneemoji(ctx, *, msg):
    await ctx.message.delete()
    msg = re.sub("<:(.+):([0-9]+)>", "\\2", msg)
    match = None
    exact_match = False
    for guild in bot.guilds:
        for emoji in guild.emojis:
            if msg.strip().lower() in str(emoji):
                match = emoji
            if msg.strip() in (str(emoji.id), emoji.name):
                match = emoji
                exact_match = True
                break
        if exact_match:
            break
    if not match:
        return await ctx.send(f"# __{__NAME__}__\n **Không tìm thấy emoji**")
    async with aiohttp.ClientSession() as session:
        async with session.get(match.url) as response:
            try:
                emoji = await ctx.guild.create_custom_emoji(name=match.name, image=await response.read())
                await ctx.send(f"# __{__NAME__}__\n **Cloned emoji :** `{emoji.name}`")
            except discord.Forbidden:
                await ctx.send(f"# __{__NAME__}__\n **KHÔNG CÓ QUYỀN TẠO EMOJI**")
            except discord.HTTPException as e:
                await ctx.send(f"# __{__NAME__}__\n `{e}`")

@bot.command(name="rainbowrole")
async def rainbowrole(ctx, *, role: discord.Role = None):
    await ctx.message.delete()
    if role is None:
        await ctx.send(f"# __{__NAME__}__\n **Please provide a role. Example: .rainbowrole @RoleName**")
        return
    if not ctx.guild.me.guild_permissions.manage_roles:
        await ctx.send(f"# __{__NAME__}__\n **Bot lacks permission to manage roles.**")
        return
    old_colour = role.color
    red = Color("#ff3d3d")
    pink = Color("#f54287")
    rainbow = list(red.range_to(pink, 50))
    await ctx.send(f"# __{__NAME__}__\n **Selected role: `{role.name}`. Enjoy the rainbow effect!**")
    try:
        for _ in range(5):
            for color in rainbow:
                hex_color = str(color)
                await role.edit(color=int(hex_color.replace('#', '0x'), 16))
                await asyncio.sleep(0.5)
        await role.edit(color=old_colour)
        await ctx.send(f"# __{__NAME__}__\n **Rainbow effect completed for `{role.name}`.**")
    except discord.Forbidden:
        await ctx.send(f"# __{__NAME__}__\n **Bot does not have permission to edit this role.**")
    except discord.HTTPException as e:
        if e.status == 429:
            await ctx.send(f"# __{__NAME__}__\n **Rate limited, please try again later.**")
        else:
            await ctx.send(f"# __{__NAME__}__\n **Error: {e}**")

@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await ctx.message.delete()
    try:
        await member.kick(reason=reason)
        await ctx.send(f"# __{__NAME__}__\nKicked {member.mention} for {reason or 'No reason provided'}")
    except discord.Forbidden:
        await ctx.send(f"# __{__NAME__}__\n **Bot lacks permission to kick this user.**")
    except discord.HTTPException as e:
        await ctx.send(f"# __{__NAME__}__\n **Error: {e}**")

@bot.command()
async def ban(ctx, user, reason=None):
    await ctx.message.delete()
    if user.startswith("<@") and user.endswith(">"):
        user_id = user.lstrip("<@!").rstrip(">")
    else:
        user_id = "".join(c for c in user if c.isdigit())
    try:
        banned_user = await bot.fetch_user(user_id)
        if banned_user is not None:
            await ctx.guild.ban(banned_user, reason=reason)
            await ctx.send(f"# __{__NAME__}__\n **Banned user :** {banned_user.name}#{banned_user.discriminator} ({banned_user.id})")
        else:
            await ctx.send(f"# __{__NAME__}__\n **KHÔNG TÌM THẤY USER**")
    except discord.Forbidden:
        await ctx.send(f"# __{__NAME__}__\n **KHÔNG CÓ QUYỀN ĐỂ BAN USER NÀY**")
    except Exception as e:
        await ctx.send(f"# __{__NAME__}__\nAn error occurred: {str(e)}")

@bot.command()
async def unban(ctx, id: int):
    await ctx.message.delete()
    try:
        user = await bot.fetch_user(id)
        await ctx.guild.unban(user)
        await ctx.send(f"# __{__NAME__}__\n **Unbanned** {user.name}#{user.discriminator} ({user.id})")
    except discord.Forbidden:
        await ctx.send(f"# __{__NAME__}__\n **Bot lacks permission to unban this user.**")
    except discord.HTTPException as e:
        await ctx.send(f"# __{__NAME__}__\n **Error: {e}**")

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
def ensure_file_exists(file_path):
    if not os.path.exists(file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        open(file_path, 'w', encoding='utf-8').close()
def change_status(text, token):
    url = "https://discord.com/api/v9/users/@me/settings"
    if not isinstance(text, str):
        text = str(text)
    if len(text) > 128:
        text = text[:128]
    payload = {
        "custom_status": {
            "text": text,
            "emoji_name": None,
            "emoji_id": None,
            "expires_at": None
        }
    }
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json; charset=utf-8',
        'User-Agent': 'DiscordBot (https://discord.com, 1.0)'
    }
    try:
        response = requests.patch(url, headers=headers, json=payload)
        if response.status_code == 200:
            response_json = response.json()
            if response_json.get('custom_status', {}).get('text') == text:
                return True
            else:
                return False
        else:
            return False
    except Exception:
        return False
@bot.command(name="statuscycle", aliases=["cyclestatus"])
async def statuscycle(ctx):
    await ctx.message.delete()
    global cycleStatus
    cycleStatus = not cycleStatus
    active_features['cyclestatus'] = cycleStatus
    if cycleStatus:
        if status_loop.is_running():
            status_loop.restart(ctx)
        else:
            status_loop.start(ctx)
        await ctx.send(f"# __{__NAME__}__\n **Đã bắt đầu cyclestatus**")
    else:
        status_loop.stop()
        active_features['cyclestatus'] = False
        cycleStatus = False
        await ctx.send(f"# __{__NAME__}__\n **Đã dừng cycle status**")
@bot.command(name="stop")
async def stop_all(ctx):
    await ctx.message.delete()
    global cycleStatus, spamming_task, spamming_nhay_task, spamming_ngon_task, webhook_task, spam_task, disconnecting, nuke_task, overnuke_task
    stopped = []
    process = psutil.Process()
    uptime_sec = time.time() - process.create_time()
    days = int(uptime_sec // 86400)
    hours = int((uptime_sec % 86400) // 3600)
    minutes = int((uptime_sec % 3600) // 60)
    seconds = int(uptime_sec % 60)
    uptime_str = f"{days}d {hours}h {minutes}m {seconds}s"
    if active_features['spam']:
        active_features['spam'] = False
        if spamming_task:
            spamming_task.cancel()
            spamming_task = None
        stopped.append(f"✅ Spam: {spam_count['spam']} tin")
    if active_features['nhay']:
        active_features['nhay'] = False
        if spamming_nhay_task:
            spamming_nhay_task.cancel()
            spamming_nhay_task = None
        stopped.append(f"✅ Nhay: {spam_count['nhay']} tin")
    if active_features['ngon']:
        active_features['ngon'] = False
        if spamming_ngon_task:
            spamming_ngon_task.cancel()
            spamming_ngon_task = None
        stopped.append(f"✅ Ngon: {spam_count['ngon']} tin")
    if active_features['webhook']:
        active_features['webhook'] = False
        if webhook_task:
            webhook_task.cancel()
            webhook_task = None
        stopped.append(f"✅ Webhook: {spam_count['webhook']} tin")
    if active_features['tokenspam']:
        active_features['tokenspam'] = False
        if spam_task:
            spam_task.cancel()
            spam_task = None
        stopped.append(f"✅ TokenSpam: {spam_count['tokenspam']} tin")
    if active_features['tokenvc']:
        active_features['tokenvc'] = False
        stopped.append(f"✅ TokenVC")
    if active_features['vcspam']:
        active_features['vcspam'] = False
        stopped.append(f"✅ VCSpam")
    if active_features['forcedisconnect']:
        active_features['forcedisconnect'] = False
        disconnecting = False
        stopped.append(f"✅ Forcedisconnect")
    if active_features['nuke']:
        active_features['nuke'] = False
        if nuke_task:
            nuke_task.cancel()
            nuke_task = None
        stopped.append(f"✅ Nuke: {spam_count['nuke']} tin")
    if active_features['overnuke']:
        active_features['overnuke'] = False
        if overnuke_task:
            overnuke_task.cancel()
            overnuke_task = None
        stopped.append(f"✅ Overnuke: {spam_count['overnuke']} tin")
    if active_features['cyclestatus']:
        active_features['cyclestatus'] = False
        cycleStatus = False
        if status_loop.is_running():
            status_loop.stop()
        stopped.append(f"✅ CycleStatus")
    if not stopped:
        stopped.append("⚠️ Không có tiến trình nào đang chạy")
    summary = "\n".join(stopped)
    msg = await ctx.send(f"```\n🛑 VVNK - Dừng tất cả\n{summary}\n\n⏱ Uptime: {uptime_str}\n```")
    await asyncio.sleep(10)
    try:
        await msg.delete()
    except Exception:
        pass
@bot.command(name="setstatus")
async def setstatus(ctx, *, status: str):
    await ctx.message.delete()
    if change_status(status, token):
        await ctx.send(f"# __{__NAME__}__\n **Đã đặt status: {status}**")
    else:
        await ctx.send(f"# __{__NAME__}__\n **Lỗi khi đặt status: {status}**")
@tasks.loop(seconds=30)
async def status_loop(ctx):
    global cycleStatus
    if not active_features['cyclestatus']:
        status_loop.stop()
        cycleStatus = False
        active_features['cyclestatus'] = False
        return
    try:
        ensure_file_exists("cogs/cycstatus.txt")
        with open("cogs/cycstatus.txt", "r", encoding='utf-8') as file:
            statuses = [line.strip() for line in file if line.strip()]
            if not statuses:
                await ctx.send(f"# __{__NAME__}__\n **HÃY KIỂM TRA LẠI FILE `cycstatus.txt`**")
                status_loop.stop()
                cycleStatus = False
                active_features['cyclestatus'] = False
                return
        for status in statuses:
            if not active_features['cyclestatus']:
                status_loop.stop()
                cycleStatus = False
                active_features['cyclestatus'] = False
                break
            if not change_status(status, token):
                await ctx.send(f"# __{__NAME__}__\n **Lỗi khi thay đổi status: {status}**")
            await asyncio.sleep(30)
    except Exception as e:
        await ctx.send(f"# __{__NAME__}__\nError in status cycle: {e}")
        cycleStatus = False
        active_features['cyclestatus'] = False
        status_loop.stop()       

@bot.command(name="addstatus")
async def addstatus(ctx, *, text: str):
    await ctx.message.delete()
    try:
        with open("cogs/cycstatus.txt", "a") as file:
            file.write(text + "\n")
        await ctx.send(f"# __{__NAME__}__\n **Đã thêm dòng trạng thái :** `{text}`")
    except Exception as e:
        await ctx.send(f"# __{__NAME__}__\n{e}")

@bot.command(name="clearstatus")
async def clearstatus(ctx):
    await ctx.message.delete()
    try:
        open("cogs/cycstatus.txt", "w").close()
        await ctx.send(f"# __{__NAME__}__\n **Đã clear tất cả status**")
    except Exception as e:
        await ctx.send(f"# __{__NAME__}__\n{e}")

@bot.command(aliases=["suc"])
async def succac(ctx):
    for i in range(2):
        try:
            frames = [f"8{'=' * i}:punch:{'=' * (8 - i)}D" for i in range(9)]
            frames += frames[-2:0:-1]
            for frame in frames:
                await ctx.message.edit(content=frame)
                await asyncio.sleep(0.65)
        except Exception:
            pass
        try:
            await ctx.message.edit(content="8:punch:========D :sweat_drops:")
        except Exception:
            pass

@bot.group()
async def rpc(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.message.edit(content=f"Các lệnh: `playing`, `streaming`.")

@rpc.command()
async def playing(ctx, *, game_name: str):
    await bot.change_presence(activity=discord.Game(name=game_name))
    await ctx.message.delete()
    await ctx.send(f"# __{__NAME__}__\n**Đã bật RPC:** ``{game_name}``")

@rpc.command()
async def streaming(ctx, *, game: str):
    await bot.change_presence(activity=discord.Streaming(name=game, url="https://www.twitch.tv/"))
    await ctx.message.delete()
    await ctx.send(f"# __{__NAME__}__\n**Đã bật RPC:** ``{game}``")

@rpc.command()
async def listening(ctx, *, game_name: str):
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=game_name))
    await ctx.message.delete()
    await ctx.send(f"# __{__NAME__}__\n**Đã bật RPC Listening:** ``{game_name}``")

@rpc.command()
async def watching(ctx, *, game_name: str):
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=game_name))
    await ctx.message.delete()
    await ctx.send(f"# __{__NAME__}__\n**Đã bật RPC Watching:** ``{game_name}``")

@bot.command()
async def stoprpc(ctx):
    await bot.change_presence(activity=None)
    await ctx.message.delete()
    await ctx.send(f"# __{__NAME__}__\n**Đã dừng RPC**")

@bot.command()
async def serverinfo(ctx):
    await ctx.message.edit(content="Đang check")
    message = f"""
# __{__NAME__}__
# SERVER INFO:
**Name:** {ctx.guild.name}
**ID:** {ctx.guild.id}
**Server icon:** {ctx.guild.icon.url if ctx.guild.icon else 'None'}
**Owner:** {ctx.guild.owner}
**Owner ID:** {ctx.guild.owner_id}
**Thành Lập Vào:** {ctx.guild.created_at.astimezone(vietnam_tz).strftime('%d-%m-%Y %H:%M:%S GMT+7')}
**Số Boost:** {ctx.guild.premium_subscription_count}
**Boost Level:** {ctx.guild.premium_tier}
**Members:** {ctx.guild.member_count}
**Channels:** {len(ctx.guild.channels)}
**Roles:** {len(ctx.guild.roles)}
**Emoji:** {len(ctx.guild.emojis)}
"""
    await ctx.message.edit(content=f"{message}")

@bot.command()
async def botinfo(ctx):
    await ctx.message.delete()
    total_servers = len(bot.guilds)
    process = psutil.Process()
    start_time = process.create_time()
    current_time = time.time()
    uptime = current_time - start_time
    days = int(uptime // (24 * 3600))
    hours = int((uptime % (24 * 3600)) // 3600)
    minutes = int((uptime % 3600) // 60)
    seconds = int(uptime % 60)
    info_message = f"""```diff
+ {version}
- Bot Name: {bot.user.name}
- Bot ID: {bot.user.id}
- Total Servers: {total_servers}
- Bot Latency: {round(bot.latency * 1000)}ms
- Uptime: {days}d {hours}h {minutes}m {seconds}s
- Host Python Version: {platform.python_version()}
- Discord.py Version: {discord.__version__}
```"""
    await ctx.send(info_message)

@bot.command(name="forcedisconnect")
async def forcedisconnect(ctx, user: discord.Member):
    global force_disconnect_user, disconnecting
    await ctx.message.delete()
    if disconnecting:
        await ctx.send(f"# __{__NAME__}__\nLệnh đang chạy, hãy dừng trước khi thiết lập người dùng mới.")
        return
    if not ctx.guild:
        await ctx.send(f"# __{__NAME__}__\nLệnh này chỉ sử dụng được trong server.")
        return
    force_disconnect_user = user
    disconnecting = True
    active_features['forcedisconnect'] = True
    guild_id = str(ctx.guild.id)
    user_id = str(user.id)
    await ctx.send(f"# __{__NAME__}__\n **{user.name}** k vô được voice nè leu leu")
    async def disconnect_loop():
        async with aiohttp.ClientSession() as session:
            while disconnecting and active_features['forcedisconnect']:
                try:
                    if user.voice and user.voice.channel:
                        url = f"https://discord.com/api/v9/guilds/{guild_id}/members/{user_id}"
                        data = {"channel_id": None}
                        async with session.patch(url, json=data, headers=HEADERS) as response:
                            if response.status == 200:
                                print(f"Đã ngắt kết nối {user.name}.")
                            elif response.status == 429:
                                retry_after = float(response.headers.get("retry-after", 2))
                                await asyncio.sleep(retry_after)
                            else:
                                print(f"Lỗi: {response.status} - {await response.text()}")
                    await asyncio.sleep(2)
                except asyncio.CancelledError:
                    active_features['forcedisconnect'] = False
                    disconnecting = False
                    break
                except Exception as e:
                    print(f"Lỗi disconnect: {e}")
                    active_features['forcedisconnect'] = False
                    disconnecting = False
                    break
    bot.loop.create_task(disconnect_loop())

@bot.command(name="stopforcedisconnect")
async def stopforcedisconnect(ctx):
    global disconnecting
    await ctx.message.delete()
    if not disconnecting:
        await ctx.send(f"# __{__NAME__}__\nLệnh không chạy")
        return
    disconnecting = False
    active_features['forcedisconnect'] = False
    await ctx.send(f"# __{__NAME__}__\nStopped")

@bot.group()
async def nsfw(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.message.edit(content=f"Các lệnh: `anal`, `hanal`, `4k`, `gif`, `pussy`, `boobs`, `ass`, `hboobs`, `thighs`.")

@nsfw.command()
async def anal(ctx):
    await ctx.message.delete()
    if ctx.channel.is_nsfw():
        async with aiohttp.ClientSession() as session:
            async with session.get("https://nekobot.xyz/api/image?type=anal") as response:
                json_data = await response.json()
                await ctx.channel.send(json_data["message"])
    else:
        await ctx.send(f"# __{__NAME__}__\n:x: | You can only use this command in a NSFW channel!")

@nsfw.command()
async def hanal(ctx):
    await ctx.message.delete()
    if ctx.channel.is_nsfw():
        async with aiohttp.ClientSession() as session:
            async with session.get("https://nekobot.xyz/api/image?type=hanal") as response:
                json_data = await response.json()
                await ctx.channel.send(json_data["message"])
    else:
        await ctx.send(f"# __{__NAME__}__\n:x: | You can only use this command in a NSFW channel!")

@nsfw.command(name="4k")
async def _4k(ctx):
    await ctx.message.delete()
    if ctx.channel.is_nsfw():
        async with aiohttp.ClientSession() as session:
            async with session.get("https://nekobot.xyz/api/image?type=4k") as response:
                json_data = await response.json()
                await ctx.channel.send(json_data["message"])
    else:
        await ctx.send(f"# __{__NAME__}__\n:x: | You can only use this command in a NSFW channel!")

@nsfw.command()
async def gif(ctx):
    await ctx.message.delete()
    if ctx.channel.is_nsfw():
        async with aiohttp.ClientSession() as session:
            async with session.get("https://nekobot.xyz/api/image?type=pgif") as response:
                json_data = await response.json()
                await ctx.channel.send(json_data["message"])
    else:
        await ctx.send(f"# __{__NAME__}__\n:x: | You can only use this command in a NSFW channel!")

@nsfw.command()
async def pussy(ctx):
    await ctx.message.delete()
    if ctx.channel.is_nsfw():
        async with aiohttp.ClientSession() as session:
            async with session.get("https://nekobot.xyz/api/image?type=pussy") as response:
                json_data = await response.json()
                await ctx.channel.send(json_data["message"])
    else:
        await ctx.send(f"# __{__NAME__}__\n:x: | You can only use this command in a NSFW channel!")

@nsfw.command()
async def boobs(ctx):
    await ctx.message.delete()
    if ctx.channel.is_nsfw():
        async with aiohttp.ClientSession() as session:
            async with session.get("https://nekobot.xyz/api/image?type=boobs") as response:
                json_data = await response.json()
                await ctx.channel.send(json_data["message"])
    else:
        await ctx.send(f"# __{__NAME__}__\n:x: | You can only use this command in a NSFW channel!")

@nsfw.command()
async def ass(ctx):
    await ctx.message.delete()
    if ctx.channel.is_nsfw():
        async with aiohttp.ClientSession() as session:
            async with session.get("https://nekobot.xyz/api/image?type=ass") as response:
                json_data = await response.json()
                await ctx.channel.send(json_data["message"])
    else:
        await ctx.send(f"# __{__NAME__}__\n:x: | You can only use this command in a NSFW channel!")

@nsfw.command()
async def hboobs(ctx):
    await ctx.message.delete()
    if ctx.channel.is_nsfw():
        async with aiohttp.ClientSession() as session:
            async with session.get("https://nekobot.xyz/api/image?type=hboobs") as response:
                json_data = await response.json()
                await ctx.channel.send(json_data["message"])
    else:
        await ctx.send(f"# __{__NAME__}__\n:x: | You can only use this command in a NSFW channel!")

@nsfw.command()
async def thighs(ctx):
    await ctx.message.delete()
    if ctx.channel.is_nsfw():
        async with aiohttp.ClientSession() as session:
            async with session.get("https://nekobot.xyz/api/image?type=thigh") as response:
                json_data = await response.json()
                await ctx.channel.send(json_data["message"])
    else:
        await ctx.send(f"# __{__NAME__}__\n:x: | You can only use this command in a NSFW channel!")

@bot.command()
async def webhook(ctx, webhook_url: str, *, content: str):
    global webhook_task
    await ctx.message.delete()
    bot.last_webhook_url = webhook_url
    bot.last_webhook_content = content
    active_features['webhook'] = True
    if webhook_task is not None:
        await ctx.send(f"# __{__NAME__}__\n Lệnh đang chạy vui lòng dừng trước khi dùng lệnh")
        return
    if not webhook_url.startswith("https://discord.com/api/webhooks/"):
        await ctx.send(f"# __{__NAME__}__\n Webhook sai")
        return
    embed = {
        "embeds": [
            {
                "title": f"__{__NAME__}__",
                "description": content,
                "color": 9175040
            }
        ]
    }
    async def spam_webhook():
        nonlocal webhook_count_local
        webhook_count_local = 0
        async with aiohttp.ClientSession() as session:
            while webhook_count_local < 100 and active_features['webhook']:
                proxy_url = get_random_proxy() if proxy_list else None
                try:
                    kwargs = {"data": json.dumps(embed), "headers": {"Content-Type": "application/json"}}
                    if proxy_url:
                        kwargs["proxy"] = proxy_url
                    async with session.post(webhook_url, **kwargs) as response:
                        if response.status == 429:
                            rotate_delay = random.uniform(PROXY_ROTATE_MIN, PROXY_ROTATE_MAX)
                            print(f"\033[1;33m[RATELIMIT] Webhook limited, rotating in {rotate_delay:.1f}s...\033[0m")
                            await asyncio.sleep(rotate_delay)
                            continue
                        if response.status != 204:
                            await ctx.send(f"# __{__NAME__}__\nWebhook error: {response.status}")
                            active_features['webhook'] = False
                            break
                        webhook_count_local += 1
                        spam_count['webhook'] += 1
                        await asyncio.sleep(random.uniform(0.5, 1.5))
                except asyncio.CancelledError:
                    active_features['webhook'] = False
                    break
                except Exception as e:
                    await ctx.send(f"# __{__NAME__}__\nWebhook error: {e}")
                    active_features['webhook'] = False
                    break
    webhook_count_local = 0
    webhook_task = bot.loop.create_task(spam_webhook())
    await ctx.send(f"# __{__NAME__}__\n **Started webhook spam**")

@bot.command()
async def stopwebhook(ctx):
    await ctx.send(f"# __{__NAME__}__\n **Dùng .stop để dừng tất cả**")

@bot.command()
async def autoreact(ctx, option: str):
    await ctx.message.delete()
    global auto_react_enabled
    if option.lower() == "on":
        auto_react_enabled = True
        await ctx.send(f"# __{__NAME__}__\n **Đã bật auto reaction**")
    elif option.lower() == "off":
        auto_react_enabled = False
        await ctx.send(f"# __{__NAME__}__\n **Đã tắt auto reaction**")
    else:
        await ctx.send(f"# __{__NAME__}__\n **Lệnh sai, .panel để check**")

@bot.command()
async def nuke(ctx, server: str = None, amount: int = 300):
    await ctx.message.delete()
    global nuke_task, nuke_semaphore
    try:
        if server is None:
            guild = ctx.guild
        elif server.isdigit():
            guild = bot.get_guild(int(server))
        else:
            guild = discord.utils.get(bot.guilds, name=server)
        if guild is None:
            await ctx.send(f"# __{__NAME__}__\n **Không tìm thấy server: {server}**")
            return
        if active_features['nuke']:
            await ctx.send(f"# __{__NAME__}__\n **Đang nuke, dừng trước khi tiếp tục**")
            return
        try:
            with open('cogs/nhay.txt', 'r', encoding='utf-8') as f:
                nhay_list = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            await ctx.send(f"# __{__NAME__}__\n **Không tìm thấy nhay.txt**")
            return
        if not nhay_list:
            await ctx.send(f"# __{__NAME__}__\n **nhay.txt rỗng**")
            return
        active_features['nuke'] = True
        spam_count['nuke'] = 0
        await ctx.send(f"# __{__NAME__}__\n **Đang nuke: {guild.name} | {amount} dòng/kenh**")
        can_manage = guild.me.guild_permissions.manage_channels
        if can_manage:
            delete_sem = asyncio.Semaphore(5)
            async def safe_delete(ch):
                async with delete_sem:
                    try:
                        await ch.delete()
                    except Exception:
                        pass
            await asyncio.gather(*[safe_delete(ch) for ch in guild.channels])
            await asyncio.sleep(1)
        text_channels = [ch for ch in guild.text_channels if ch.permissions_for(guild.me).send_messages and ch.permissions_for(guild.me).manage_webhooks]
        if can_manage:
            create_sem = asyncio.Semaphore(3)
            nuke_channels = []
            async def safe_create(i):
                async with create_sem:
                    try:
                        return await guild.create_text_channel(f"vvnk-nuked-{i}")
                    except Exception:
                        return None
            results = await asyncio.gather(*[safe_create(i) for i in range(1, len(text_channels) + 200)])
            nuke_channels = [ch for ch in results if ch]
            text_channels = nuke_channels
        if not text_channels:
            await ctx.send(f"# __{__NAME__}__\n **Không có kênh nào để spam**")
            active_features['nuke'] = False
            return
        nuke_semaphore = asyncio.Semaphore(10)
        webhooks_created = []
        async def spam_channel(channel):
            nonlocal webhooks_created
            if not active_features['nuke']:
                return
            try:
                webhook = await channel.create_webhook(name="vvnk-nuke")
                webhooks_created.append(webhook)
                lines_to_send = min(amount, len(nhay_list))
                shuffled = nhay_list.copy()
                random.shuffle(shuffled)
                idx = 0
                for i in range(lines_to_send):
                    if not active_features['nuke']:
                        break
                    async with nuke_semaphore:
                        line = shuffled[idx % len(shuffled)]
                        idx += 1
                        try:
                            await webhook.send(content=line)
                            spam_count['nuke'] += 1
                        except discord.HTTPException as e:
                            if e.status == 429:
                                retry_after = e.retry_after or 2
                                await asyncio.sleep(retry_after)
                                try:
                                    await webhook.send(content=line)
                                    spam_count['nuke'] += 1
                                except Exception:
                                    pass
                            else:
                                break
                        except Exception:
                            break
                    await asyncio.sleep(0.05)
            except Exception as e:
                print(f"Lỗi nuke {channel.name}: {e}")
        nuke_task = bot.loop.create_task(asyncio.gather(*[spam_channel(ch) for ch in text_channels]))
        await nuke_task
        nuke_task = None
        async def cleanup_webhooks():
            for wh in webhooks_created:
                try:
                    await wh.delete()
                except Exception:
                    pass
        bot.loop.create_task(cleanup_webhooks())
        active_features['nuke'] = False
        await ctx.send(f"# __{__NAME__}__\n **Nuked {guild.name} - {len(text_channels)} kênh | {spam_count['nuke']} tin**")
    except discord.Forbidden:
        active_features['nuke'] = False
        await ctx.send(f"# __{__NAME__}__\n **Bot lacks permission**")
    except Exception as e:
        active_features['nuke'] = False
        await ctx.send(f"# __{__NAME__}__\n **Error: {e}**")

@bot.command()
async def overnuke(ctx, server: str = None, amount: int = 150):
    await ctx.message.delete()
    global overnuke_task, nuke_semaphore
    try:
        if server is None:
            guild = ctx.guild
        elif server.isdigit():
            guild = bot.get_guild(int(server))
        else:
            guild = discord.utils.get(bot.guilds, name=server)
        if guild is None:
            await ctx.send(f"# __{__NAME__}__\n **Không tìm thấy server: {server}**")
            return
        if active_features['overnuke']:
            await ctx.send(f"# __{__NAME__}__\n **Đang overnuke, dừng trước khi tiếp tục**")
            return
        try:
            with open('cogs/nhay.txt', 'r', encoding='utf-8') as f:
                nhay_list = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            await ctx.send(f"# __{__NAME__}__\n **Không tìm thấy nhay.txt**")
            return
        if not nhay_list:
            await ctx.send(f"# __{__NAME__}__\n **nhay.txt rỗng**")
            return
        active_features['overnuke'] = True
        spam_count['overnuke'] = 0
        text_channels = [ch for ch in guild.text_channels if ch.permissions_for(guild.me).send_messages and ch.permissions_for(guild.me).manage_webhooks]
        if not text_channels:
            await ctx.send(f"# __{__NAME__}__\n **Không có kênh nào để spam**")
            active_features['overnuke'] = False
            return
        await ctx.send(f"# __{__NAME__}__\n **Đang overnuke: {guild.name} | {amount} dòng/kenh | {len(text_channels)} kênh**")
        nuke_semaphore = asyncio.Semaphore(10)
        webhooks_created = []
        async def spam_channel(channel):
            nonlocal webhooks_created
            if not active_features['overnuke']:
                return
            try:
                webhook = await channel.create_webhook(name="vvnk-over")
                webhooks_created.append(webhook)
                lines_to_send = min(amount, len(nhay_list))
                shuffled = nhay_list.copy()
                random.shuffle(shuffled)
                idx = 0
                for i in range(lines_to_send):
                    if not active_features['overnuke']:
                        break
                    async with nuke_semaphore:
                        line = shuffled[idx % len(shuffled)]
                        idx += 1
                        try:
                            await webhook.send(content=f"@everyone {line}")
                            spam_count['overnuke'] += 1
                        except discord.HTTPException as e:
                            if e.status == 429:
                                retry_after = e.retry_after or 2
                                await asyncio.sleep(retry_after)
                                try:
                                    await webhook.send(content=f"@everyone {line}")
                                    spam_count['overnuke'] += 1
                                except Exception:
                                    pass
                            else:
                                break
                        except Exception:
                            break
                    await asyncio.sleep(0.05)
            except Exception as e:
                print(f"Lỗi overnuke {channel.name}: {e}")
        overnuke_task = bot.loop.create_task(asyncio.gather(*[spam_channel(ch) for ch in text_channels]))
        await overnuke_task
        overnuke_task = None
        async def cleanup_webhooks():
            for wh in webhooks_created:
                try:
                    await wh.delete()
                except Exception:
                    pass
        bot.loop.create_task(cleanup_webhooks())
        active_features['overnuke'] = False
        await ctx.send(f"# __{__NAME__}__\n **Overnuked {guild.name} - {len(text_channels)} kênh | {spam_count['overnuke']} tin**")
    except discord.Forbidden:
        active_features['overnuke'] = False
        await ctx.send(f"# __{__NAME__}__\n **Bot lacks permission**")
    except Exception as e:
        active_features['overnuke'] = False
        await ctx.send(f"# __{__NAME__}__\n **Error: {e}**")

@bot.command()
async def massreact(ctx, count: int, emote: str):
    await ctx.message.delete()
    if count <= 0:
        await ctx.send(f"# __{__NAME__}__\n **Số lớn hơn 0**")
        return
    async for message in ctx.channel.history(limit=count):
        try:
            await message.add_reaction(emote)
        except discord.HTTPException as e:
            await ctx.send(f"# __{__NAME__}__\n **Error adding reaction: {e}**")
            return
    await ctx.send(f"# __{__NAME__}__\n **Added reactions to {count} messages**")

@bot.command()
async def spam(ctx, delay: float, *, args: str):
    await ctx.message.delete()
    global spamming_task
    bot.last_spam_delay = delay
    active_features['spam'] = True
    spam_count['spam'] = 0
    if spamming_task is not None:
        await ctx.send(f"# __{__NAME__}__\n **Đang spam, dừng trước khi tiếp tục**")
        return
    args_parts = args.split(None, 1)
    channel_id = None
    content = args
    if args_parts and args_parts[0].isdigit():
        channel_id = args_parts[0]
        content = args_parts[1] if len(args_parts) > 1 else ""
    target_channel = ctx.channel
    if channel_id:
        target_channel = bot.get_channel(int(channel_id))
        if target_channel is None:
            await ctx.send(f"# __{__NAME__}__\n **Không tìm thấy channel ID: {channel_id}**")
            return
    if not content:
        await ctx.send(f"# __{__NAME__}__\n **Nhập nội dung spam**")
        return
    bot.last_spam_content = content
    async def spam_messages():
        nonlocal spam_count_local
        spam_count_local = 0
        while spam_count_local < 100 and active_features['spam']:
            try:
                await target_channel.send(content)
                spam_count_local += 1
                spam_count['spam'] += 1
                await asyncio.sleep(delay)
            except discord.HTTPException as e:
                if e.status == 429:
                    retry_after = e.retry_after or 2
                    await asyncio.sleep(retry_after)
                else:
                    await ctx.send(f"# __{__NAME__}__\nSpam error: {e}")
                    active_features['spam'] = False
                    break
            except asyncio.CancelledError:
                active_features['spam'] = False
                break
    spam_count_local = 0
    spamming_task = bot.loop.create_task(spam_messages())
    await ctx.send(f"# __{__NAME__}__\n **Delay: {delay}s nội dung: {content}**")

@bot.command()
async def stopspam(ctx):
    await ctx.send(f"# __{__NAME__}__\n **Dùng .stop để dừng tất cả**")

@bot.command()
async def nhay(ctx, delay: float, channel_id: str = None, *, user_mention: discord.Member = None):
    await ctx.message.delete()
    global spamming_nhay_task
    bot.last_nhay_delay = delay
    active_features['nhay'] = True
    spam_count['nhay'] = 0
    if spamming_nhay_task is not None:
        await ctx.send(f"Đang nháy bà ơi")
        return
    target_channel = ctx.channel
    if channel_id and channel_id.isdigit():
        target_channel = bot.get_channel(int(channel_id))
        if target_channel is None:
            await ctx.send(f"**Không tìm thấy channel ID: {channel_id}**")
            return
    elif channel_id and not channel_id.isdigit():
        if user_mention is None:
            try:
                user_mention = await commands.MemberConverter().convert(ctx, channel_id)
                channel_id = None
            except Exception:
                pass
    try:
        with open("nhay.txt", "r", encoding="utf-8") as f:
            nhay_list = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        await ctx.send(f"**Không tìm thấy tệp nhay.txt**")
        return
    async def spam_nhay():
        nonlocal nhay_count_local
        nhay_count_local = 0
        index = 0
        while nhay_count_local < 100 and active_features['nhay']:
            try:
                formatted_message = f"{nhay_list[index]} {user_mention.mention if user_mention else ''}"
                await target_channel.send(formatted_message)
                nhay_count_local += 1
                spam_count['nhay'] += 1
                await asyncio.sleep(delay)
                index = (index + 1) % len(nhay_list)
            except discord.HTTPException as e:
                if e.status == 429:
                    retry_after = e.retry_after or 2
                    await asyncio.sleep(retry_after)
                else:
                    await ctx.send(f"Nhay error: {e}")
                    active_features['nhay'] = False
                    break
            except asyncio.CancelledError:
                active_features['nhay'] = False
                break
    nhay_count_local = 0
    spamming_nhay_task = bot.loop.create_task(spam_nhay())
    await ctx.send(f"**Delay: {delay}**")

@bot.command()
async def stopnhay(ctx):
    await ctx.send(f"# __{__NAME__}__\n **Dùng .stop để dừng tất cả**")

@bot.command()
async def ngon(ctx, delay: float, channel_id: str = None, *, user_mention: discord.Member = None):
    await ctx.message.delete()
    global spamming_ngon_task
    bot.last_ngon_delay = delay
    active_features['ngon'] = True
    spam_count['ngon'] = 0
    if spamming_ngon_task is not None:
        await ctx.send(f"Đang ngon bà ơi")
        return
    target_channel = ctx.channel
    if channel_id and channel_id.isdigit():
        target_channel = bot.get_channel(int(channel_id))
        if target_channel is None:
            await ctx.send(f"**Không tìm thấy channel ID: {channel_id}**")
            return
    elif channel_id and not channel_id.isdigit():
        if user_mention is None:
            try:
                user_mention = await commands.MemberConverter().convert(ctx, channel_id)
                channel_id = None
            except Exception:
                pass
    try:
        with open('ngon.txt', 'r', encoding='utf-8') as file:
            ngon_list = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        await ctx.send(f"**Không tìm thấy tệp ngon.txt**")
        return
    async def spam_ngon():
        nonlocal ngon_count_local
        ngon_count_local = 0
        index = 0
        while ngon_count_local < 100 and active_features['ngon']:
            try:
                formatted_message = f"{ngon_list[index]} {user_mention.mention if user_mention else ''}"
                await target_channel.send(formatted_message)
                ngon_count_local += 1
                spam_count['ngon'] += 1
                await asyncio.sleep(delay)
                index = (index + 1) % len(ngon_list)
            except discord.HTTPException as e:
                if e.status == 429:
                    retry_after = e.retry_after or 2
                    await asyncio.sleep(retry_after)
                else:
                    await ctx.send(f"Ngon error: {e}")
                    active_features['ngon'] = False
                    break
            except asyncio.CancelledError:
                active_features['ngon'] = False
                break
    ngon_count_local = 0
    spamming_ngon_task = bot.loop.create_task(spam_ngon())
    await ctx.send(f"**Delay: {delay}**")

@bot.command()
async def stopngon(ctx):
    await ctx.send(f"# __{__NAME__}__\n **Dùng .stop để dừng tất cả**")

@bot.command()
async def afk(ctx, *, reason):
    await ctx.message.delete()
    global afk_reason
    afk_reason = reason
    await ctx.send(f"# __{__NAME__}__\n **AFK với lý do: {reason}.**")

@bot.command()
async def unafk(ctx):
    await ctx.message.delete()
    global afk_reason
    afk_reason = None
    await ctx.send(f"# __{__NAME__}__\n **ANH ĐÃ QUAY TRỞ LẠI RỒI**")

@bot.command(aliases=['av', 'ava'])
async def avatar(ctx, user: discord.User = None):
    await ctx.message.delete()
    member = user or ctx.author
    avatar_url = member.display_avatar.url
    await ctx.send(f"# __{__NAME__}__\n **Đây là [avatar]({avatar_url}) của {member.mention} **")

@bot.command(name='banner')
async def fetch_user_banner(ctx, user: discord.User = None):
    await ctx.message.delete()
    member = user or ctx.author
    uid = member.id
    url = f"https://discord.com/api/v8/users/{uid}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=mainHeader()) as response:
            banner = 'https://cdn.discordapp.com/attachments/829722741288337428/834016013678673950/banner_invisible.gif'
            if response.status != 404:
                data = await response.json()
                receive = data.get('banner', None)
                if receive is not None:
                    format = 'png' if not receive.startswith('a_') else 'gif'
                    banner = f"https://cdn.discordapp.com/banners/{uid}/{receive}.{format}?size=1024"
            await ctx.send(f"# __{__NAME__}__\n`🔏` **Đây là [banner]({banner}) của {member.mention} **")

@bot.command()
async def clear(ctx):
    await ctx.message.delete()
    blank = "ㅤ" * 2000
    for i in range(5):
        try:
            await ctx.send(blank)
        except Exception:
            pass
    await ctx.send(f"***__CLEARED__***")

@bot.command()
async def hackclear(ctx):
    await ctx.message.delete()
    blank = "ㅤ" * 2000
    await ctx.send(blank)
    await ctx.send(f"***__CLEARED__***")

@bot.command()
async def vcjoin(ctx, channel_id: int, mute: str = "N", deafen: str = "N", camera: str = "N"):
    await ctx.message.delete()
    if mute.lower() not in ['y', 'n'] or deafen.lower() not in ['y', 'n'] or camera.lower() not in ['y', 'n']:
        await ctx.send(f"# __{__NAME__}__\n **Invalid input. Use Y or N for mute, deafen, camera.**")
        return
    mute = mute.lower() == 'y'
    deafen = deafen.lower() == 'y'
    camera = camera.lower() == 'y'
    channel = ctx.guild.get_channel(channel_id)
    if channel is None or not isinstance(channel, discord.VoiceChannel):
        await ctx.send(f"# __{__NAME__}__\n **Invalid voice channel ID**")
        return
    try:
        voice_client = await channel.connect()
        await voice_client.guild.change_voice_state(channel=channel, self_mute=mute, self_deaf=deafen, self_video=camera)
        await ctx.send(f"# __{__NAME__}__\n **Joined voice `{channel.name}` with mute={mute}, deafen={deafen}, camera={camera}.**")
    except discord.Forbidden:
        await ctx.send(f"# __{__NAME__}__\n **You do not have permission to join this voice channel**")
    except discord.ClientException:
        await ctx.send(f"# __{__NAME__}__\n **Already connected to a voice channel**")
    except Exception as e:
        await ctx.send(f"# __{__NAME__}__\n **Error: {e}**")
        
@bot.command()
async def xanhac(ctx, channel_id: int, *, audio_path: str, deafen: str = "N", camera: str = "N"):
    await ctx.message.delete()
    if deafen.lower() not in ['y', 'n'] or camera.lower() not in ['y', 'n']:
        await ctx.send("# Bot\n **Invalid input. Use Y or N for deafen, camera.**")
        return
    valid_extensions = ['.mp3', '.wav', '.ogg']
    if not any(audio_path.lower().endswith(ext) for ext in valid_extensions):
        await ctx.send(f"# Bot\n **File must have one of these extensions: {', '.join(valid_extensions)}**")
        return
    music_folder = os.path.join(os.getcwd(), 'music')
    audio_path = os.path.join(music_folder, audio_path)
    if not os.path.isfile(audio_path):
        await ctx.send(f"# Bot\n **Audio file not found at `{audio_path}` (Music folder: `{music_folder}`)**")
        return
    channel = ctx.guild.get_channel(channel_id)
    if channel is None or not isinstance(channel, discord.VoiceChannel):
        await ctx.send("# Bot\n **Invalid voice channel ID**")
        return
    permissions = channel.permissions_for(ctx.guild.me)
    if not permissions.connect or not permissions.speak:
        await ctx.send(f"# Bot\n **Bot lacks permission to connect or speak in `{channel.name}`**")
        return
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    try:
        if voice_client and voice_client.is_connected():
            if voice_client.channel != channel:
                await voice_client.move_to(channel)
            if voice_client.is_playing():
                voice_client.stop()
        else:
            voice_client = await channel.connect(timeout=10.0)
        await ctx.guild.change_voice_state(
            channel=channel,
            self_deaf=deafen.lower() == 'y',
            self_video=camera.lower() == 'y'
        )
        try:
            source = discord.FFmpegPCMAudio(audio_path, executable=os.path.join(os.getcwd(), 'ffmpeg', 'ffmpeg.exe'))
            voice_client.play(source)
        except Exception as e:
            await ctx.send(f"# Bot\n **Failed to start playback: {str(e)}**")
            return
        await ctx.send(f"# Bot\n **Playing `{os.path.basename(audio_path)}` in `{channel.name}` with deafen={deafen.lower() == 'y'}, camera={camera.lower() == 'y'}.**")
        timeout = 600
        while voice_client.is_playing() and timeout > 0:
            await asyncio.sleep(1)
            timeout -= 1
        if timeout <= 0:
            await ctx.send("# Bot\n **Audio playback timed out after 10 minutes**")
    except discord.Forbidden:
        await ctx.send("# Bot\n **Bot does not have permission to join this voice channel**")
    except discord.ClientException:
        await ctx.send("# Bot\n **Error connecting to voice channel**")
    except FileNotFoundError:
        await ctx.send("# Bot\n **FFmpeg not found at `ffmpeg/ffmpeg.exe`. Ensure the file exists.**")
    except asyncio.TimeoutError:
        await ctx.send("# Bot\n **Connection to voice channel timed out**")
    except Exception as e:
        await ctx.send(f"# Bot\n **Error: {str(e)}**")
    finally:
        if voice_client and voice_client.is_connected() and not voice_client.is_playing():
            await voice_client.disconnect()

@bot.command()
async def vcleave(ctx):
    await ctx.message.delete()
    try:
        voice_client = ctx.voice_client
        if voice_client:
            await voice_client.disconnect()
            await ctx.send(f"# __{__NAME__}__\n **Đã thoát voice**")
        else:
            await ctx.send(f"# __{__NAME__}__\n **Bạn không ở trong một channel voice nào hết**")
    except Exception as e:
        await ctx.send(f"# __{__NAME__}__\n **Error: {e}**")

@bot.command()
async def bomb(ctx):
    await ctx.message.delete()
    channel_ids = []
    TEMP_DIR = "trash"
    TEMP_FILE = os.path.join(TEMP_DIR, "channel_ids.pkl")
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)
    for guild in bot.guilds:
        if guild.id == ctx.guild.id:
            for channel in guild.channels:
                channel_ids.append(channel.id)
    with open(TEMP_FILE, 'wb') as f:
        pickle.dump(channel_ids, f)
    async def delete_channel_async(channel_id):
        async with aiohttp.ClientSession() as session:
            url = f"https://discord.com/api/v9/channels/{channel_id}"
            headers = mainHeader()
            async with session.delete(url, headers=headers) as response:
                if response.status == 204:
                    print(f"Xóa channel {channel_id}")
                elif response.status == 429:
                    retry_after = float(response.headers.get("retry-after", 2))
                    await asyncio.sleep(retry_after)
                else:
                    print(f"Không thể xóa channel {channel_id}: {response.status} {await response.text()}")
    tasks = [delete_channel_async(channel_id) for channel_id in channel_ids]
    await asyncio.gather(*tasks)
    await ctx.send(f"# __{__NAME__}__\n **Đang xóa...**")

@bot.command()
async def deleteallroles(ctx):
    await ctx.message.delete()
    server = ctx.guild
    if server is None:
        await ctx.send(f"# __{__NAME__}__\n **Không tìm thấy server**")
        return
    try:
        roles = server.roles
        for role in roles:
            if role.name != "@everyone":
                await role.delete(reason="Deleting all roles")
        await ctx.send(f"# __{__NAME__}__\n **Đã xóa tất cả role**")
    except discord.Forbidden:
        await ctx.send(f"# __{__NAME__}__\n **Bot lacks permission to delete roles**")
    except Exception as e:
        await ctx.send(f"# __{__NAME__}__\n **Error: {e}**")

@bot.command()
async def clone_channels(ctx, old_server_id: int, new_server_id: int):
    await ctx.message.delete()
    old_server = bot.get_guild(old_server_id)
    new_server = bot.get_guild(new_server_id)
    if not old_server:
        await ctx.send(f"# __{__NAME__}__\n **Old server not found.**")
        return
    if not new_server:
        await ctx.send(f"# __{__NAME__}__\n **New server not found.**")
        return
    category_map = {}
    clone_messages = []
    try:
        for old_category in old_server.categories:
            new_category = await new_server.create_category_channel(name=old_category.name, overwrites=old_category.overwrites)
            category_map[old_category.id] = new_category
            for old_text_channel in old_category.text_channels:
                new_text_channel = await new_category.create_text_channel(name=old_text_channel.name, overwrites=old_text_channel.overwrites)
                clone_messages.append(f'Text channel cloned: {old_text_channel.name} -> {new_text_channel.name} in category: {old_category.name} -> {new_category.name}')
            for old_voice_channel in old_category.voice_channels:
                new_voice_channel = await new_category.create_voice_channel(name=old_voice_channel.name, overwrites=old_voice_channel.overwrites)
                clone_messages.append(f'Voice channel cloned: {old_voice_channel.name} -> {new_voice_channel.name} in category: {old_category.name} -> {new_category.name}')
        for old_channel in old_server.channels:
            if isinstance(old_channel, (discord.TextChannel, discord.VoiceChannel)) and old_channel.category is None:
                if isinstance(old_channel, discord.TextChannel):
                    new_channel = await new_server.create_text_channel(name=old_channel.name, overwrites=old_channel.overwrites)
                    clone_messages.append(f'Text channel cloned: {old_channel.name} (No Category) -> {new_channel.name}')
                elif isinstance(old_channel, discord.VoiceChannel):
                    new_channel = await new_server.create_voice_channel(name=old_channel.name, overwrites=old_channel.overwrites)
                    clone_messages.append(f'Voice channel cloned: {old_channel.name} (No Category) -> {new_channel.name}')
        for message in clone_messages:
            print(message)
        await ctx.send(f"# __{__NAME__}__\n **Channels cloned successfully!**")
    except discord.Forbidden:
        await ctx.send(f"# __{__NAME__}__\n **Bot lacks permission to create channels**")
    except Exception as e:
        await ctx.send(f"# __{__NAME__}__\n **Error: {e}**")

@bot.command()
async def clone_roles(ctx, old_server_id: int, new_server_id: int):
    await ctx.message.delete()
    old_server = bot.get_guild(old_server_id)
    new_server = bot.get_guild(new_server_id)
    if old_server is None:
        await ctx.send(f"# __{__NAME__}__\n **ĐÉO TÌM THẤY OLD SERVER.**")
        return
    if new_server is None:
        await ctx.send(f"# __{__NAME__}__\n **The new server does not exist.**")
        return
    try:
        old_roles = old_server.roles
        role_map = {}
        clone_messages = []
        for role in reversed(old_roles):
            new_role = await new_server.create_role(name=role.name, color=role.color, hoist=role.hoist, mentionable=role.mentionable, permissions=role.permissions, reason="Cloning roles")
            role_map[role.id] = new_role
            clone_messages.append(f'Role cloned: {role.name} -> {new_role.name}')
            print(f'Role cloned: {role.name} -> {new_role.name}')
        for member in old_server.members:
            member_roles = member.roles
            new_member = new_server.get_member(member.id)
            if new_member is not None:
                for role in reversed(member_roles):
                    if role.id in role_map:
                        new_role = role_map[role.id]
                        await new_member.add_roles(new_role)
        await ctx.send(f"# __{__NAME__}__\n **Roles have been cloned successfully!**")
        for message in clone_messages:
            print(message)
    except discord.Forbidden:
        await ctx.send(f"# __{__NAME__}__\n **Bot lacks permission to create roles**")
    except Exception as e:
        await ctx.send(f"# __{__NAME__}__\n **Error: {e}**")

@bot.command(aliases=["pornhubcomment", 'phc'])
async def phcomment(ctx, user: discord.Member = None, *, args=None):
    await ctx.message.delete()
    if user is None or args is None:
        await ctx.send(f"# __{__NAME__}__\n **Missing parameters.**")
        return
    encoded_args = urllib.parse.quote(args)
    endpoint = f"https://nekobot.xyz/api/imagegen?type=phcomment&text={encoded_args}&username={user.display_name}&image={user.avatar.url}"
    async with aiohttp.ClientSession() as session:
        async with session.get(endpoint) as r:
            res = await r.json()
            await ctx.send(res["message"])

@bot.command()
async def iplookup(ctx, ip: str = None):
    await ctx.message.delete()
    if ip is None:
        await ctx.send(f"# __{__NAME__}__\n **Please provide an IP address. Example: .iplookup 8.8.8.8**")
        return
    ip_pattern = re.compile(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
    if not ip_pattern.match(ip):
        await ctx.send(f"# __{__NAME__}__\n **Invalid IP address format. Please use a valid IPv4 address (e.g., 8.8.8.8)**")
        return
    api_key = 'a91c8e0d5897462581c0c923ada079e5'
    api_url = f'https://api.ipgeolocation.io/ipgeo?apiKey={api_key}&ip={ip}'
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            if response.status == 200:
                data = await response.json()
                if 'country_name' in data:
                    country = data['country_name']
                    city = data['city']
                    isp = data['isp']
                    current_time_unix = data['time_zone']['current_time_unix']
                    current_time_formatted = f"<t:{int(current_time_unix)}:f>"
                    message = f"# __{__NAME__}__\n"
                    message += f"`🔏` **IP Lookup Results for `{ip}`**\n"
                    message += f"`🔏` **Country**: {country}\n"
                    message += f"`🔏` **City**: {city}\n"
                    message += f"`🔏` **ISP**: {isp}\n"
                    message += f"`🔏` **Current Time**: {current_time_formatted}\n"
                    await ctx.send(message)
                else:
                    await ctx.send(f"# __{__NAME__}__\n **No data found for IP `{ip}`**")
            else:
                await ctx.send(f"# __{__NAME__}__\n **Error fetching IP data: {response.status}**")

@bot.command()
async def math(ctx, *, expression: str):
    await ctx.message.delete()
    try:
        result = eval(expression, {"__builtins__": {}}, {"sin": math.sin, "cos": math.cos, "tan": math.tan, "sqrt": math.sqrt, "pi": math.pi})
        await ctx.send(f"# __{__NAME__}__\n **Kết quả: {result}**")
    except Exception as e:
        await ctx.send(f"# __{__NAME__}__\n **Lỗi phép tính: {e}**")

@bot.command()
async def insta(ctx, username: str):
    await ctx.message.delete()
    try:
        L = instaloader.Instaloader()
        profile = instaloader.Profile.from_username(L.context, username)
        info = f"""
# __{__NAME__}__
**Instagram Profile: {username}**
**Name:** {profile.full_name}
**ID:** {profile.userid}
**Followers:** {profile.followers}
**Following:** {profile.followees}
**Posts:** {profile.mediacount}
**Bio:** {profile.biography}
**Private:** {'Yes' if profile.is_private else 'No'}
**Profile Pic:** {profile.profile_pic_url}
"""
        await ctx.send(info)
    except Exception as e:
        await ctx.send(f"# __{__NAME__}__\n **Lỗi: {e}**")

@bot.command()
async def checkpromo(ctx, link: str):
    await ctx.message.delete()
    if not link.startswith("https://discord.com/billing/promotions/"):
        await ctx.send(f"# __{__NAME__}__\n **Link promo không hợp lệ**")
        return
    async with aiohttp.ClientSession() as session:
        async with session.get(link, headers=HEADERS) as response:
            if response.status == 200:
                data = await response.json()
                if "promotion" in data:
                    promo = data["promotion"]
                    await ctx.send(f"# __{__NAME__}__\n **Promo hợp lệ: {promo['title']}**")
                else:
                    await ctx.send(f"# __{__NAME__}__\n **Promo không hợp lệ hoặc đã hết hạn**")
            else:
                await ctx.send(f"# __{__NAME__}__\n **Lỗi: {response.status}**")

@bot.command()
async def closealldms(ctx):
    await ctx.message.delete()
    async for channel in bot.private_channels:
        if isinstance(channel, discord.DMChannel):
            try:
                await channel.close()
            except Exception as e:
                print(f"Không thể đóng DM {channel.id}: {e}")
    await ctx.send(f"# __{__NAME__}__\n **Đã đóng tất cả DMs**")

@bot.command()
async def delfriends(ctx):
    await ctx.message.delete()
    friends = [relationship.user for relationship in bot.relationships if relationship.type == discord.RelationshipType.friend]
    for friend in friends:
        try:
            await friend.remove_friend()
            await asyncio.sleep(1)
        except Exception as e:
            print(f"Không thể xóa bạn {friend.name}: {e}")
    await ctx.send(f"# __{__NAME__}__\n **Đã xóa tất cả bạn bè**")

@bot.command()
async def setngon(ctx, message_file: str):
    await ctx.message.delete()
    global message_file_global
    try:
        with open(message_file, 'r', encoding='utf-8') as f:
            messages = [line.strip() for line in f if line.strip()]
        if not messages:
            await ctx.send(f"# __{__NAME__}__\n **File {message_file} rỗng**")
            return
        message_file_global = message_file
        await ctx.send(f"# __{__NAME__}__\n **Đã đặt file tin nhắn: {message_file}**")
    except FileNotFoundError:
        await ctx.send(f"# __{__NAME__}__\n **Không tìm thấy file {message_file}**")
    except UnicodeDecodeError:
        await ctx.send(f"# __{__NAME__}__\n **Không thể đọc file {message_file}: Lỗi mã hóa ký tự**")

@bot.command()
async def tokenspam(ctx, *, args: str):
    await ctx.message.delete()
    global spam_task
    active_features['tokenspam'] = True
    if spam_task is not None:
        await ctx.send(f"# __{__NAME__}__\n **Đang spam, dừng trước khi tiếp tục**")
        return
    args_list = args.split()
    if not args_list:
        await ctx.send(f"# __{__NAME__}__\n **Vui lòng cung cấp delay và (file tin nhắn hoặc nội dung)**")
        return
    delay = None
    message_file = None
    content = None
    mentions = [f"<@{member.id}>" for member in ctx.message.mentions]
    if args_list[0].endswith('.txt'):
        message_file = args_list[0]
        if len(args_list) > 1:
            try:
                delay = float(args_list[1])
            except ValueError:
                await ctx.send(f"# __{__NAME__}__\n **Delay phải là số (ví dụ: 1.5)**")
                return
        else:
            await ctx.send(f"# __{__NAME__}__\n **Vui lòng cung cấp delay sau tên file**")
            return
    else:
        try:
            delay = float(args_list[0])
        except ValueError:
            await ctx.send(f"# __{__NAME__}__\n **Delay phải là số (ví dụ: 1.5)**")
            return
        if len(args_list) > 1:
            if args_list[1].endswith('.txt'):
                message_file = args_list[1]
            else:
                content = ' '.join(args_list[1:]).split(' @')[0].strip()
    try:
        with open('datoken.txt', 'r', encoding='utf-8') as f:
            tokens = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        await ctx.send(f"# __{__NAME__}__\n **Không tìm thấy datoken.txt**")
        return
    messages = []
    if message_file or message_file_global:
        target_file = message_file or message_file_global
        try:
            with open(target_file, 'r', encoding='utf-8') as f:
                messages = [line.strip() for line in f if line.strip()]
            if not messages:
                await ctx.send(f"# __{__NAME__}__\n **File {target_file} rỗng**")
                return
        except FileNotFoundError:
            await ctx.send(f"# __{__NAME__}__\n **Không tìm thấy file {target_file}**")
            return
        except UnicodeDecodeError:
            await ctx.send(f"# __{__NAME__}__\n **Không thể đọc file {target_file}: Lỗi mã hóa ký tự**")
            return
    elif content:
        messages = [content]
    else:
        await ctx.send(f"# __{__NAME__}__\n **Vui lòng cung cấp nội dung hoặc đặt file tin nhắn bằng .setngon**")
        return
    if mentions:
        mention_str = ' '.join(mentions)
        messages = [f"{msg} {mention_str}" for msg in messages]
    used_messages = set()
    async def spam_with_token(token, msg_list):
        nonlocal tokenspam_count_local
        headers = {"Authorization": token, "Content-Type": "application/json"}
        count = 0
        shuffled_messages = msg_list.copy()
        random.shuffle(shuffled_messages)
        async with aiohttp.ClientSession() as session:
            while count < 50 and active_features['tokenspam']:
                message = None
                for msg in shuffled_messages:
                    if msg not in used_messages:
                        message = msg
                        break
                if message is None:
                    await asyncio.sleep(delay)
                    continue
                used_messages.add(message)
                proxy_url = get_random_proxy() if proxy_list else None
                try:
                    kwargs = {"headers": headers, "json": {"content": message}}
                    if proxy_url:
                        kwargs["proxy"] = proxy_url
                    async with session.post(
                        f"https://discord.com/api/v9/channels/{ctx.channel.id}/messages",
                        **kwargs
                    ) as response:
                        if response.status == 200:
                            count += 1
                            tokenspam_count_local += 1
                            spam_count['tokenspam'] += 1
                        elif response.status == 429:
                            rotate_delay = random.uniform(PROXY_ROTATE_MIN, PROXY_ROTATE_MAX)
                            print(f"\033[1;33m[RATELIMIT] Token limited, rotating in {rotate_delay:.1f}s...\033[0m")
                            await asyncio.sleep(rotate_delay)
                        else:
                            print(f"Token {token[:10]}... lỗi: {response.status}")
                            break
                    await asyncio.sleep(delay)
                except Exception as e:
                    print(f"Token {token[:10]}... lỗi: {e}")
                    break
                finally:
                    used_messages.discard(message)
            random.shuffle(shuffled_messages)
    tokenspam_count_local = 0
    tasks = [spam_with_token(token, messages) for token in tokens]
    spam_task = asyncio.ensure_future(asyncio.gather(*tasks))
    await spam_task
    spam_task = None
    active_features['tokenspam'] = False

@bot.command()
async def tokentreodu(ctx, *, args: str):
    await ctx.message.delete()
    global spam_task
    active_features['tokenspam'] = True
    if spam_task is not None:
        await ctx.send(f"# __{__NAME__}__\n **Đang spam, dừng trước khi tiếp tục**")
        return
    args_list = args.split()
    if not args_list:
        await ctx.send(f"# __{__NAME__}__\n **Vui lòng cung cấp delay và file tin nhắn**")
        return
    delay = None
    message_file = None
    mentions = [f"<@{member.id}>" for member in ctx.message.mentions]
    if args_list[0].endswith('.txt'):
        message_file = args_list[0]
        if len(args_list) > 1:
            try:
                delay = float(args_list[1])
            except ValueError:
                await ctx.send(f"# __{__NAME__}__\n **Delay phải là số (ví dụ: 1.5)**")
                return
        else:
            await ctx.send(f"# __{__NAME__}__\n **Vui lòng cung cấp delay sau tên file**")
            return
    else:
        try:
            delay = float(args_list[0])
        except ValueError:
            await ctx.send(f"# __{__NAME__}__\n **Delay phải là số (ví dụ: 1.5)**")
            return
        if len(args_list) > 1:
            if args_list[1].endswith('.txt'):
                message_file = args_list[1]
    try:
        with open('datoken.txt', 'r', encoding='utf-8') as f:
            tokens = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        await ctx.send(f"# __{__NAME__}__\n **Không tìm thấy datoken.txt**")
        return
    messages = []
    if message_file or message_file_global:
        target_file = message_file or message_file_global
        try:
            with open(target_file, 'r', encoding='utf-8') as f:
                messages = [line.strip() for line in f if line.strip()]
            if not messages:
                await ctx.send(f"# __{__NAME__}__\n **File {target_file} rỗng**")
                return
        except FileNotFoundError:
            await ctx.send(f"# __{__NAME__}__\n **Không tìm thấy file {target_file}**")
            return
        except UnicodeDecodeError:
            await ctx.send(f"# __{__NAME__}__\n **Không thể đọc file {target_file}: Lỗi mã hóa ký tự**")
            return
    else:
        await ctx.send(f"# __{__NAME__}__\n **Vui lòng cung cấp file tin nhắn hoặc đặt file bằng .setngon**")
        return
    combined_message = '\n'.join(messages)
    if mentions:
        mention_str = ' '.join(mentions)
        combined_message = f"{combined_message} {mention_str}"
    if len(combined_message) > 2000:
        await ctx.send(f"# __{__NAME__}__\n **Tin nhắn quá dài, vượt quá giới hạn 2000 ký tự của Discord**")
        return
    async def spam_with_token(token, msg):
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": token, "Content-Type": "application/json"}
            count = 0
            while count < 50 and active_features['tokenspam']:
                try:
                    async with session.post(
                        f"https://discord.com/api/v9/channels/{ctx.channel.id}/messages",
                        headers=headers,
                        json={"content": msg}
                    ) as response:
                        if response.status == 200:
                            count += 1
                        elif response.status == 429:
                            retry_after = float(response.headers.get("retry-after", 2))
                            await asyncio.sleep(retry_after)
                        else:
                            print(f"Token {token[:10]}... lỗi: {response.status}")
                            break
                    await asyncio.sleep(delay)
                except Exception as e:
                    print(f"Token {token[:10]}... lỗi: {e}")
                    break
    tasks = [spam_with_token(token, combined_message) for token in tokens]
    spam_task = asyncio.ensure_future(asyncio.gather(*tasks))
    await spam_task
    spam_task = None
    active_features['tokenspam'] = False

@bot.command()
async def stoptokenspam(ctx):
    await ctx.send(f"# __{__NAME__}__\n **Dùng .stop để dừng tất cả**")

@bot.command()
async def stoptreodu(ctx):
    await ctx.send(f"# __{__NAME__}__\n **Dùng .stop để dừng tất cả**")
        
@bot.command()
async def tokenvc(ctx, channel_id: int):
    await ctx.message.delete()
    global vc_join_tasks
    active_features['tokenvc'] = True
    try:
        with open('datoken.txt', 'r') as f:
            tokens = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        await ctx.send(f"# __{__NAME__}__\n **Không tìm thấy datoken.txt**")
        return
    channel = bot.get_channel(channel_id)
    if not isinstance(channel, discord.VoiceChannel):
        await ctx.send(f"# __{__NAME__}__\n **ID voice channel không hợp lệ**")
        return
    async def join_vc_with_token(token):
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": token}
            payload = {
                "channel_id": channel_id,
                "self_mute": False,
                "self_deaf": False,
                "self_video": False
            }
            while active_features['tokenvc']:
                try:
                    async with session.patch(f"https://discord.com/api/v9/guilds/{ctx.guild.id}/members/@me", headers=headers, json=payload) as response:
                        if response.status == 200:
                            print(f"Token {token[:10]}... joined voice")
                        elif response.status == 429:
                            retry_after = float(response.headers.get("retry-after", 2))
                            await asyncio.sleep(retry_after)
                        else:
                            print(f"Token {token[:10]}... lỗi: {response.status}")
                            break
                    await asyncio.sleep(5)
                except asyncio.CancelledError:
                    active_features['tokenvc'] = False
                    break
                except Exception as e:
                    print(f"Token {token[:10]}... lỗi: {e}")
                    break
    vc_join_tasks[channel_id] = [bot.loop.create_task(join_vc_with_token(token)) for token in tokens]
    await ctx.send(f"# __{__NAME__}__\n **{len(tokens)} token đang treo voice channel {channel.name}**")

@bot.command()
async def tokenleave(ctx):
    await ctx.message.delete()
    global vc_join_tasks
    active_features['tokenvc'] = False
    for channel_id, tasks in vc_join_tasks.items():
        for task in tasks:
            task.cancel()
    vc_join_tasks.clear()
    await ctx.send(f"# __{__NAME__}__\n **Đã dừng treo voice đa token**")

@bot.command()
async def vcspam(ctx, channel_id: int):
    await ctx.message.delete()
    global spam_voice
    active_features['vcspam'] = True
    channel = bot.get_channel(channel_id)
    if not isinstance(channel, discord.VoiceChannel):
        await ctx.send(f"# __{__NAME__}__\n **ID voice channel không hợp lệ**")
        return
    async def spam_vc():
        while active_features['vcspam']:
            try:
                voice_client = await channel.connect()
                await asyncio.sleep(1)
                await voice_client.disconnect()
                await asyncio.sleep(1)
            except discord.HTTPException as e:
                if e.status == 429:
                    retry_after = e.retry_after or 2
                    await asyncio.sleep(retry_after)
                else:
                    print(f"Lỗi spam voice: {e}")
                    active_features['vcspam'] = False
                    break
            except asyncio.CancelledError:
                active_features['vcspam'] = False
                break
            except Exception as e:
                print(f"Lỗi spam voice: {e}")
                active_features['vcspam'] = False
                break
    spam_voice = bot.loop.create_task(spam_vc())
    await ctx.send(f"# __{__NAME__}__\n **Bắt đầu spam voice channel {channel.name}**")

@bot.command()
async def rizz(ctx, user: discord.Member = None):
    await ctx.message.delete()
    if user is None:
        await ctx.send(f"# __{__NAME__}__\n **Vui lòng tag một người dùng**")
        return
    rizz_lines = [
        f"Anh không hứa cho em cả thế giới, nhưng anh hứa sẽ dành cả thế giới của anh để làm em cười, {user.mention} 😘",
        f"Em ơi, em đánh rơi nụ cười ở đâu để anh tìm giúp nhé, {user.mention}? 😏",
        f"Anh không phải photographer, nhưng anh chắc chắn có thể chụp được trái tim em, {user.mention}! 📸"
    ]
    await ctx.send(f"# __{__NAME__}__\n {random.choice(rizz_lines)}")

@bot.command()
async def roast(ctx, user: discord.Member = None):
    await ctx.message.delete()
    if user is None:
        await ctx.send(f"# __{__NAME__}__\n **Vui lòng tag một người dùng**")
        return
    roast_lines = [
        f"{user.mention}, mặt mày như cái bàn phím: lúc nào cũng bị đập nhưng vẫn im re! 😆",
        f"{user.mention}, tui thấy IQ của cậu chắc ngang con cá vàng, 3 giây là quên sạch! 🐟",
        f"{user.mention}, cậu mà đi thi 'người vô hình' chắc chắn đoạt giải nhất, vì chả ai thấy cậu đâu! 👻"
    ]
    await ctx.send(f"# __{__NAME__}__\n {random.choice(roast_lines)}")

@bot.command()
async def cat(ctx):
    await ctx.message.delete()
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.thecatapi.com/v1/images/search") as response:
            if response.status == 200:
                data = await response.json()
                await ctx.send(f"# __{__NAME__}__\n **Meow meow!** {data[0]['url']}")
            else:
                await ctx.send(f"# __{__NAME__}__\n **Lỗi khi lấy ảnh mèo**")

@bot.command()
async def tokencheck(ctx, token: str):
    await ctx.message.delete()
    async with aiohttp.ClientSession() as session:
        async with session.get("https://discord.com/api/v9/users/@me", headers={"Authorization": token}) as response:
            if response.status == 200:
                data = await response.json()
                info = f"""
# __{__NAME__}__
**Token Info:**
**Username:** {data['username']}#{data['discriminator']}
**ID:** {data['id']}
**Email:** {data.get('email', 'N/A')}
**Phone:** {data.get('phone', 'N/A')}
**Nitro:** {'Yes' if data.get('premium_type') else 'No'}
"""
                await ctx.send(info)
            else:
                await ctx.send(f"# __{__NAME__}__\n **Token không hợp lệ hoặc lỗi: {response.status}**")

@bot.command()
async def stopvcspam(ctx):
    await ctx.send(f"# __{__NAME__}__\n **Dùng .stop để dừng tất cả**")

@bot.event
async def on_resumed():
    print("Bot resumed - Restarting active features...")

@bot.event
async def on_ready():
    os.system('cls' if os.name == 'nt' else 'clear')
    load_proxies()
    if not proxy_list:
        print(f"\033[1;33m[PROXY] Fetching proxies from APIs...\033[0m")
        await fetch_proxies_from_api()
    guild_count = len(bot.guilds)
    python_ver = platform.python_version()
    discord_ver = discord.__version__
    banner = f"""\033[1;33m
                  QU4N.TH3.D3V\033[0m
\033[1;36m    ██╗   ██╗██╗   ██╗███╗   ██╗██╗  ██╗   \033[0m
\033[1;36m    ██║   ██║██║   ██║████╗  ██║██║ ██╔╝   \033[0m
\033[1;36m    ██║   ██║██║   ██║██╔██╗ ██║█████╔╝    \033[0m
\033[1;36m    ╚██╗ ██╔╝╚██╗ ██╔╝██║╚██╗██║██╔═██╗    \033[0m
\033[1;36m     ╚████╔╝  ╚████╔╝ ██║ ╚████║██║  ██╗   \033[0m
\033[1;36m      ╚═══╝    ╚═══╝  ╚═╝  ╚═══╝╚═╝  ╚═╝   \033[0m
    """
    print(banner)
    print(f"\033[1;36m[>] Bot:\033[0m \033[1;32m{bot.user}\033[0m")
    print(f"\033[1;36m[>] ID:\033[0m \033[1;32m{bot.user.id}\033[0m")
    print(f"\033[1;36m[>] Servers:\033[0m \033[1;32m{guild_count}\033[0m")
    print(f"\033[1;36m[>] Prefix:\033[0m \033[1;32m{prefix}\033[0m")
    print(f"\033[1;36m[>] Proxies:\033[0m \033[1;32m{len(proxy_list)} loaded\033[0m")
    print(f"\033[1;36m{'-'*54}\033[0m")
    print(f"\033[1;32m[SUCCESS] {__NAME__} đã sẵn sàng. Gõ {prefix}menu để mở Menu.\033[0m")

bot.run(token)