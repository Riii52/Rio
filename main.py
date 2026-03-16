import discord
from discord.ext import commands
import json
import os

# --- إعدادات البوت ---
intents = discord.Intents.default()
intents.message_content = True
intents.members = True # ضروري جداً للترحيب والرتب

bot = commands.Bot(command_prefix="!", intents=intents, case_insensitive=True)

# --- نظام حفظ البيانات ---
DATA_FILE = "toon_stats.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

user_data = load_data()

# --- الإعدادات (الآيديات) ---
HOST_CHANNEL_ID = 1450459023617949747
GAME_ROLE_ID = 1450818743251894472
WELCOME_CHANNEL_ID = 1450798372100243517
GOODBYE_CHANNEL_ID = 1450799020556554240

# جدول الرتب المتفق عليه
LEVEL_ROLES = {
    1: 1483227597801521316,
    4: 1483227645016674384,
    6: 1483227734728773784,
    8: 1483227747563081841,
    9: 1483227757981859950,
    12: 1483227765669888092,
    14: 1483227776638255307,
    16: 1483227784737460225,
    20: 1483227826718249031
}

# --- حسبة اللفل المتدرجة (Scaling) ---
def calculate_level(score):
    if score <= 12: # من لفل 0 لـ 6 (كل 2 هوست لفل)
        return score // 2
    elif score <= 24: # من لفل 7 لـ 10 (تحتاج 3 هوستات)
        return 6 + (score - 12) // 3
    elif score <= 44: # من لفل 11 لـ 15 (تحتاج 4 هوستات)
        return 10 + (score - 24) // 4
    else: # لفل 16 وفوق (تحتاج 5 هوستات)
        return 15 + (score - 44) // 5

# --- نظام الترحيب (نسخة ميمو) ---
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        embed = discord.Embed(
            title="Welcome to ໑ °. !!BASSIE WORLD Ꮺ ˚₊",
            description=f"⊹ ˖ \n ⚔️ . . welcome {member.mention} ! \n 🌸 ||| \n\n 🦋 𓋼 ᵎ 𓂃 <#1450798372100243517> 🎟️ \n\n <#1450459023617949747> 🧾 . . 🏹",
            color=0xffc0cb
        )
        embed.set_image(url="https://i.ibb.co/LkhmG8M/welcome-image.png")
        embed.set_footer(text="Enjoy your stay here!!")
        await channel.send(content=f"welcome {member.mention} !", embed=embed)

# --- نظام التوديع (نسخة ميمو) ---
@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(GOODBYE_CHANNEL_ID)
    if channel:
        embed = discord.Embed(
            description=f"(,,>_<,,)\n**{member.name} has left ;⊱**\n**BASSIE WORLD 🪷 ໒꒱ ; !!**\n((ಡ_ಡ)/ 🌸 * . . goodbye\n{member.mention}\n🔮 ᵲ ◞ we're sad to see you go !\n\n ◞ if you choose to return, you are always welcome. ‼️\n---------- ςορ ----------",
            color=0x2f3136
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        await channel.send(content=f"goodbye {member.mention} !", embed=embed)

# --- نظام الهوست رن (رصد اللفل والرتب) ---
@bot.event
async def on_message(message):
    if message.channel.id == HOST_CHANNEL_ID and not message.author.bot:
        # فلترة: استبعاد @game والبوتات والمكرر
        players = list(set([m for m in message.mentions if not m.bot and m.id != GAME_ROLE_ID]))
        
        for player in players:
            uid = str(player.id)
            old_score = user_data.get(uid, 0)
            new_score = old_score + 1
            user_data[uid] = new_score
            
            old_lvl = calculate_level(old_score)
            new_lvl = calculate_level(new_score)
            
            if new_lvl > old_lvl:
                # رسالة اللفل أب (بينك + صورة الزهور)
                embed = discord.Embed(title="LEVEL UP! 🌸", color=0xffc0cb)
                embed.set_image(url="https://i.ibb.co/aec358ce/flower-image.gif")
                await message.channel.send(content=f"🎊 {player.mention} ارتفع مستواك!", embed=embed)
                
                # تحديث الرتبة (حذف القديم وإضافة الجديد)
                if new_lvl in LEVEL_ROLES:
                    new_role = message.guild.get_role(LEVEL_ROLES[new_lvl])
                    if new_role:
                        for lvl, rid in LEVEL_ROLES.items():
                            role_to_remove = message.guild.get_role(rid)
                            if role_to_remove and role_to_remove in player.roles:
                                await player.remove_roles(role_to_remove)
                        await player.add_roles(new_role)

        save_data(user_data)
        if players: await message.add_reaction("⭐")

    await bot.process_commands(message)

# --- الأوامر (بالاختصارات) ---
@bot.command(aliases=['tr', 'TR', 'Toonrank'])
async def toonrank(ctx, member: discord.Member = None):
    member = member or ctx.author
    score = user_data.get(str(member.id), 0)
    level = calculate_level(score)
    
    embed = discord.Embed(title="🎮 Toon Profile", color=0xffc0cb)
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="الاسم", value=member.mention, inline=False)
    embed.add_field(name="🔥 الهوستات", value=f"**{score}**", inline=True)
    embed.add_field(name="🏆 المستوى", value=f"**Lvl {level}**", inline=True)
    await ctx.send(embed=embed)

@bot.command(aliases=['tt', 'TT', 'Toptoons'])
async def toptoons(ctx):
    sorted_data = sorted(user_data.items(), key=lambda x: x[1], reverse=True)[:10]
    desc = ""
    for i, (uid, sc) in enumerate(sorted_data, 1):
        lvl = calculate_level(sc)
        desc += f"**#{i}** <@{uid}> — `Lvl {lvl}` ({sc} هوست)\n"

    embed = discord.Embed(title="🏆 قائمة أساطير الهوست", description=desc or "القائمة فارغة", color=0xffc0cb)
    await ctx.send(embed=embed)

# --- التشغيل الآمن ---
token = os.getenv('TOKEN')
if token:
    bot.run(token)
else:
    print("خطأ: لم يتم العثور على TOKEN في إعدادات الموقع!")
