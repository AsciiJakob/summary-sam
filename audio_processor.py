from io import BytesIO
import discord
import pydub
import tempfile
import time
import asyncio
import importlib
import os

import config as config
from transcribe import whisper_transcribe

try:
    language_model = importlib.import_module("lm_"+config.model_name)
    print("Loaded model "+config.model_name)
except Exception as e:
    print("failed to load language model called: "+config.model_name, "reason:", e)
    exit(1)


async def process_audio(sink, channel: discord.TextChannel, self, *args):
    print("processing audio")
    bot = self.bot

    transcription_start = time.time()
    ordered_segments = []

    files: list[discord.File] = []
    for user_id, audio in sink.audio_data.items():
        audio.file.seek(0)
        files.append(discord.File(audio.file, filename=f"{user_id}.wav"))
        with tempfile.NamedTemporaryFile(dir="tempAudios", suffix=f".{sink.encoding}", delete=False) as temp_file:
            audio.file.seek(0)  # reset file pointer to beginning
            temp_file.write(audio.file.read())
            temp_file_path = temp_file.name

        user_transcript = whisper_transcribe(temp_file_path, user_id)
        # os.remove(temp_file_path)

        for segment in user_transcript["segments"]:
                segment["user_id"] = user_id
                ordered_segments.append(segment)

    ordered_segments.sort(key=lambda s: s["start"])

    # compile transcript as a string
    transcriptStr = ""
    if config.writeOutStatuses:
        print("writing statuses thing")
        transcriptStr += "{Statuses}: "
        for member in bot.voice_clients[0].channel.members:
            for activity in member.activities:
                if (activity.type == discord.ActivityType.playing):
                    transcriptStr += f"{member.name}: {activity.name}, "
                    print("member: ", member.name, "activity: ", activity.name)
        if not transcriptStr.endswith("{Statuses}: "):
            transcriptStr += transcriptStr[:-2]
        transcriptStr += "\n"

    if config.makeTranscriptsAnonymousParagraph:
        for segment in ordered_segments:
            text = segment["text"].strip()
            if (not text[-1] in [".", "?", "!", ","]):
                text += "."
            transcriptStr += f"{text} "
    else:
        for segment in ordered_segments:
            user_id = segment["user_id"]
            text = segment["text"]
            transcriptStr += f"[{bot.get_user(user_id).display_name}]: {text.strip()}\n"
    
    transcriptStr = transcriptStr.rstrip("\n") # remove the trailing newline character
    print("compiled transcript. Transcription string:\n", transcriptStr)
    try:
        message = f"**__Transcript__** ({round(time.time()-transcription_start, 2)}s):\n{transcriptStr}"
        if len(message) > 2000:
            print("transcript too long for normal message.")
            bytes = BytesIO(message.encode("utf-8"))
            await bot.get_channel(self.join_command_channel_id).send(file=discord.File(fp=bytes, filename="message.txt"), silent=True)
        else:
            print("sending message")
            await bot.get_channel(self.join_command_channel_id).send(content=message, silent=True)
    except Exception as e:
        print("Failed to send message, error:", e)


    # run transcript through language model to summarize
    summarize_start = time.time()
    summary = await asyncio.to_thread(language_model.summarize_transcript, transcriptStr)

    print("Topic was summarized as:", summary)

    # await bot.voice_clients[0].channel.edit(status=summary)
    await bot.voice_clients[0].channel.set_status(summary)
    await bot.get_channel(self.join_command_channel_id).send(content=f"**__Summary__ ({config.model_name} {round(time.time()-summarize_start, 2)}s): {summary}**")
