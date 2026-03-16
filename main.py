import discord, json, os, random
from discord.ext import commands

# --- الإعدادات ---
TOKEN = os.environ.get('DISCORD_TOKEN') 
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all(), case_insensitive=True)

XP_FILE = 'xp_data.json'
LINE_URL = "https://cdn.discordapp.com/attachments/1458508427054813245/1459190184200503387/image.png"

def load_data():
    if os.path.exists(XP_FILE):
        with open(XP_FILE, 'r', encoding='utf-8') as f: return json.load(f)
    return {}

def save_data(data):
    with open(XP_FILE, 'w', encoding='utf-8') as f: json.dump(data, f, indent=2)

def get_host_lvl(s):
    if s <= 12: return s // 2
    elif s <= 24: return 6 + (s-12)//3
    elif s <= 44: return 10 + (s-24)//4
    return 15 + (s-44)//5

@bot.event
async def on_ready(): print(f'✅ {bot.user} Online')

@bot.event
async def on_member_join(m):
    ch = discord.utils.get(m.guild.text_channels, name='ᥫ᭡₊⊹الترحيب✦˚೯⁺')
    if ch:
        emb = discord.Embed(title="Welcome to ໑ °. !!BASSIE WORLD Ꮺ ˚₊", description=f"⊹ ˖ \n ⚔️ . . welcome {m.mention} ! \n\n <#1450798372100243517> 🎟️ \n <#1450459023617949747> 🧾", color=0xffc0cb)
        emb.set_image(url="https://i.ibb.co/LkhmG8M/welcome-image.png")
        await ch.send(content=f"welcome {m.mention} !", embed=emb)
        await ch.send(LINE_URL)

@bot.event
async def on_member_remove(m):
    ch = discord.utils.get(m.guild.text_channels, name='ᥫ᭡₊⊹الوداع✦˚೯⁺')
    if ch:
        emb = discord.Embed(description=f"**{m.name} has left ;⊱**\nwe're sad to see you go !", color=0x2f3136)
        await ch.send(embed=emb)

@bot.event
async def on_message(msg):
    if msg.author.bot: return
    data = load_data()
    uid = str(msg.author.id)
    if uid not in data: data[uid] = {'xp': 0, 'hosts': 0}
    
    # نظام الهوست
    if msg.channel.id == 1450459023617949747 and msg.mentions:
        for p in [m for m in msg.mentions if not m.bot and m.id != 1450818743251894472]:
            pid = str(p.id)
            if pid not in data: data[pid] = {'xp': 0, 'hosts': 0}
            old_l = get_host_lvl(data[pid]['hosts'])
            data[pid]['hosts'] += 1
            if get_host_lvl(data[pid]['hosts']) > old_l:
                await msg.channel.send(f"🎊 {p.mention} لفل هوست جديد!")
        await msg.add_reaction("⭐")

    # XP تفاعل
    data[uid]['xp'] += random.randint(15, 25)
    save_data(data)
    await bot.process_commands(msg)

@bot.command(name='Toonrank')
async def tr(ctx, m: discord.Member = None):
    m = m or ctx.author
    h = load_data().get(str(m.id), {}).get('hosts', 0)
    await ctx.send(f"🌸 {m.mention} | الهوستات: {h} | لفل: {get_host_lvl(h)}")

@bot.command(name='Toptoons')
async def tt(ctx):
    sd = sorted(load_data().items(), key=lambda x: x[1].get('hosts', 0), reverse=True)[:10]
    txt = "\n".join([f"#{i} <@{u}> — {d.get('hosts',0)} هوست" for i, (u, d) in enumerate(sd, 1)])
    await ctx.send(embed=discord.Embed(title="🏆 Top Toons", description=txt or "None", color=0xffc0cb))

@bot.command(name='L')
async def line(ctx): await ctx.send(LINE_URL)

bot.run(TOKEN)
