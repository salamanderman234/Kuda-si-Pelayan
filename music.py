# from distutils import command2
import discord
from discord.ext import commands
import re
from asyncio import sleep
# import requests
from requests_html import HTMLSession
import DiscordUtils

class music(commands.Cog):
    def __init__(self,client):
        self.client = client
        self.session = HTMLSession()
        self.music = DiscordUtils.Music()

    async def join(self,ctx):
        if not ctx.voice_client :
            if(ctx.author.voice):
                channel = ctx.author.voice.channel
                await channel.connect()
            else:
                await ctx.send('!! Join Voice Channel Dulu Bre !!')

    @commands.command()
    # command play
    async def play(self,ctx,*args):
        # bot akan mencoba join terlebih dahulu
        await self.join(ctx)
        try:
            keyword = '+'.join(args)
            if(keyword[0:32]=='https://www.youtube.com/watch?v=' and len(keyword)==43 and self.is_url(keyword)):
                url = keyword
            else:
                html_result = self.session.get('https://www.youtube.com/results?search_query='+keyword)
                url = 'https://www.youtube.com/watch?v='+ re.findall(r'watch\?v=(\S{11})', html_result.text)[0]
            
            player = self.music.get_player(guild_id=ctx.guild.id)
            if not player:
                player = self.music.create_player(ctx,ffmpeg_error_betterfix=True)

            song = await player.queue(url,search=True)
            print(f'== Menambahkan {song.name} ==\nUrl: {url}\n')
            if not ctx.voice_client.is_playing() and len(player.current_queue()) == 1:
                await player.play()
            embed = discord.Embed(title="**"+song.name+"**",url=song.url,description="From : "+song.channel,color=0x7E6AA6)
            embed.set_thumbnail(url=song.thumbnail)
            await ctx.send(f'!! **{song.name}** Ditambahkan ke Dalam Daftar Putar !!')
            await ctx.send(embed=embed)
        except:
            print('Exception Play')
    # akhir dari command play
    @commands.command()
    async def queue(self,ctx):
        player = self.music.get_player(guild_id=ctx.guild.id)
        try:
            queue_list = []
            for index,song in enumerate(player.current_queue()):
                if(index == 0):
                    queue_list.append('**'+str(index+1)+'. '+song.name+'**')
                else:
                    queue_list.append(str(index+1)+'. '+song.name)

            await ctx.send('\n'.join(queue_list))
        except:
            print("Exception Queue")
            await ctx.send('!! Daftar Putar Sedang Kosong !!')

    @commands.command()
    async def stop(self,ctx):
        if ctx.bot.voice_clients:
            await ctx.voice_client.disconnect()
            try:
                player = self.music.get_player(guild_id=ctx.guild.id)
                await player.stop()
            except:
                await ctx.send('!! Sedang Tidak Memutar Apapun !!')
        else:
            print('Exception Stop')
            await ctx.send('!! Sedang Tidak Memutar Apapun !!')


    @commands.command()
    async def skip(self,ctx):
        try:
            player = self.music.get_player(guild_id=ctx.guild.id)
            if len(player.current_queue()) >= 1:
                data = await player.skip(force=True)
                await ctx.send(f"!! **{data[0].name}**--Telah Dilewati !!")
            else:
                await ctx.send("!! Daftar Putar Sedang Kosong !!")
        except:
            print("Exception Skip")
            await ctx.send("!! Bot Sedang Tidak Memutar Apapun !!")
    
    @commands.command()
    async def resume(self,ctx):
        try:
            player = self.music.get_player(guild_id=ctx.guild.id)
            if not ctx.voice_client.is_playing():
                song = await player.resume()
                await ctx.send(f"!! **{song.name}**--Dilanjutkan !!")
            else:
                await ctx.send(f'!! Bot Sedang Memutar Lagu !!')
        except:
            print('Exception Resume')
            await ctx.send("!! Bot Sedang Tidak Memutar Apapun !!")

    @commands.command()
    async def pause(self,ctx):
        try:
            player = self.music.get_player(guild_id=ctx.guild.id)
            if ctx.voice_client.is_playing():
                song = await player.pause()
                await ctx.send(f"!! **{song.name}**--Dijeda !!")
            else:
                await ctx.send("!! Bot Sedang Tidak Memutar Apapun !!")
        except:
            print('Exception Pause')
            await ctx.send("!! Bot Sedang Tidak Memutar Apapun !!")

    @commands.command()
    async def info(self,ctx):
        player = self.music.get_player(guild_id=ctx.guild.id)
        try:
            song = player.now_playing()
            duration = "{:.1f}".format(song.duration/60)
            await ctx.send(f'Judul\t\t: {song.name}\nDari\t\t  : {song.channel}\nView\t\t: {song.views:,}\nDuration : {duration} Menit\nUrl\t\t\t: {song.url}')
        except:
            print('Exception Info')

    # auto leave jika semua peserta vc meninggalkan vc
    @commands.Cog.listener()
    async def on_voice_state_update(self,member, before, after):
        try:
            if self.client.get_guild(member.guild.id).voice_client is not None:
                if len(self.client.get_guild(member.guild.id).voice_client.channel.members) == 1:
                    await sleep(180)
                    if len(self.client.get_guild(member.guild.id).voice_client.channel.members) == 1:
                        await self.client.get_guild(member.guild.id).voice_client.disconnect()
                        player = self.music.get_player(guild_id=member.guild.id)
                        await player.stop()
                        print("Meninggalkan Voice Channel Karena Tidak ada Peserta")
                        print("Playlist Dibatalkan")
        except:
            print('Exception Auto Leave')

    def is_url(self,url):
        if re.match(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", url):
            return True
        else:
            return False
def setup(client):
    client.add_cog(music(client))
