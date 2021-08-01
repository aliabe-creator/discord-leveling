import os
import discord
from discord.ext import commands
import json
from dotenv import load_dotenv
import datetime

load_dotenv()
token = os.environ.get("token")

activity = discord.Activity(type=discord.ActivityType.watching, name="the Inferno Squadron Server")
client = commands.Bot(command_prefix='.',activity=activity)

bad_words = ['anal','anus','arse','ass','ballsack','balls','bastard','bitch','biatch','bloody','blowjob','blow job','bollock','bollok','boner','boob','bugger','bum','butt','buttplug','clitoris','cock','coon','crap','cunt','damn','dick','dildo','dyke','fag','feck','fellate','fellatio','felching','fuck','f u c k','fudgepacker','fudge packer','flange','Goddamn','God damn','homo','jizz','knobend','knob end','labia','muff','nigger','nigga','penis','piss','poop','porn','p*rn', 'p0rn','prick','pube','pussy','queer','scrotum','sex','shit','s hit','sh1t','slut','smegma','spunk','tit','turd','twat','vagina','wank','whore']

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    channel = client.get_channel(843208748096159744)
    await channel.send('Ready to award some epic roles!')

@client.event
async def on_member_join(member):
    with open('users.json', 'r') as f:
        users = json.load(f)

    await update_data(users, member)

    with open('users.json', 'w') as f:
        json.dump(users, f)

@client.event
async def on_message(message):
    split = message.content.split()
    
    if message.author.bot == False:
        for w in bad_words:
            if (w in split):
                log = client.get_channel(827689365429026816)
                await log.send('Potentially offensive word caught. Blacklisted word: ' + w + '. Message from ' + message.author.mention + ': '+ message.content)
        
        with open('users.json', 'r') as f:
            users = json.load(f)

        await update_data(users, message.author)
        await add_experience(users, message.author, 5)
        await level_up(users, message.author, message)

        with open('users.json', 'w') as f:
            json.dump(users, f)

    await client.process_commands(message)


async def update_data(users, user):
    if not f'{user.id}' in users:
        users[f'{user.id}'] = {}
        users[f'{user.id}']['experience'] = 0
        users[f'{user.id}']['level'] = 1


async def add_experience(users, user, exp):
    users[f'{user.id}']['experience'] += exp


async def level_up(users, user, message):
    experience = users[f'{user.id}']['experience']
    lvl_start = users[f'{user.id}']['level']
    lvl_end = int(experience ** (1 / 4))
    if lvl_start < lvl_end:
        channel = client.get_channel(827687525920669717)
        await channel.send(f'{user.mention} has leveled up to level {lvl_end}.')
        users[f'{user.id}']['level'] = lvl_end

        roles = str(message.author.roles) #get roles
        now = datetime.datetime.now()
        joined_date = message.author.joined_at
        
        days_in_server = (now - joined_date).days #get days in server
        
        if '827702967057645568' in roles or '845099404821528586' in roles: #checks if they are at least Class B
            if (users[f'{message.author.id}']['level'] >= 4 and days_in_server > 7):
                var = discord.utils.get(message.guild.roles, name = "🗡️ Warrior 🗡️")
                await user.add_roles(var)
            if (users[f'{message.author.id}']['level'] >= 6 and days_in_server > 14):
                var = discord.utils.get(message.guild.roles, name = "⚔️ Knight ⚔️")
                await user.add_roles(var)
            if (users[f'{message.author.id}']['level'] >= 8 and days_in_server > 30):
                var = discord.utils.get(message.guild.roles, name = "🛡️ Brevet 🛡️")
                await user.add_roles(var)
            if (users[f'{message.author.id}']['level'] >= 10 and days_in_server > 60):
                var = discord.utils.get(message.guild.roles, name = "💥 Lord 💥")
                await user.add_roles(var)
            if (users[f'{message.author.id}']['level'] >= 15 and days_in_server > 120):
                var = discord.utils.get(message.guild.roles, name = "🥋 Master 🥋")
                await user.add_roles(var)

@client.command(help='Checks your current level.')
async def level(ctx, member: discord.Member = None):
    if not member:
        uid = ctx.message.author.id
        with open('users.json', 'r') as f:
            users = json.load(f)
        lvl = users[str(uid)]['level']
        await ctx.send(f'You are at level {lvl}!')
    else:
        uid = member.id
        with open('users.json', 'r') as f:
            users = json.load(f)
        lvl = users[str(uid)]['level']
        await ctx.send(f'{member} is at level {lvl}!')

client.run(token)