import os
from dotenv import load_dotenv
import asyncio

import discord
from discord.ext import commands

from audio_processor import process_audio
import config as config

connections = {}
summarize_loop_tasks = {}

class Sam(commands.Cog):
    def __init__(self, bot_: commands.Bot):
        self.bot = bot_

    @commands.command()
    async def start(self, ctx: commands.Context):
        channel = ctx.message.author.voice.channel

        if ctx.voice_client is not None:
            await ctx.voice_client.move_to(channel)
            connections[ctx.guild.id] = ctx.voice_client
        else:
            vc = await channel.connect()
            connections.update({ctx.guild.id: vc})

        self.join_command_channel_id = ctx.message.channel.id
        async def on_recording_ended(sink, channel: discord.TextChannel, *args):
            # process_audio(sink, channel, *args)
            self.bot.loop.create_task(process_audio(sink, channel, self, *args))

        ctx.voice_client.start_recording(discord.sinks.WaveSink(), on_recording_ended, channel)

    @commands.command()
    async def stop(self, ctx: commands.Context):
        if ctx.guild.id not in connections:
            print("guild ", ctx.guild.id, " is not in connections")
            ctx.message.reply("recording was not active.")
        else:
            # if ctx.guild.id in summarize_loop_tasks: # todo
            #
            try:
                print(connections)
                vc = connections[ctx.guild.id]
                await ctx.message.reply("alright, just a second...")
                vc.stop_recording()

            except Exception as e:
                print("error: ", e)
                await ctx.message.reply("failed to stop recording. ")


    @commands.command()
    async def loop(self, ctx: commands.Context):
        print("user is requesting summarize")
        if (not ctx.message.author.voice or not ctx.message.author.voice.channel):
            return await ctx.message.reply("You must be in a vc first.")

        channel = ctx.message.author.voice.channel

        if ctx.voice_client is not None:
            await ctx.voice_client.move_to(channel)
            connections[ctx.guild.id] = ctx.voice_client
        else:
            vc = await channel.connect()
            connections.update({ctx.guild.id: vc})

        self.join_command_channel_id = ctx.message.channel.id
        if ctx.guild.id not in summarize_loop_tasks:
            print("creating summarize loop")
            task = self.bot.loop.create_task(self.summarize_loop(ctx))
            summarize_loop_tasks[ctx.guild.id] = task


    async def summarize_loop(self, ctx: commands.Context):
        channel = ctx.channel
        await asyncio.sleep(config.sleepTime)

        try:
            while True:
                if ctx.guild.id not in connections:
                    print("guild ", ctx.guild.id, " is not in connections, break-ing.")
                    break

                vc = connections[ctx.guild.id]
                
                recording_done = asyncio.Event()

                async def on_recording_ended(sink, channel: discord.TextChannel, *args):
                    # asyncio.run_coroutine_threadsafe(process_audio(sink, channel, self, *args), self.bot.loop)
                    # self.bot.loop.create_task(process_audio(sink, channel, self, *args))
                    asyncio.create_task(process_audio(sink, channel, self, *args))
                    recording_done.set()  # allow loop to continue recording right away


                vc.start_recording(discord.sinks.WaveSink(), on_recording_ended, channel)
                await asyncio.sleep(config.contextTime)
                vc.stop_recording()
                await recording_done.wait()

        except Exception as e:
            print("error in summarizing loop: ", e)
            if ctx.guild.id in connections:
                await connections[ctx.guild.id].disconnect()
                del connections[ctx.guild.id]
            summarize_loop_tasks.pop(ctx.guild.id, None)


    @commands.command()
    async def leave(self, ctx: commands.Context):

        if ctx.guild.id in connections:
            vc = connections[ctx.guild.id]
            vc.stop_recording()
            del connections[ctx.guild.id]

        await ctx.voice_client.disconnect(force=True)

    @loop.before_invoke
    @start.before_invoke
    async def ensure_voice(self, ctx: commands.Context):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()


bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("sam "),
    description="test description",
    # intents=intents,
    intents=discord.Intents.default().all(),
)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")


load_dotenv()
bot.add_cog(Sam(bot))
bot.run(os.getenv("TOKEN"))
