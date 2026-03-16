import discord, json, os, random
from discord.ext import commands

TOKEN = os.environ.get('DISCORD_TOKEN')
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents, case_insensitive=True)

DATA_FILE = 'xp_data.json'
GIF_URL = "https://i.ibb.co/aec358ce/flower-image.gif"
LINE_URL = "https://cdn.discordapp.com/attachments/1458508427054813245/1459190184200503387/image.png"

# الرتب التلقائية حسب اللفل
ROLES = {1: 1483227597801521316, 4: 1483227645016674384, 6: 1483227734728773784, 8: 1483227747563081841, 9: 1483227757981859950, 12: 1483227765669888092, 14: 1483227776638255307, 16: 1483227784737460225, 20: 1483227826718249031}

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f: return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f: json.dump(data, f, indent=2)

def get_lvl(s):
    if s <= 12: return s // 2
    elif s <= 24: return 6 + (s - 12) // 3
    elif s <= 44: return 10 + (s - 24) // 4
    else: return 15 + (s - 44) // 5

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_member_join(m):
    ch = discord.utils.get(m.guild.text_channels, name='ᥫ᭡₊⊹الترحيب✦˚೯⁺')
    if ch:
        emb = discord.Embed(title="Welcome to ໑ °. !!BASSIE WORLD Ꮺ ˚₊", 
                            description=f"⊹ ˖ \n ⚔️ . . welcome {m.mention} ! \n 🌸 ||| \n\n <#1450798372100243517> 🎟️ \n\n <#1450459023617949747> 🧾 . . 🏹", 
                            color=0xffc0cb)
        emb.set_image(url="https://i.ibb.co/LkhmG8M/welcome-image.png")
        await ch.send(content=f"welcome {m.mention} !", embed=emb)
        await ch.send(LINE_URL)

@bot.event
async def on_member_remove(m):
    ch = discord.utils.get(m.guild.text_channels, name='ᥫ᭡₊⊹الوداع✦˚೯⁺')
    if ch:
        emb = discord.Embed(description=f"(,,>_<,,)\n**{m.name} has left ;⊱**\n**BASSIE WORLD 🪷 ໒꒱ ; !!**\n((ಡ_ಡ)/ 🌸 * . . goodbye\n{m.mention}\n🔮 ᵲ ◞ we're sad to see you go !", color=0x2f3136)
        emb.set_thumbnail(url=m.display_avatar.url)
        await ch.send(embed=emb)

@bot.event
async def on_message(msg):
    if msg.author.bot: return
    if msg.content == '.': await msg.channel.send('مياو')
    
    data = load_data()
    uid = str(msg.author.id)
    if uid not in data: data[uid] = {'xp': 0, 'runs': 0}
    
    if msg.channel.id == 1450459023617949747 and msg.mentions:
        for p in [m for m in msg.mentions if not m.bot and m.id != 1450818743251894472]:
            pid = str(p.id)
            if pid not in data: data[pid] = {'xp': 0, 'runs': 0}
            old_l = get_lvl(data[pid].get('runs', 0))
            data[pid]['runs'] = data[pid].get('runs', 0) + 1
            new_l = get_lvl(data[pid]['runs'])
            
            if new_l > old_l:
                l_ch = discord.utils.get(msg.guild.text_channels, name='·𓈒⟡⌇المستوى⋆₊˚⋆') or msg.channel
                await l_ch.send(f"{p.mention} Level Up: {new_l}")
                if new_l in ROLES:
                    role = msg.guild.get_role(ROLES[new_l])
                    if role: await p.add_roles(role)
        await msg.add_reaction("✅")

    data[uid]['xp'] += random.randint(15, 25)
    save_data(data)
    await bot.process_commands(msg)

@bot.command(name='Toonrank', aliases=['tr', 'Tr!'])
async def toonrank(ctx, m: discord.Member = None):
    m = m or ctx.author
    d = load_data().get(str(m.id), {'runs': 0})
    r = d.get('runs', 0)
    e = discord.Embed(title="Toon Profile", color=0xffc0cb)
    e.set_author(name=m.display_name, icon_url=m.display_avatar.url)
    e.add_field(name="Total Runs", value=f"{r}", inline=True)
    e.add_field(name="Level", value=f"Lvl {get_lvl(r)}", inline=True)
    e.set_image(url=GIF_URL)
    await ctx.send(embed=e)

@bot.command(name='Toptoons', aliases=['tt', 'TT!'])
async def toptoons(ctx):
    data = load_data()
    sd = sorted(data.items(), key=lambda x: x[1].get('runs', 0), reverse=True)[:10]
    txt = ""
    for i, (uid, udata) in enumerate(sd, 1):
        txt += f"#{i} | <@{uid}> - {udata.get('runs', 0)} Runs\n"
    e = discord.Embed(title="Top Toons", description=txt or "No data", color=0xffc0cb)
    await ctx.send(embed=e)

@bot.command(name='L')
async def line(ctx): await ctx.send(LINE_URL)

bot.run(TOKEN)
