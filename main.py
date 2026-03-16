import discord
from discord.ext import commands
import json
import os

# --- 1. الإعدادات الأساسية ---
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents, case_insensitive=True)

# --- 2. ملف البيانات ---
DATA_FILE = "toon_stats.json"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except: return {}
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

user_data = load_data()

# --- 3. الآيديات والقوانين ---
HOST_CHANNEL_ID = 1450459023617949747
GAME_ROLE_ID = 1450818743251894472
WELCOME_CHANNEL_ID = 1450798372100243517
GOODBYE_CHANNEL_ID = 1450799020556554240

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

def calculate_level(score):
    if score <= 12: return score // 2
    elif score <= 24: return 6 + (score - 12) // 3
    elif score <= 44: return 10 + (score - 24) // 4
    else: return 15 + (score - 44) // 5

# --- 4. أحداث الترحيب والتوديع (نفس ميمو) ---
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

# --- 5. نظام الهوست والرتب ---
@bot.event
async def on_message(message):
    if message.channel.id == HOST_CHANNEL_ID and not message.author.bot:
        players = list(set([m for m in message.mentions if not m.bot and m.id != GAME_ROLE_ID]))
        for player in players:
            uid = str(player.id)
            old_score = user_data.get(uid, 0)
            new_score = old_score + 1
            user_data[uid] = new_score
            
            old_lvl = calculate_level(old_score)
            new_lvl = calculate_level(new_score)
            
            if new_lvl > old_lvl:
                embed = discord.Embed(title="LEVEL UP! 🌸", color=0xffc0cb)
                embed.set_image(url="https://i.ibb.co/aec358ce/flower-image.gif")
                await message.channel.send(content=f"🎊 {player.mention} ارتفع مستواك لـ {new_lvl}!", embed=embed)
                
                if new_lvl in LEVEL_ROLES:
                    new_role = message.guild.get_role(LEVEL_ROLES[new_lvl])
                    if new_role:
                        for r_id in LEVEL_ROLES.values():
                            role_to_rem = message.guild.get_role(r_id)
                            if role_to_rem in player.roles: await player.remove_roles(role_to_rem)
                        await player.add_roles(new_role)
        save_data(user_data)
        if players: await message.add_reaction("⭐")
    await bot.process_commands(message)

# --- 6. الأوامر ---
@bot.command(aliases=['tr', 'Tr'])
async def toonrank(ctx, member: discord.Member = None):
    member = member or ctx.author
    score = user_data.get(str(member.id), 0)
    lvl = calculate_level(score)
    embed = discord.Embed(title="🎮 Toon Profile", color=0xffc0cb)
    embed.add_field(name="الاسم", value=member.mention, inline=False)
    embed.add_field(name="🔥 الهوستات", value=f"**{score}**", inline=True)
    embed.add_field(name="🏆 المستوى", value=f"**Lvl {lvl}**", inline=True)
    await ctx.send(embed=embed)

@bot.command(aliases=['tt', 'TT'])
async def toptoons(ctx):
    sorted_data = sorted(user_data.items(), key=lambda x: x[1], reverse=True)[:10]
    desc = "".join([f"**#{i}** <@{u}> — `Lvl {calculate_level(s)}` ({s} هوست)\n" for i, (u, s) in enumerate(sorted_data, 1)])
    embed = discord.Embed(title="🏆 قائمة أساطير الهوست", description=desc or "لا يوجد بيانات", color=0xffc0cb)
    await ctx.send(embed=embed)

# --- 7. التشغيل الآمن ---
token = os.getenv('TOKEN')
if token:
    bot.run(token)
else:
    print("خطأ: TOKEN غير موجود في الـ Variables!")
