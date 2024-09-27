import threading
import discord
import os
import requests
import json
import asyncio
import database
import func
import random
import logging
import googleapiclient
import youtube_live

from discord.ext.commands import Bot
from discord.ext import commands
from discord.errors import HTTPException, GatewayNotFound, ConnectionClosed
from keep_alive import keep_alive
from detect_game import get_last_window_active
from dotenv import load_dotenv
# from log import log_error

import tray

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True
intents.messages = True


# client = discord.Client(intents=intents)



load_dotenv()
TOKEN = os.getenv('TOKEN')
YOUTUBE_API = os.getenv('YOUTUBE_API')

class MyBotClient(discord.Client):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)


  # @client.event
  async def on_ready(self):
    print('{0.user} logged in'.format(self))
    detect_game_task = asyncio.create_task(detect_game_loop(self))
    # detect_live_active_task = asyncio.create_task(detect_live_active_loop())
    await asyncio.gather(detect_game_task)

  # @client.event
  async def on_message(self, message):

    if message.author == self.user:
      return

    msg = str(message.content)
    msgch = message.channel
    msgsv = message.guild

    if msg.startswith('>>mute'):
      temp = msg.split(' ')
      if len(temp) == 1:
        await msgch.send(f'sai cú pháp')
      elif len(temp) >= 2:
        member_mentions = message.mentions
        muterole = discord.utils.get(msgsv.roles, name = 'Muted')
        note = ''
        for m_mem in member_mentions:
          await m_mem.add_roles(muterole)
          note = note + f'{m_mem.mention} '
        note = note + f'đã ~~được~~ mute'
        m_channel = discord.utils.get(msgsv.channels, name = 'unban')
        await msgch.send(note + f' bởi {message.author.mention}' +\
                        f'\ntype `>>unmute` vào room {m_channel.mention} để được unmute')

    if msg.startswith('>>name'):
      if message.channel.name == 'change-nickname':
        member_mentions = message.mentions
        if len(member_mentions) > 0:
          await msgch.send('không được phép đổi tên của người khác')
        else:
          m_nick = message.author.nick
          m_newnick = msg.replace('>>name ', '')
          await message.author.edit(nick = m_newnick)
          m_announce =f'Đã đổi tên của {message.author.mention} từ `{m_nick}` thành `{m_newnick}`'
          await msgch.send(m_announce)
      else:
        await msgch.send(f'{message.author.mention}Không được đổi tên ở đây')

    if msg.startswith('>>unmute'):
      muterole = discord.utils.get(msgsv.roles, name = 'Muted')
      await message.author.remove_roles(muterole)
      note = f'{message.author.mention} đã được mute và có thể trò chuyện bình thường'
      await msgch.send(note)

    if msg.startswith('!rank'):
      if database._response_() is False:
        await msgch.send(f'{message.author.mention}' + ' rank '.join(database.rsp_f()) +\
                        '\n`éo lên đưuọc top 1 đâu khỏi kiểm`\n' + func.get_gif('smug anime')) 
        
    if msg.startswith('>>slogan'):
      await msgch.send('ta là trùm của cả sever này, muahahaha\n' + func.get_gif("smug anime"))

    if msg.startswith('>>check'):
      await msgch.send(f'check ok')

    if msg.startswith('>>thumbsup'):
      await msgch.send(func.get_gif('thumbs up anime'))

    if msg.startswith('>>wakeup'):
      await msgch.send(func.get_gif('wake up anime'))

    if msg.startswith('>>drama'):
      await msgch.send(func.get_gif('popcorn anime'))  
      
    if msg.startswith('>>gif'):
      msgcom = msg.replace('>>gif', '').strip()
      print(msgcom)
      if msgcom is not None:
        await msgch.send(func.get_gif(msgcom + ' anime'))

    if msg.startswith('>>random'):
      temp = msg.split(' ')
      if len(temp) > 1:
        try:
          begin = int(temp[1])
          end = int(temp[2])
          b = random.choice(range(begin, end))
          await msgch.send(f'số được chọn là: {b}')
        except:
          await msgch.send("lỗi")

    if msg.startswith('>>ban'):
      if message.author.guild_permissions.administrator:
        command = msg.split()
        if msg == '>>ban':
          await msgch.send('`>>ban <@mentions|list>`')
        elif ' list' in msg:
          ban_list = []
          try:
            async for member in msgsv.bans():
              user = member.user
              ban_list.append(f'{user.name} || {user.id} || {user.mention}')
            await msgch.send(f'Danh sách ban: {ban_list}')
          except Exception as e:
            await msgch.send(e)
        else: # tien hanh ban
          member_mentions = message.mentions
          list_cant_ban =['administrator', 'leader', 'master']
          for m_mem in member_mentions:
            memroles = [role.name.lower() for role in m_mem.roles if role.name.lower() in list_cant_ban]
            if len(memroles) > 0 or m_mem.bot == True or m_mem == message.author:  
              print(m_mem.roles)             
              await msgch.send(f'không thể ban {m_mem.mention}')
            else:
              await msgch.send(f'{m_mem.mention} đã bị ban')
              await msgsv.ban(m_mem)
              await msgch.send(f'{m_mem.mention} đã bị ban')
      else:
        await msgch.send(message.author.mention + ' không đủ quyền hạn')

    if msg.startswith('>>unban'):
      if message.author.guild_permissions.administrator:
        member_id = msg.split()[1]
        try:
          user = await self.fetch_user(int(member_id))
          await msgsv.unban(user)
          await msgch.send(f'{user.mention} đã được unban')
        except Exception as e:
          await msgch.send(e)
      else:
        await msgch.send(message.author.mention + ' không đủ quyền hạn')

    if msg.startswith('>>kick'):
      if message.author.guild_permissions.administrator:
        member_mentions = message.mentions
        for m_mem in member_mentions:
          if m_mem.author.guild_permissions.administrator or m_mem.bot == True or m_mem == message.author:
            await msgch.send(f'không thể kick {m_mem.mention}')
          else:
            await msgsv.kick(m_mem)
            await msgch.send(f'{m_mem.mention} đã bị kick')
      else:
        await msgch.send(message.author.mention + ' không đủ quyền hạn')

    if msg.startswith('>>help'):
      await msgch.send(f'```\n'
                      f'>>mute <@mentions> - mute người được mention\n'
                      f'>>unmute - unmute bản thân\n'
                      f'>>name <new_name> - đổi tên  tại kênh change-nickname\n'
                      f'>>ban <@mentions|list> - ban người được mention hoặc xem danh sách thành viên\n'
                      f'>>unban <@mentions> - unban người được mention\n'
                      f'>>kick <@mentions> - kick người được mention\n'
                      f'>>gif <keyword> - tìm kiếm gif\n'
                      f'>>random <begin> <end> - chọn số ngẫu nhiên trong khoảng\n'
                      f'>>live - xem kênh youtube\n'
                      f'```')

    # if msg.startswith('>>'):
    #   if database._response_() is False:
    #     await msgch.send(f'{message.author.mention}' + ' '.join(database.rsp_f()))
    #   else:
    #     await msgch.send(database.rsp_tr())
        
      
    if msg.startswith('>>live'):
      if msg.strip()  == '>>live':
        await msgch.send(youtube_live.get_channel())

      if len(msg.split()) > 1:
        pass

  # @client.event
  async def on_voice_state_update(self, member, before, after):
    if after.channel is not None and after.channel.name == 'Phòng Nghe Nhạc':
      guild = member.guild
      category = after.channel.category
      new_channel = await guild.create_voice_channel('Music for {0.display_name} '.format(member)\
                                                    , category=category)
      await member.move_to(new_channel)
      
    if before.channel is not None and before.channel.name.startswith('Music for'):
      if len(before.channel.members) == 0:
        await before.channel.delete()
      


async def start_bot():
  while True:
    try:
      if TOKEN is None:
        logging.error("TOKEN is missing. Please set the TOKEN environment variable.")
      else:
        client = MyBotClient(intents=intents)
        await client.start(TOKEN)
    except (HTTPException, GatewayNotFound, ConnectionClosed) as e:
      print(e)
      await asyncio.sleep(5)
    except Exception as e:
      print(e)
      await asyncio.sleep(5)

async def detect_game_loop(client):
  last_game_display = ''
  while True:
    # Cập nhật thông tin game
    last_game_display = get_last_window_active(last_game_display)
    
    if last_game_display is not None:
      await client.change_presence(
          status=discord.Status.online,
          activity=discord.Game(last_game_display)
      )
    else:
      await client.change_presence(status = discord.Status.online)
      
    # Dừng vòng lặp trong 10 giây trước khi kiểm tra lại
    await asyncio.sleep(10)  # Kiểm tra lại sau mỗi 10 giây

def run_bot():
  loop = asyncio.new_event_loop()
  asyncio.set_event_loop(loop)
  loop.run_until_complete(start_bot())

async def detect_live_active_loop(client):
  previous_live_videos = set()
  while True:
    list_live_video = youtube_live.get_list_live_video()
    live_video_id = youtube_live.get_live_video_id(list_live_video)
    current_live_videos = set([live_video_id]) if live_video_id else set()

    discord_channel = discord.utils.get(client.get_all_channels(), name='test-bot')
    if discord_channel is None:
      logging.error("Discord channel 'test-bot' not found.")
      await asyncio.sleep(5)  # Nghỉ 5 giây trước khi thử lại
      continue  # Quay lại đầu vòng lặp

     # Kiểm tra xem có video nào vừa bắt đầu live không
    new_live_videos = current_live_videos - previous_live_videos
    for video_id in new_live_videos:
      video_url = f"https://www.youtube.com/watch?v={video_id}"
      await discord_channel.send(f"Stream đã bắt đầu: {video_url}")

    # Kiểm tra xem có video nào vừa kết thúc không
    ended_live_videos = previous_live_videos - current_live_videos
    for video_id in ended_live_videos:
      video_url = f"https://www.youtube.com/watch?v={video_id}"
      await discord_channel.send(f"Stream đã kết thúc: {video_url}")

    previous_live_videos = current_live_videos
    # Dừng vòng lặp trong 10 giây trước khi kiểm tra lại
    await asyncio.sleep(10)



if __name__ == '__main__':
  keep_alive()
  run_bot()
      
  tray_thread = threading.Thread(target=tray.run_tray)
  tray_thread.daemon = True
  tray_thread.start()

  detect_game_thread = threading.Thread(target=detect_game_loop)
  detect_game_thread.daemon = True
  detect_game_thread.start()

  detect_live_active_thread = threading.Thread(target=detect_live_active_loop)
  detect_live_active_thread.daemon = True
  detect_live_active_thread.start()
