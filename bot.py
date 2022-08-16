from asyncio.windows_events import ERROR_CONNECTION_ABORTED
from pickletools import read_unicodestringnl
import discord
from discord.ext import commandsAPTX 4869
import asyncio
import os
import random

err_noperm= "あなたにはこのコマンドを実行する権限がありません"

client = discord.Client()
TOKEN = "OTYxNjEwMTE0NTU5NzgyOTQy.Yk7fNQ.YwkKTIuRqntXTaTkCo8dJzCjY90"
channelid_list = [962207533760647168,962192453459394581,962192523521060904,962195999894413332,962196080668323890,962196045130002432,962196112435982358,962196159017918464]#入学年選択,学部選択,学科選択
reactionamount_list = [4,6,4,5,5,3,5,2]#リアクション必要数
reactions_list = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣'] #リアクション配列
roles_list = [[962191686807728168,962191685113241630,962191680755355668,962191679945863208],[962187785563947008,962188193669734401,962188268584173648,962188276368830494,962188538051448852,962188543457910804],[962188902934908940,962189079863263232,962189080609837057,962189081599680555],[962189082295951471,962189474396266587,962189474715025499,962189475872636978,962189476451459082],[962190269640474675,962190270684876850,962190271297232926,962190271729242144,962190272861708338],[962189477260959805,962189477676220466,962190269292347483],[962190273604124763,962190273994190869,962190274841436281,962190951743356929,962190953408528404],[962190955665063977,962190954671009823]]
karirole_list = [962300634047057991,962300644348272670,962300675260293131,962300647179419668,962300676615061614,962300677978198156]
itjirole_list = [962312318761447485,962357921751117905]
tokushurole_list = [974553224575090739,975050952065302589]
homekotoba_list = ["偉い","すごい","勉強できて偉い","生きてるだけで偉いのに！！勉強まで！！","よしよしヾ(・ω・｀)","えらいえらい","勉強頑張って！！"]


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
            await send_msg.add_reaction(reactions_list[j])
        if i!=0:
            await send_msg.add_reaction('⛔')
        i+=1
    #------------------------------------------------------------------------
    channel = client.get_channel(975623166938476574)
    await channel.purge()
    send_msg = await channel.send("追加したいロールを選択してください。 :one: => TRPG :two: => ざつだんぶ")
    for i in range(2):
        await send_msg.add_reaction(reactions_list[i])
    #------------------------------------------------------------------------
        
@client.event
async def on_reaction_add(reaction,user):
    if user.bot:
        return
    x=-1
    y=-1
    #--------------------------------------------------------------------------
    if reaction.message.channel.id == 975623166938476574:
        for j in range(5):
            if reaction.emoji == reactions_list[j]:
                role = user.guild.get_role(tokushurole_list[j])
                await user.add_roles(role)
    #-------------------------------------------------------------------------
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
        if reaction.emoji == reactions_list[j]:
            y=j
    #--------------------------------------------------------------------------
    if x == 0:
        role = user.guild.get_role(962312318761447485)
        await user.add_roles(role)
    elif x == 1:
        role =user.guild.get_role(karirole_list[y])
        await user.add_roles(role)
        role = user.guild.get_role(962312318761447485)
        await user.remove_roles(role)
    else:
        for j in range(6):
            role = user.guild.get_role(karirole_list[j])
            await user.remove_roles(role)
        role = user.guild.get_role(962357921751117905)
        await user.add_roles(role)
    role = user.guild.get_role(roles_list[x][y])
    await user.add_roles(role)

@client.event
async def on_reaction_remove(reaction,user):
    if reaction.message.channel.id == 975623166938476574:
        for j in range(5):
            if reaction.emoji == reactions_list[j]:
                role = user.guild.get_role(tokushurole_list[j])
                await user.remove_roles(role)
    
#メンバー数表示        
@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content.startswith('/rolereset'):
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
    
    #if "勉強" in message.content or "課題" in message.content and "する" in message.content or "やる" in message.content or "します" in message.content:
    #    homekotoba = homekotoba_list[random.randint(0,len(homekotoba_list)-1)]
    #    msg = f'{message.author.mention}{homekotoba}'
    #    await message.channel.send(msg)

async def rolereset(user):
    await user.remove_roles(itjirole_list)
    await user.remove_roles(roles_list)
    await user.remove_roles(karirole_list)
    return

client.run(TOKEN)







"""    if message.content.startswith('/serverregister'):
        if message.author.administrator:
            data = ((message.guild.id,message.guild.name))
            cursor.execute(sql, data)
            conn.commit
        else:
            message.channel.send(err_noperm)

    if message.content.statswith('/serverremove'):
        if message.autor.administrator:
            cursor.execute('delete drom server wjere id=?',(message.guild.id,))
            conn.commit()
        else:
            message.channel.send(err_noperm)
"""
