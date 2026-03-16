import discord
from discord.ext import commands
import json, os

# إعدادات البوت
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents, case_insensitive=True)

DATA_FILE = "toon_stats.json"

# وظيفة تتأكد إن الملف موجود وتفتحه، وإذا مو موجود تسوي واحد جديد
def load_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({}, f)
        return {}
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

user_data = load_data()

# الآيديات (ثابتة زي ما اتفقنا)
HOST_CH = 1450459023617949747
GAME_ROLE = 1450818743251894472
WELCOME_CH = 1450798372100243517
GOODBYE_CH = 1450799020556554240
ROLES = {1: 1483227597801521316, 4: 1483227645016674384, 6: 1483227734728773784, 8: 1483227747563081841, 9: 1483227757981859950, 12: 1483227765669888092, 14: 1483227776638255307, 16: 1483227784737460225, 20: 1483227826718249031}

def get_lvl(s):
    if s <= 12: return s // 2
    elif s <= 24: return 6 + (s - 12) // 3
    elif s <= 44: return 10 + (s - 24) // 4
    else: return 15 + (s - 44) // 5

@bot.event
async def on_ready():
    print(f"✅ {bot.user} is online and ready!")

@bot.event
async def on_member_join(m):
    c = bot.get_channel(WELCOME_CH)
    if c:
        e = discord.Embed(title="Welcome to ໑ °. !!BASSIE WORLD Ꮺ ˚₊", description=f"⊹ ˖ \n ⚔️ . . welcome {m.mention} ! \n 🌸 ||| \n\n 🦋 𓋼 ᵎ 𓂃 <#1450798372100243517> 🎟️ \n\n <#1450459023617949747> 🧾 . . 🏹", color=0xffc0cb)
        e.set_image(url="https://i.ibb.co/LkhmG8M/welcome-image.png")
        await c.send(content=f"welcome {m.mention} !", embed=e)

@bot.event
async def on_member_remove(m):
    c = bot.get_channel(GOODBYE_CH)
    if c:
        e = discord.Embed(description=f"(,,>_<,,)\n**{m.name} has left ;⊱**\n**BASSIE WORLD 🪷 ໒꒱ ; !!**\n((ಡ_ಡ)/ 🌸 * . . goodbye\n{m.mention}\n🔮 ᵲ ◞ we're sad to see you go !", color=0x2f3136)
        e.set_thumbnail(url=m.display_avatar.url)
        await c.send(content=f"goodbye {m.mention} !", embed=e)

@bot.event
async def on_message(msg):
    if msg.channel.id == HOST_CH and not msg.author.bot:
        pls = list(set([m for m in msg.mentions if not m.bot and m.id != GAME_ROLE]))
        if pls:
            for p in pls:
                uid = str(p.id)
                old_s = user_data.get(uid, 0)
                new_s = old_s + 1
                user_data[uid] = new_s
                if get_lvl(new_s) > get_lvl(old_s):
                    le = discord.Embed(title="LEVEL UP! 🌸", color=0xffc0cb)
                    le.set_image(url="https://i.ibb.co/aec358ce/flower-image.gif")
                    await msg.channel.send(content=f"🎊 {p.mention} ارتفع مستواك!", embed=le)
                    nl = get_lvl(new_s)
                    if nl in ROLES:
                        nr = msg.guild.get_role(ROLES[nl])
                        if nr:
                            for rid in ROLES.values():
                                rl = msg.guild.get_role(rid)
                                if rl and rl in p.roles: await p.remove_roles(rl)
                            await p.add_roles(nr)
            with open(DATA_FILE, "w") as f:
                json.dump(user_data, f, indent=4)
            await msg.add_reaction("⭐")
    await bot.process_commands(msg)

@bot.command(aliases=['tr', 'TR'])
async def toonrank(ctx, m: discord.Member = None):
    m = m or ctx.author
    s = user_data.get(str(m.id), 0)
    e = discord.Embed(title="🎮 Toon Profile", color=0xffc0cb)
    e.add_field(name="🔥 الهوستات", value=f"**{s}**", inline=True)
    e.add_field(name="🏆 المستوى", value=f"**Lvl {get_lvl(s)}**", inline=True)
    await ctx.send(embed=e)

@bot.command(aliases=['tt', 'TT'])
async def toptoons(ctx):
    sd = sorted(user_data.items(), key=lambda x: x[1], reverse=True)[:10]
    txt = "".join([f"**#{i}** <@{u}> — `Lvl {get_lvl(s)}` ({s})\n" for i, (u, s) in enumerate(sd, 1)])
    await ctx.send(embed=discord.Embed(title="🏆 Top Toons", description=txt or "None", color=0xffc0cb))

bot.run(os.getenv('TOKEN'))
