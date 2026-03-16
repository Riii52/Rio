import os
import json
import random
import time
import discord
from discord.ext import commands

TOKEN = os.environ.get('DISCORD_TOKEN')

if not TOKEN:
    raise ValueError("DISCORD_TOKEN غير موجود. يرجى إضافته في Secrets.")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

_cooldowns = {}
XP_FILE = 'xp_data.json'
CONFIG_FILE = 'config.json'

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"levelup_message": "🎉 {mention} وصل للفل **{level}** — {rank_title}"}

def load_xp():
    if os.path.exists(XP_FILE):
        with open(XP_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_xp(data):
    with open(XP_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_level(xp):
    level = 0
    while xp >= xp_for_next_level(level):
        xp -= xp_for_next_level(level)
        level += 1
    return level

def xp_for_next_level(level):
    return 5 * (level ** 2) + 50 * level + 100

def get_user_data(data, user_id):
    if user_id not in data:
        data[user_id] = {'xp': 0, 'total_xp': 0}
    return data[user_id]

def xp_progress(total_xp):
    level = 0
    xp = total_xp
    while xp >= xp_for_next_level(level):
        xp -= xp_for_next_level(level)
        level += 1
    needed = xp_for_next_level(level)
    return level, xp, needed

@bot.event
async def on_ready():
    print(f'تم تشغيل البوت بنجاح باسم: {bot.user}')

@bot.event
async def on_member_join(member):
    welcome_channel = discord.utils.get(member.guild.text_channels, name='ᥫ᭡₊⊹الترحيب✦˚೯⁺')
    if not welcome_channel:
        return

    msg = (
        f"welcome {member.mention} !\n"
        f"𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐭𝐨 ୭ ˚. ᵎᵎ𝐁𝐀𝐒𝐒𝐈𝐄 𝐖𝐎𝐑𝐋𝐃 Ꮺ ָ࣪ ۰ ͙⊹\n"
        f"𓏵۪۪　﹒　welcome　{member.mention}　<:Hi:1458708778257092742> 𓏼\n\n"
        f"<:Green_butterfly:1457032840867745813>  ۪۫۫𓏫　⌣　<#1450537026045870287>　﹕\n\n"
        f"　<#1450803745675022429>　𓈒　 ͝ །"
    )

    embed = discord.Embed(description=msg, color=0xf5c2d8)
    embed.set_image(url="https://cdn.discordapp.com/attachments/1458508427054813245/1458521031357628632/Untitled24_20260102213614.png?ex=695ff10f&is=695e9f8f&hm=dacef3236cbb20937ca8495b68fc502fd7b0d897ab0056d3909bb30531e1a670&")
    embed.set_footer(text="Enjoy your stay here!!")

    await welcome_channel.send(embed=embed)

@bot.event
async def on_member_remove(member):
    goodbye_channel = discord.utils.get(member.guild.text_channels, name='ᥫ᭡₊⊹ˑالوداع✦˚೯⁺')
    if not goodbye_channel:
        return

    msg = (
        f"{member.name}#{member.discriminator} has left {member.guild.name} !*!*\n\n"
        f"(ಡ‸ಡ)ﾉ　<:Hszzaqw22:1456806028917084375> ⁑　﹒　goodbye {member.mention}\n"
        f"　　　　 <:Khbb:1456805753451974656> ꒷　◞　we're sad to see you go !\n\n"
        f"◞.   if you choose to return, you are always welcome. <:emoji_50:1451309888851542066>\n\n"
        f"┄┄　﹒　᧔𐓪᧓　﹒　┄┄"
    )

    embed = discord.Embed(description=msg, color=0x9ba8c2)
    if member.guild.icon:
        embed.set_thumbnail(url=member.guild.icon.url)

    await goodbye_channel.send(embed=embed)

@bot.command(name='testgoodbye')
async def test_goodbye(ctx):
    goodbye_channel = discord.utils.get(ctx.guild.text_channels, name='ᥫ᭡₊⊹ˑالوداع✦˚೯⁺')
    target = goodbye_channel if goodbye_channel else ctx.channel

    msg = (
        f"{ctx.author.name}#{ctx.author.discriminator} has left {ctx.guild.name} !*!*\n\n"
        f"(ಡ‸ಡ)ﾉ　<:Hszzaqw22:1456806028917084375> ⁑　﹒　goodbye {ctx.author.mention}\n"
        f"　　　　 <:Khbb:1456805753451974656> ꒷　◞　we're sad to see you go !\n\n"
        f"◞.   if you choose to return, you are always welcome. <:emoji_50:1451309888851542066>\n\n"
        f"┄┄　﹒　᧔𐓪᧓　﹒　┄┄"
    )

    embed = discord.Embed(description=msg, color=0x9ba8c2)
    if ctx.guild.icon:
        embed.set_thumbnail(url=ctx.guild.icon.url)

    await target.send(embed=embed)

@bot.command(name='testwelcome')
async def test_welcome(ctx):
    welcome_channel = discord.utils.get(ctx.guild.text_channels, name='ᥫ᭡₊⊹الترحيب✦˚೯⁺')
    target = welcome_channel if welcome_channel else ctx.channel

    msg = (
        f"welcome {ctx.author.mention} !\n"
        f"𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐭𝐨 ୭ ˚. ᵎᵎ𝐁𝐀𝐒𝐒𝐈𝐄 𝐖𝐎𝐑𝐋𝐃 Ꮺ ָ࣪ ۰ ͙⊹\n"
        f"𓏵۪۪　﹒　welcome　{ctx.author.mention}　<:Hi:1458708778257092742> 𓏼\n\n"
        f"<:Green_butterfly:1457032840867745813>  ۪۫۫𓏫　⌣　<#1450537026045870287>　﹕\n\n"
        f"　<#1450803745675022429>　𓈒　 ͝ །"
    )

    embed = discord.Embed(description=msg, color=0xf5c2d8)
    embed.set_image(url="https://cdn.discordapp.com/attachments/1458508427054813245/1458521031357628632/Untitled24_20260102213614.png?ex=695ff10f&is=695e9f8f&hm=dacef3236cbb20937ca8495b68fc502fd7b0d897ab0056d3909bb30531e1a670&")
    embed.set_footer(text="Enjoy your stay here!!")

    await target.send(embed=embed)

@bot.event
async def on_message(message):
    if message.author == bot.user or message.author.bot:
        return

    if message.content == '.':
        await message.channel.send('مياو')

    # نظام XP
    data = load_xp()
    user_id = str(message.author.id)
    user = get_user_data(data, user_id)

    old_level, _, _ = xp_progress(user['total_xp'])

    earned_xp = random.randint(15, 25)
    user['total_xp'] += earned_xp
    user['xp'] = user['total_xp']

    new_level, current_xp, needed_xp = xp_progress(user['total_xp'])

    save_xp(data)

    if new_level > old_level:
        level_channel = discord.utils.get(message.guild.text_channels, name='·𓈒⟡⌇المستوى⋆₊˚⋆')
        target = level_channel if level_channel else message.channel

        embed = discord.Embed(
            title='مبروك ترقيت بالمستوى!',
            description=f'مبروك {message.author.mention}! صرت لفل {new_level}.',
            color=level_color(new_level)
        )
        embed.set_thumbnail(url=message.author.display_avatar.url)
        embed.set_footer(text=level_rank_title(new_level))

        notice = f"{message.author.mention} لقد ترقيت بالمستوى !"

        if os.path.exists('levelup.gif'):
            file = discord.File('levelup.gif', filename='levelup.gif')
            embed.set_image(url='attachment://levelup.gif')
            await target.send(content=notice, file=file, embed=embed)
        else:
            await target.send(content=notice, embed=embed)

    await bot.process_commands(message)

def level_color(level):
    if level < 5:    return 0xFFFFFF   # أبيض
    elif level < 10: return 0xD3D3D3   # رمادي فاتح
    elif level < 15: return 0xA9A9A9   # رمادي
    elif level < 20: return 0x808080   # رمادي متوسط
    elif level < 25: return 0x696969   # رصاصي
    elif level < 35: return 0x404040   # داكن
    else:            return 0x111111   # أسود

def level_rank_title(level):
    if level < 5:    return '⬜ مبتدئ'
    elif level < 10: return '🔘 متقدم'
    elif level < 15: return '🩶 محترف'
    elif level < 20: return '⚙️ رصاصي'
    elif level < 25: return '🌑 خبير'
    elif level < 35: return '🖤 متمرس'
    else:            return '⬛ أسطوري'

@bot.command(name='test')
async def test_levelup(ctx, level: int = 1):
    embed = discord.Embed(
        title='مبروك ترقيت بالمستوى!',
        description=f'مبروك {ctx.author.mention}! صرت لفل {level}.',
        color=level_color(level)
    )
    embed.set_thumbnail(url=ctx.author.display_avatar.url)
    embed.set_footer(text=level_rank_title(level))

    notice = f"{ctx.author.mention} لقد ترقيت بالمستوى !"

    if os.path.exists('levelup.gif'):
        file = discord.File('levelup.gif', filename='levelup.gif')
        embed.set_image(url='attachment://levelup.gif')
        await ctx.send(content=notice, file=file, embed=embed)
    else:
        await ctx.send(content=notice, embed=embed)

@bot.command(name='rank', aliases=['رانك', 'r', 'R'])
async def rank(ctx, member: discord.Member = None):
    member = member or ctx.author
    data = load_xp()
    user_id = str(member.id)
    user = get_user_data(data, user_id)

    level, current_xp, needed_xp = xp_progress(user['total_xp'])
    percent = current_xp / needed_xp

    bar_length = 12
    filled = int(percent * bar_length)
    bar = '━' * filled + '○' + '╌' * (bar_length - filled)

    # ترتيب المستخدم في السيرفر
    sorted_users = sorted(data.items(), key=lambda x: x[1]['total_xp'], reverse=True)
    rank_pos = next((i + 1 for i, (uid, _) in enumerate(sorted_users) if uid == user_id), '?')

    embed = discord.Embed(
        description=f'## {member.display_name}\n{level_rank_title(level)}',
        color=level_color(level)
    )

    embed.add_field(name='level', value=f'**{level}**', inline=True)
    embed.add_field(name='total XP', value=f'**{user["total_xp"]}**', inline=True)
    embed.add_field(name='ترتيبك بالسيرفر', value=f'**#{rank_pos}**', inline=True)

    remaining = needed_xp - current_xp
    embed.add_field(
        name=f'لفلك سيكون {level + 1}',
        value=f'`{bar}`\nيبي لك **{remaining:,}** اكس بي عشان تصير اللفل {level + 1}! شد حيلك🤍',
        inline=False
    )

    embed.set_thumbnail(url=member.display_avatar.url)
    embed.set_footer(text=f'طلب بواسطة {ctx.author.display_name}', icon_url=ctx.author.display_avatar.url)

    await ctx.send(embed=embed)

@bot.command(name='top', aliases=['لوحة', 'leaderboard'])
async def leaderboard(ctx):
    data = load_xp()

    if not data:
        await ctx.send('ما في بيانات بعد!')
        return

    sorted_users = sorted(data.items(), key=lambda x: x[1]['total_xp'], reverse=True)[:10]

    embed = discord.Embed(title='🏆 لوحة المتصدرين', color=discord.Color.gold())

    medals = ['🥇', '🥈', '🥉']
    lines = []
    for i, (user_id, user_data) in enumerate(sorted_users):
        try:
            member = ctx.guild.get_member(int(user_id))
            name = member.display_name if member else f'مستخدم ({user_id})'
        except:
            name = f'مستخدم ({user_id})'

        level, _, _ = xp_progress(user_data['total_xp'])
        medal = medals[i] if i < 3 else f'`{i+1}.`'
        lines.append(f'{medal} **{name}** — لفل {level} | {user_data["total_xp"]} XP')

    embed.description = '\n'.join(lines)
    await ctx.send(embed=embed)

@bot.group(name='ticket', invoke_without_command=True)
async def ticket(ctx):
    pass

@ticket.command(name='rules')
async def send_ticket(ctx):
    ticket_channel = discord.utils.get(ctx.guild.text_channels, name='݁₊⊹﹒˖°ʚتيكت🎟️ɞ°﹒₊⊹˖')
    target = ticket_channel if ticket_channel else ctx.channel

    msg = (
        "⏔⏔⏔⏔⏔⏔ ꒰ ᧔ෆ᧓ ꒱ ⏔⏔⏔⏔⏔⏔\n"
        "⭑ عند فتح تكت ومرور ساعة ولم يتم الرد منك سيتم إغلاقه\n"
        "⭑ الرجاء التحلي بالصبر عند انتظار مسؤولين التيكت و دون سبام منشن\n"
        "⭑ احترام مسؤولين التيكت بدون مزح !\n"
        "⭑ إذا فتحت تيكت بدون سبب سيتم إعطاؤك تايم أوت 4 ساعات"
    )

    embed = discord.Embed(description=msg, color=0xf0c8e0)

    file = discord.File('ticket.gif', filename='ticket.gif')
    embed.set_image(url='attachment://ticket.gif')


    await target.send(file=file, embed=embed) 
@bot.command(name="showtop")
async def show_leaderboard_rank(ctx):
    try:
        rankings = sorted(levels.items(), key=lambda x: x[1]['xp'], reverse=True)
        embed = discord.Embed(title="🏆 قائمة توب 10", color=discord.Color.gold())
        count = 1
        for user_id, data in rankings[:10]:
            try:
                user = await bot.fetch_user(int(user_id))
                user_name = user.name
            except:
                user_name = "عضو غادر"
            embed.add_field(name=f"#{count} | {user_name}", value=f"اللفل: {data['level']}", inline=False)
            count += 1
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"خطأ: {e}")

bot.run(TOKEN)
