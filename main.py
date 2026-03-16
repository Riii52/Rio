import discord, json, os, random
from discord.ext import commands

# --- الإعدادات والتوكن ---
TOKEN = os.environ.get('DISCORD_TOKEN') 

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents, case_insensitive=True)

XP_FILE = 'xp_data.json'
LINE_URL = "https://cdn.discordapp.com/attachments/1458508427054813245/1459190184200503387/image.png"

# --- دالات النظام ---
def load_xp():
    if os.path.exists(XP_FILE):
        with open(XP_FILE, 'r', encoding='utf-8') as f: return json.load(f)
    return {}

def save_xp(data):
    with open(XP_FILE, 'w', encoding='utf-8') as f: json.dump(data, f, indent=2)

# حسبة لفل التفاعل (XP)
def xp_progress(total_xp):
    level = 0
    xp = total_xp
    def xp_for_next_level(l): return 5 * (l ** 2) + 50 * l + 100
    while xp >= xp_for_next_level(level):
        xp -= xp_for_next_level(level)
        level += 1
    return level, xp, xp_for_next_level(level)

# حسبة لفل الهوستات (Toon)
def get_host_lvl(s):
    if s <= 12: return s // 2
    elif s <= 24: return 6 + (s - 12) // 3
    elif s <= 44: return 10 + (s - 24) // 4
    else: return 15 + (s - 44) // 5

# --- الأحداث (Events) ---
@bot.event
async def on_ready():
    print(f'✅ {bot.user} شغال وبأفضل حال!')

# نظام الترحيب (نفس الصورة بالضبط)
@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name='ᥫ᭡₊⊹الترحيب✦˚೯⁺')
    if channel:
        embed = discord.Embed(
            title="Welcome to ໑ °. !!BASSIE WORLD Ꮺ ˚₊",
            description=f"⊹ ˖ \n ⚔️ . . welcome {member.mention} ! \n 🌸 ||| \n\n 🦋 𓋼 ᵎ 𓂃 <#1450798372100243517> 🎟️ \n\n <#1450459023617949747> 🧾 . . 🏹",
            color=0xffc0cb
        )
        embed.set_image(url="https://i.ibb.co/LkhmG8M/welcome-image.png") # حطي رابط صورة سيرفرك هنا
        embed.set_footer(text="Enjoy your stay here!!")
        await channel.send(content=f"welcome {member.mention} !", embed=embed)

# نظام التوديع (نفس الصورة بالضبط)
@bot.event
async def on_member_remove(member):
    channel = discord.utils.get(member.guild.text_channels, name='ᥫ᭡₊⊹الوداع✦˚೯⁺')
    if channel:
        embed = discord.Embed(
            description=f"(,,>_<,,)\n**{member.name} has left ;⊱**\n**BASSIE WORLD 🪷 ໒꒱ ; !!**\n((ಡ_ಡ)/ 🌸 * . . goodbye\n{member.mention}\n🔮 ᵲ ◞ we're sad to see you go !\n\n ◞ if you choose to return, you are always welcome. ‼️\n---------- ςορ ----------",
            color=0x2f3136
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        await channel.send(content=f"goodbye {member.mention} !", embed=embed)

@bot.event
async def on_message(message):
    if message.author.bot: return
    if message.content == '.': await message.channel.send('مياو')

    data = load_xp()
    u_id = str(message.author.id)
    if u_id not in data: data[u_id] = {'total_xp': 0, 'hosts': 0}
    if 'hosts' not in data[u_id]: data[u_id]['hosts'] = 0

    # رصد الهوستات (بناءً على الآيدي حقك)
    if message.channel.id == 1450459023617949747:
        players = list(set([m for m in message.mentions if not m.bot and m.id != 1450818743251894472]))
        for p in players:
            p_id = str(p.id)
            if p_id not in data: data[p_id] = {'total_xp': 0, 'hosts': 0}
            old_h_lvl = get_host_lvl(data[p_id].get('hosts', 0))
            data[p_id]['hosts'] = data[p_id].get('hosts', 0) + 1
            if get_host_lvl(data[p_id]['hosts']) > old_h_lvl:
                le = discord.Embed(title="LEVEL UP! 🌸", color=0xffc0cb)
                le.set_image(url="https://i.ibb.co/aec358ce/flower-image.gif")
                await message.channel.send(content=f"🎊 {p.mention} ارتفع لفل الهوست!", embed=le)
        await message.add_reaction("⭐")

    # نظام الـ XP التلقائي
    old_lvl, _, _ = xp_progress(data[u_id]['total_xp'])
    data[u_id]['total_xp'] += random.randint(15, 25)
    new_lvl, _, _ = xp_progress(data[u_id]['total_xp'])
    save_xp(data)

    if new_lvl > old_lvl:
        lvl_ch = discord.utils.get(message.guild.text_channels, name='·𓈒⟡⌇المستوى⋆₊˚⋆') or message.channel
        emb = discord.Embed(title="🎉 لفل جديد!", description=f"ماشاءالله {message.author.mention} وصلت لفل تفاعل (**{new_lvl}**)! ❤️", color=0xf5c2d8)
        await lvl_ch.send(embed=emb)
    
    await bot.process_commands(message)

# --- الأوامر ---
@bot.command(name='L', aliases=['l'])
async def send_line(ctx): await ctx.send(LINE_URL)

@bot.command(name='Toonrank', aliases=['tr', 'TR'])
async def toonrank(ctx, m: discord.Member = None):
    m = m or ctx.author
    d = load_xp().get(str(m.id), {'hosts': 0})
    h = d.get('hosts', 0)
    embed = discord.Embed(title="🎮 Toon Profile", color=0xffc0cb)
    embed.add_field(name="🔥 الهوستات", value=f"**{h}**", inline=True)
    embed.add_field(name="🏆 المستوى", value=f"**Lvl {get_host_lvl(h)}**", inline=True)
    embed.set_thumbnail(url=m.display_avatar.url)
    await ctx.send(embed=embed)

@bot.command(name='Toptoons', aliases=['tt', 'TT'])
async def toptoons(ctx):
    sd = sorted(load_xp().items(), key=lambda x: x[1].get('hosts', 0), reverse=True)[:10]
    txt = "".join([f"**#{i}** <@{u}> — `{d.get('hosts', 0)} هوست` (Lvl {get_host_lvl(d.get('hosts', 0))})\n" for i, (u, d) in enumerate(sd, 1)])
    await ctx.send(embed=discord.Embed(title="🏆 Top Toons", description=txt or "فارغة", color=0xffc0cb))

bot.run(TOKEN)
