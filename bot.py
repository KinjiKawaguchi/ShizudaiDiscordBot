from pickletools import read_unicodestringnl
import discord
from discord.ext import commands
import asyncio
import os

client = discord.Client()
TOKEN = ""
channelid_list = [962207533760647168,962192453459394581,962192523521060904,962195999894413332,962196080668323890,962196045130002432,962196112435982358,962196159017918464]#入学年選択,学部選択,学科選択
reactionamount_list = [4,6,4,5,5,3,5,2]#リアクション必要数
reacitons_list = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣'] #リアクション配列
roles_list = [[962191686807728168,962191685113241630,962191680755355668,962191679945863208],[962187785563947008,962188193669734401,962188268584173648,962188276368830494,962188538051448852,962188543457910804],[962188902934908940,962189079863263232,962189080609837057,962189081599680555],[962189082295951471,962189474396266587,962189474715025499,962189475872636978,962189476451459082],[962190269640474675,962190270684876850,962190271297232926,962190271729242144,962190272861708338],[962189477260959805,962189477676220466,962190269292347483],[962190273604124763,962190273994190869,962190274841436281,962190951743356929,962190953408528404],[962190955665063977,962190954671009823]]
karirole_list = [962300634047057991,962300644348272670,962300675260293131,962300647179419668,962300676615061614,962300677978198156]
itjirole_list = [962312318761447485,962357921751117905]


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    file = open('roleselect.txt','r',encoding='UTF-8')
    messagelist = file.readlines()
    i=0
    for channelid in channelid_list:
        channel = client.get_channel(channelid)
        await channel.purge()
        send_msg = await channel.send(messagelist[i])
        for j in range(reactionamount_list[i]):
            await send_msg.add_reaction(reacitons_list[j])
        if i!=0:
            await send_msg.add_reaction('⛔')
        i+=1
        
@client.event
async def on_reaction_add(reaction,user):
    if user.bot:
        return
    x=-1
    y=-1
    #--------------------------------------------------------------------------
    for j in range(8):
        if reaction.message.channel.id == channelid_list[j]:
            x=j
    if x == -1:
        return
    
    if reaction.emoji == '⛔':
        for j in itjirole_list:
            role = discord.utils.find(lambda r: r.id == j,user.guild.roles)
            await user.remove_roles(role)
        for j in sum(roles_list,[]):
            role = discord.utils.find(lambda r: r.id == j,user.guild.roles)
            await user.remove_roles(role)
        for j in karirole_list:
            role = discord.utils.find(lambda r: r.id == j,user.guild.roles)
            await user.remove_roles(role)
        return
    for j in range(6):
        if reaction.emoji == reacitons_list[j]:
            y=j
    #--------------------------------------------------------------------------
    if x == 0:
        role = discord.utils.find(lambda r: r.id == 962312318761447485,user.guild.roles)
        await user.add_roles(role)
    elif x == 1:
        role = discord.utils.find(lambda r: r.id == karirole_list[y],user.guild.roles)
        await user.add_roles(role)
        role = discord.utils.find(lambda r: r.id == 962312318761447485,user.guild.roles)
        await user.remove_roles(role)
    else:
        for j in range(6):
            role = discord.utils.find(lambda r: r.id == karirole_list[j],user.guild.roles)
            await user.remove_roles(role)
        role = discord.utils.find(lambda r: r.id == 962357921751117905,user.guild.roles)
        await user.add_roles(role)
    role = discord.utils.find(lambda r: r.id == roles_list[x][y],user.guild.roles)
    await user.add_roles(role)

#メンバー数表示        
@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content.startswith('/rolereset'):
        print('aaaa')
        user = message.author
        for j in itjirole_list:
            role = discord.utils.find(lambda r: r.id == j,user.guild.roles)
            await user.remove_roles(role)
        for j in sum(roles_list,[]):
            role = discord.utils.find(lambda r: r.id == j,user.guild.roles)
            await user.remove_roles(role)
        for j in karirole_list:
            role = discord.utils.find(lambda r: r.id == j,user.guild.roles)
            await user.remove_roles(role)
        return
    member_count = message.guild.member_count 
    GuildName = f'静大交流鯖 {str(member_count)}Members'
    await message.guild.edit(name=GuildName)

client.run(TOKEN)
