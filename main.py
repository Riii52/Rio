import discord, json, os, random
from discord.ext import commands

TOKEN = os.environ.get('DISCORD_TOKEN')
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents, case_insensitive=True)

DATA_FILE = 'xp_data.json'
GIF_URL = "https://i.ibb.co/aec358ce/flower-image.gif"
LINE_URL = "https://cdn.discordapp.com/attachments/1458508427054813245/1459190184200503387/image.png"

# الرتب التلقائية للـ Runs
ROLES = {1: 1483227597801521316, 4: 1483227645016674384, 6: 1483227734728773784, 8: 1483227747563081841, 9: 1483227757981859950, 12: 1483227765669888092, 14: 1483227776638255307, 16: 1483227784737460225, 20: 1483227826718249031}

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f: return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f: json.dump(data, f, indent=2)

def get_toon_lvl(s):
    if s <= 12: return s // 2
    elif s <= 24: return 6 + (s - 12) // 3
    elif s <= 44: return 10 + (s - 24) // 4
    else: return 15 + (s - 44) // 5

def xp_lvl_info(txp):
    lvl = 0
    xp = txp
    def next_xp(l): return 5*(l**2) + 50*l + 100
    while xp >= next_xp(lvl):
        xp -= next_xp(lvl)
        lvl += 1
    return lvl, xp, next_xp(lvl)

@bot.event
async def on_ready(): print(f'Logged in as {bot.user}')

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name='ᥫ᭡₊⊹الترحيب✦˚೯⁺')
    if channel:
        notice = f"Welcome {member.mention}! 🤍"
        msg = f"𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐭𝐨 ୭ ˚. ᵎᵎ𝐁𝐀𝐒𝐒𝐈𝐄 𝐖𝐎𝐑𝐋𝐃\nEnjoy your stay!! ✨"
        embed = discord.Embed(description=msg, color=0xf5c2d8)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1456666896563965993/1487072872236187779/Untitled24_20260102213614.png?ex=69c7d009&is=69c67e89&hm=99541b14006c613c67316b78694dd94ca99dca6484fb9161db59a90db3023e0d&")
        await channel.send(content=notice, embed=embed)


@bot.event
async def on_member_remove(m):
    ch = discord.utils.get(m.guild.text_channels, name='ᥫ᭡₊⊹الوداع✦˚೯⁺')
    if ch:
        # وردي غامق للوداع أيضاً
        emb = discord.Embed(description=f"(,,>_<,,)\n**{m.name} has left ;⊱**\n**BASSIE WORLD 🪷 ໒꒱ ; !!**\n((ಡ_ಡ)/ 🌸 * . . goodbye\n{m.mention}\n🔮 ᵲ ◞ we're sad to see you go !", 
                            color=0xE5A9B8)
        emb.set_thumbnail(url=m.display_avatar.url)
        await ch.send(embed=emb)

@bot.event
async def on_message(msg):
    if msg.author.bot: return
    if msg.content == '.': await msg.channel.send('مياو')
    
    data = load_data()
    uid = str(msg.author.id)
    if uid not in data: data[uid] = {'xp': 0, 'runs': 0}
    
    old_l, _, _ = xp_lvl_info(data[uid].get('xp', 0))
    data[uid]['xp'] = data[uid].get('xp', 0) + random.randint(15, 25)
    new_l, _, _ = xp_lvl_info(data[uid]['xp'])
    
    if new_l > old_l:
        l_ch = discord.utils.get(msg.guild.text_channels, name='·𓈒⟡⌇المستوى⋆₊˚⋆') or msg.channel
        # اللون أبيض لرسالة اللفل
        e = discord.Embed(title="🎉 لفل جديد!", 
                          description=f"ماشاء الله {msg.author.mention} شاد حيلك اليوم! وصلت لفل ({new_l}) استمر نبي نشوفك دايم بالتوب ! ❤️", 
                          color=0xffffff)
        e.set_thumbnail(url=msg.author.display_avatar.url)
        await l_ch.send(content=f"ترقيت! {msg.author.mention}", embed=e)

    if msg.channel.id == 1450459023617949747 and msg.mentions:
        for p in [m for m in msg.mentions if not m.bot and m.id != 1450818743251894472]:
            pid = str(p.id)
            if pid not in data: data[pid] = {'xp': 0, 'runs': 0}
            ol_t = get_toon_lvl(data[pid].get('runs', 0))
            data[pid]['runs'] = data[pid].get('runs', 0) + 1
            if get_toon_lvl(data[pid]['runs']) > ol_t:
                if ol_t+1 in ROLES:
                    role = msg.guild.get_role(ROLES[ol_t+1])
                    if role: await p.add_roles(role)
        await msg.add_reaction("✅")

    save_data(data)
    await bot.process_commands(msg)

@bot.command(name='rank', aliases=['r'])
async def rank(ctx, m: discord.Member = None):
    m = m or ctx.author
    data = load_data()
    d = data.get(str(m.id), {'xp': 0})
    lvl, cur_xp, n_xp = xp_lvl_info(d['xp'])
    sorted_xp = sorted(data.items(), key=lambda x: x[1].get('xp', 0), reverse=True)
    rank_pos = next(i for i, (uid, _) in enumerate(sorted_xp, 1) if uid == str(m.id))
    # اللون أبيض للرانك
    e = discord.Embed(title=m.name, 
                      description=f"level\n{lvl}\ntotal XP\n{d['xp']}\n\nترتيبك بالسيرفر\n#{rank_pos}\n\nلفلك سيكون {lvl+1}\nيبي لك {n_xp-cur_xp} اكس بي عشان تصير اللفل {lvl+1}!\nشد حيلك🤍", 
                      color=0xffffff)
    e.set_thumbnail(url=m.display_avatar.url)
    e.set_footer(text=f"طلب بواسطة {ctx.author.display_name}")
    await ctx.send(embed=e)

@bot.command(name='Toonrank', aliases=['tr'])
async def toonrank(ctx, m: discord.Member = None):
    m = m or ctx.author
    r = load_data().get(str(m.id), {'runs': 0}).get('runs', 0)
    # اللون أبيض للـ Toonrank
    e = discord.Embed(title="Toon Profile", color=0xffffff)
    e.set_author(name=m.display_name, icon_url=m.display_avatar.url)
    e.add_field(name="Total Runs", value=f"{r}", inline=True)
    e.add_field(name="Level", value=f"Lvl {get_toon_lvl(r)}", inline=True)
    e.set_image(url=GIF_URL)
    await ctx.send(embed=e)

@bot.command(name='Toptoons', aliases=['tt'])
async def tt(ctx):
    sd = sorted(load_data().items(), key=lambda x: x[1].get('runs', 0), reverse=True)[:10]
    txt = "\n".join([f"#{i} | <@{u}> - {d.get('runs',0)} Runs" for i, (u, d) in enumerate(sd, 1)])
    # اللون أبيض للتوب
    await ctx.send(embed=discord.Embed(title="Top Toons", description=txt or "No data", color=0xffffff))

@bot.command(name='L')
async def line(ctx): await ctx.send(LINE_URL)

bot.run(TOKEN)
