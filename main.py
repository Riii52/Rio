import discord
from discord.ext import commands
import json
import os

# --- الإعدادات ---
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents, case_insensitive=True)

# --- البيانات ---
DATA_FILE = "toon_stats.json"
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f: return json.load(f)
        except: return {}
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f: json.dump(data, f, indent=4)

user_data = load_data()

# --- الآيديات ---
HOST_CHANNEL_ID = 1450459023617949747
GAME_ROLE_ID = 1450818743251894472
WELCOME_CHANNEL_ID = 1450798372100243517
GOODBYE_CHANNEL_ID = 1450799020556554240

LEVEL_ROLES = {
    1: 1483227597801521316, 4: 1483227645016674384, 6: 1483227734728773784,
    8: 1483227747563081841, 9: 1483227757981859950, 12: 1483227765669888092,
    14: 1483227776638255307, 16: 1483227784737460225, 20: 1483227826718249031
}

def calculate_level(score):
    if score <= 12: return score // 2
    elif score <= 24: return 6 + (score - 12) // 3
    elif score <= 44: return 10 + (score - 24) // 4
    else: return 15 + (score - 44) // 5

# --- الترحيب والتوديع ---
@bot.event
async def on_member_join(member):
    ch = bot.get_channel(WELCOME_CHANNEL_ID)
    if ch:
        emb = discord.Embed(title="Welcome to ໑ °. !!BASSIE WORLD Ꮺ ˚₊", description=f"⊹ ˖ \n ⚔️ . . welcome {member.mention} ! \n 🌸 ||| \n\n 🦋 𓋼 ᵎ 𓂃 <#1450798372100243517> 🎟️ \n\n <#1450459023617949747> 🧾 . . 🏹", color=0xffc0cb)
        emb.set_image(url="https://i.ibb.co/LkhmG8M/welcome-image.png")
        await ch.send(content=f"welcome {member.mention} !", embed=emb)

@bot.event
async def on_member_remove(member):
    ch = bot.get_channel(GOODBYE_CHANNEL_ID)
    if ch:
        emb = discord.Embed(description=f"(,,>_<,,)\n**{member.name} has left ;⊱**\n**BASSIE WORLD 🪷 ໒꒱ ; !!**\n((ಡ_ಡ)/ 🌸 * . . goodbye\n{member.mention}\n🔮 ᵲ ◞ we're sad to see you go !\n\n ◞ if you choose to return, you are always welcome. ‼️\n---------- ςορ ----------", color=0x2f3136)
        emb.set_thumbnail(url=member.display_avatar.url)
        await ch.send(content=f"goodbye {member.mention} !", embed=emb)

# --- الهوست ---
@bot.event
async def on_message(msg):
    if msg.channel.id == HOST_CHANNEL_ID and not msg.author.bot:
        pls = list(set([m for m in msg.mentions if not m.bot and m.id != GAME_ROLE_ID]))
        for p in pls:
            uid = str(p.id)
            old_s = user_data.get(uid, 0)
            new_s = old_s + 1
            user_data[uid] = new_s
            if calculate_level(new_s) > calculate_level(old_s):
                lvl_emb = discord.Embed(title="LEVEL UP! 🌸", color=0xffc0cb)
                lvl_emb.set_image(url="https://i.ibb.co/aec358ce/flower-image.gif")
                await msg.channel.send(content=f"🎊 {p.mention} ارتفع مستواك!", embed=lvl_emb)
                nl = calculate_level(new_s)
                if nl in LEVEL_ROLES:
                    nr = msg.guild.get_role(LEVEL_ROLES[nl])
                    if nr:
                        for rid in LEVEL_ROLES.values():
                            rl = msg.guild.get_role(rid)
                            if rl in p.roles: await p.remove_roles(rl)
                        await p.add_roles(nr)
        save_data(user_data)
        if pls: await msg.add_reaction("⭐")
    await bot.process_commands(msg)

# --- الأوامر (تغيير الأسماء لمنع التكرار) ---
@bot.command(name="my_rank", aliases=['tr', 'TR', 'toonrank'])
async def my_rank(ctx, m: discord.Member = None):
    m = m or ctx.author
    s = user_data.get(str(m.id), 0)
    l = calculate_level(s)
    emb = discord.Embed(title="🎮 Toon Profile", color=0xffc0cb)
    emb.add_field(name="الاسم", value=m.mention, inline=False)
    emb.add_field(name="🔥 الهوستات", value=f"**{s}**", inline=True)
    emb.add_field(name="🏆 المستوى", value=f"**Lvl {l}**", inline=True)
    await ctx.send(embed=emb)

@bot.command(name="leaderboard", aliases=['tt', 'TT', 'toptoons'])
async def leaderboard(ctx):
    sd = sorted(user_data.items(), key=lambda x: x[1], reverse=True)[:10]
    txt = "".join([f"**#{i}** <@{u}> — `Lvl {calculate_level(s)}` ({s} هوست)\n" for i, (u, s) in enumerate(sd, 1)])
    await ctx.send(embed=discord.Embed(title="🏆 قائمة الأساطير", description=txt or "فارغة", color=0xffc0cb))

# --- التشغيل ---
bot.run(os.getenv('TOKEN'))
