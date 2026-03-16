import discord, json, os, random
from discord.ext import commands

# --- الإعدادات ---
TOKEN = os.environ.get('DISCORD_TOKEN') 
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents, case_insensitive=True)

XP_FILE = 'xp_data.json'
LINE_URL = "https://cdn.discordapp.com/attachments/1458508427054813245/1459190184200503387/image.png"

def load_xp():
    if os.path.exists(XP_FILE):
        with open(XP_FILE, 'r', encoding='utf-8') as f: return json.load(f)
    return {}

def save_xp(data):
    with open(XP_FILE, 'w', encoding='utf-8') as f: json.dump(data, f, indent=2)

def xp_progress(txp):
    lvl = 0
    xp = txp
    def next_xp(l): return 5*(l**2) + 50*l + 100
    while xp >= next_xp(lvl):
        xp -= next_xp(lvl)
        lvl += 1
    return lvl, xp, next_xp(lvl)

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
        emb = discord.Embed(title="Welcome to ໑ °. !!BASSIE WORLD Ꮺ ˚₊", description=f"⊹ ˖ \n ⚔️ . . welcome {m.mention} ! \n 🌸 ||| \n\n 🦋 𓋼 ᵎ 𓂃 <#1450798372100243517> 🎟️ \n\n <#1450459023617949747> 🧾 . . 🏹", color=0xffc0cb)
        emb.set_image(url="https://i.ibb.co/LkhmG8M/welcome-image.png")
        await ch.send(content=f"welcome {m.mention} !", embed=emb)
        await ch.send(LINE_URL) # اللاين يرسل تلقائياً بعد الترحيب

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
    
    data = load_xp()
    uid = str(msg.author.id)
    if uid not in data: data[uid] = {'total_xp': 0, 'hosts': 0}
    
    # نظام الهوست
    if msg.channel.id == 1450459023617949747:
        pls = [m for m in msg.mentions if not m.bot and m.id != 1450818743251894472]
        for p in pls:
            pid = str(p.id)
            if pid not in data: data[pid] = {'total_xp': 0, 'hosts': 0}
            ol = get_host_lvl(data[pid].get('hosts', 0))
            data[pid]['hosts'] = data[pid].get('hosts', 0) + 1
            if get_host_lvl(data[pid]['hosts']) > ol:
                await msg.channel.send(f"🎊 {p.mention} لفل هوست جديد: {ol+1}")
        await msg.add_reaction("⭐")

    # نظام الـ XP
    olvl, _, _ = xp_progress(data[uid]['total_xp'])
    data[uid]['total_xp'] += random.randint(15, 25)
    nlvl, _, _ = xp_progress(data[uid]['total_xp'])
    save_xp(data)
    
    if nlvl > olvl:
        lch = discord.utils.get(msg.guild.text_channels, name='·𓈒⟡⌇المستوى⋆₊˚⋆') or msg.channel
        await lch.send(f"🎉 {msg.author.mention} وصلت لفل {nlvl}!")
    await bot.process_commands(msg)

@bot.command(name='L', aliases=['l'])
async def line(ctx): await ctx.send(LINE_URL)

@bot.command(name='Toonrank', aliases=['tr'])
async def tr(ctx, m: discord.Member = None):
    m = m or ctx.author
    h = load_xp().get(str(m.id), {}).get('hosts', 0)
    e = discord.Embed(title="🎮 Toon Profile", color=0xffc0cb)
    e.add_field(name="🔥 الهوستات", value=h)
    e.add_field(name="🏆 لفل الهوست", value=get_host_lvl(h))
    await ctx.send(embed=e)

@bot.command(name='Toptoons', aliases=['tt'])
async def tt(ctx):
    sd = sorted(load_xp().items(), key=lambda x: x[1].get('hosts', 0), reverse=True)[:10]
    txt = "\n".join([f"#{i} <@{u}> — {d.get('hosts',0)} هوست" for i, (u, d) in enumerate(sd, 1)])
    await ctx.send(embed=discord.Embed(title="🏆 Top Toons", description=txt or "None", color=0xffc0cb))

bot.run(TOKEN)
