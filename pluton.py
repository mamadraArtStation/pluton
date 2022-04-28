# coding=utf-8
import json
import discord
import random
import constant


discordNew = discord

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

with open(file='config.json', mode='r') as file:
    config = json.load(file)

botId = config['botId']


def checkAutorNotBot(message):
    if not message.author == client.user:
        return True
    else:
        return False


def get_info(message):
    channel = client.get_channel(config['start_channel'])
    members = channel.members
    users_array=[]
    for item in members:
        role_array = []
        for item_role in item.roles:
            role_id = item_role.id
            role_array.append(role_id)
        user = {'user_id': item.id, 'user_roles': role_array}
        users_array.append(user)
    users_json = {'users':users_array}
    with open(file='./files/users.json', mode='w', encoding="utf-8") as file:
        json.dump(users_json, file, ensure_ascii=False)
    pass




async def set_start_channel(message):
    global config
    message_content = message.content
    await message.delete()
    with open(file='config.json', mode='r') as file:
        config_for_bot = json.load(file)
    config_for_bot['start_channel'] = message_content.split(' ')[-1]
    with open(file='config.json', mode='w', encoding="utf-8") as file:
        json.dump(config_for_bot, file, ensure_ascii=False)
    with open(file='config.json', mode='r') as file:
        config = json.load(file)
    pass


@client.event
async def on_ready():
    constant.init()
    constant.client = client
    print('бот запущен')
    pass


@client.event
async def on_message(message):
    if checkAutorNotBot(message):
        if message.content.startswith("-get_info"):
            get_info(message)
        if message.content.startswith("-set_start_channel"):
            await set_start_channel(message)
    return


@client.event
async def on_member_join(member):
    roles_array = []
    with open(file='./files/users.json', mode='r') as file:
        users_json = json.load(file)
        for user in users_json['users']:
            if user['user_id'] == member.id:
                roles_array = user['user_roles']
    guild = member.guild
    for role_id in roles_array:
        role = guild.get_role(role_id)  # получаем объект роли*
        if not role.name == '@everyone':
            await member.add_roles(role)



@client.event
async def on_member_remove(member):
    roles_array = []
    with open(file='./files/users.json', mode='r') as file:
        users_json = json.load(file)
        for user in users_json['users']:
            if user['user_id'] == member.id:
                for role_item in member.roles:
                    role = role_item.id
                    roles_array.append(role)
                user['user_roles'] = roles_array
    with open(file='./files/users.json', mode='w', encoding="utf-8") as file:
        json.dump(users_json, file, ensure_ascii=False)
    print(member)




workSpace = 'production'
client.run(config['tokenDiscordProd'])


# python3 -m pip install -U discord.py
# pip install -U discord-py-slash-command
# pip install -U discord_components
# pip3 install discord
