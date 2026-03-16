import os
import json
import random
import discord
from discord.ext import commands

# إعدادات البوت والتوكن من الـ Secrets
TOKEN = os.environ.get('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

XP_FILE = 'xp_data.json'

# --- دالات النظام (قاعدة البيانات والحسابات) ---
def load_xp():
    if os.path.exists(XP_FILE):
        with open(XP_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_xp(data):
    with open(XP_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def xp_progress(total_xp):
    level = 0
    xp = total_xp
    def xp_for_next_level(l):
        return 5 * (l ** 2) + 50 * l + 100
    while xp >= xp_for_next_level(level):
        xp -= xp_for_next_level(level)
        level += 1
    needed = xp_for_next_level(level)
    return level, xp, needed

def level_color(level):
    if level < 5:    return 0xFFFFFF
    elif level < 10: return 0xD3D3D3
    elif level < 15: return 0xA9A9A9
    elif level < 25: return 0x696969
    else:            return 0x111111

def level_rank_title(level):
    if level < 5:    return '⬜ مبتدئ'
    elif level < 10: return '🔘 متقدم'
    elif level < 15: return '🩶 محترف'
    elif level < 25: return '🌑 خبير'
    else:            return '⬛ أسطوري'

# --- الأحداث (Events) ---
@bot.event
async def on_ready():
    print(f'✅ تم تشغيل البوت بنجاح باسم: {bot.user}')

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name='ᥫ᭡₊⊹الترحيب✦˚೯⁺')
    if channel:
        notice = f"Welcome {member.mention}! 🤍"
        msg = (
            f"𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐭𝐨 ୭ ˚. ᵎᵎ𝐁𝐀𝐒𝐒𝐈𝐄 𝐖𝐎𝐑𝐋𝐃 Ꮺ ָ࣪ ۰ ͙⊹\n"
            f"𓏵۪۪　﹒　welcome　{member.mention}　<:Hi:1458708778257092742> 𓏼\n\n"
            f"Enjoy your stay here!! ✨"
        )
        embed = discord.Embed(description=msg, color=0xf5c2d8)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1458508427054813245/1458521031357628632/Untitled24_20260102213614.png")
        embed.set_footer(text=f"You are our {member.guild.member_count} member!")
        await channel.send(content=notice, embed=embed)

@bot.event
async def on_member_remove(member):
    channel = discord.utils.get(member.guild.text_channels, name='ᥫ᭡₊⊹ˑالوداع✦˚೯⁺')
    if channel:
        msg = f"(ಡ‸ಡ)ﾉ goodbye {member.mention}\nwe're sad to see you go !"
        embed = discord.Embed(description=msg, color=0x9ba8c2)
        await channel.send(embed=embed)

@bot.event
async def on_message(message):
    if message.author.bot: return
    if message.content == '.': await message.channel.send('مياو')

    data = load_xp()
    u_id = str(message.author.id)
    if u_id not in data:
        data[u_id] = {'xp': 0, 'total_xp': 0}
    
    old_lvl, _, _ = xp_progress(data[u_id]['total_xp'])
    data[u_id]['total_xp'] += random.randint(15, 25)
    new_lvl, _, _ = xp_progress(data[u_id]['total_xp'])
    save_xp(data)

    if new_lvl > old_lvl:
        lvl_channel = discord.utils.get(message.guild.text_channels, name='·𓈒⟡⌇المستوى⋆₊˚⋆') or message.channel
        embed = discord.Embed(
            title='🎉 مبروك ترقيت بالمستوى!',
            description=f'مبروك {message.author.mention}! صرت لفل {new_lvl}.',
            color=level_color(new_lvl)
        )
        embed.set_footer(text=level_rank_title(new_lvl))
        await lvl_channel.send(content=f"{message.author.mention} لقد ترقيت!", embed=embed)
    
    await bot.process_commands(message)

# --- الأوامر (Commands) ---
@bot.command(name='rank', aliases=['رانك', 'r'])
async def rank(ctx, member: discord.Member = None):
    member = member or ctx.author
    data = load_xp()
    u_id = str(member.id)
    if u_id not in data: return await ctx.send("لا توجد بيانات لهذا العضو.")

    lvl, curr, need = xp_progress(data[u_id]['total_xp'])
    sorted_users = sorted(data.items(), key=lambda x: x[1]['total_xp'], reverse=True)
    pos = next((i + 1 for i, (uid, _) in enumerate(sorted_users) if uid == u_id), '?')

    embed = discord.Embed(description=f'## {member.display_name}\n{level_rank_title(lvl)}', color=level_color(lvl))
    embed.add_field(name='level', value=f'**{lvl}**', inline=True)
    embed.add_field(name='Rank', value=f'**#{pos}**', inline=True)
    embed.set_thumbnail(url=member.display_avatar.url)
    await ctx.send(embed=embed)

@bot.command(name="showtop", aliases=['top', 'توب'])
async def show_leaderboard_rank(ctx):
    try:
        data = load_xp()
        if not data: return await ctx.send("القائمة فارغة حالياً.")
        
        rankings = sorted(data.items(), key=lambda x: x[1]['total_xp'], reverse=True)[:10]
        embed = discord.Embed(title="🏆 قائمة توب 10 المتفاعلين", color=0xFFD700)
        
        for i, (u_id, u_data) in enumerate(rankings, 1):
            try:
                user = await bot.fetch_user(int(u_id))
                name = user.name
            except:
                name = "عضو غادر"
            
            lvl, _, _ = xp_progress(u_data['total_xp'])
            embed.add_field(name=f"#{i} | {name}", value=f"اللفل: `{lvl}` | XP: `{u_data['total_xp']}`", inline=False)
        
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"خطأ: {e}")

@bot.command(name='ticket_rules')
async def ticket_rules(ctx):
    msg = (
        "⏔⏔⏔⏔⏔⏔ ꒰ ᧔ෆ᧓ ꒱ ⏔⏔⏔⏔⏔⏔\n"
        "⭑ عند فتح تكت ومرور ساعة ولم يتم الرد منك سيتم إغلاقه\n"
        "⭑ الرجاء التحلي بالصبر وعدم السبام\n"
        "⭑ احترام المسؤولين بدون مزح !\n"
        "⭑ التيكت بدون سبب = تايم أوت 4 ساعات"
    )
    embed = discord.Embed(description=msg, color=0xf0c8e0)
    if os.path.exists('ticket.gif'):
        file = discord.File('ticket.gif', filename='ticket.gif')
        embed.set_image(url='attachment://ticket.gif')
        await ctx.send(file=file, embed=embed)
    else:
        await ctx.send(embed=embed)

bot.run(TOKEN)
