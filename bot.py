import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

SOURCE_ID = 1538831968794312775
TARGET_ID = 1538832177666727956

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.id == SOURCE_ID and message.attachments:
        target = bot.get_channel(TARGET_ID) or await bot.fetch_channel(TARGET_ID)
        files = [await att.to_file() for att in message.attachments]
        caption = f"Uploaded by {message.author.mention}\n{message.content}".strip()
        await target.send(content=caption, files=files)
        await message.delete()

    await bot.process_commands(message)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def cleanup(ctx, limit: int = 100):
    if ctx.channel.id != SOURCE_ID:
        await ctx.send("Run this inside the source channel/thread")
        return

    target = bot.get_channel(TARGET_ID) or await bot.fetch_channel(TARGET_ID)
    count = 0

    async for msg in ctx.channel.history(limit=limit):
        if msg.attachments and not msg.author.bot:
            files = [await att.to_file() for att in msg.attachments]
            caption = f"Archived from {msg.author.mention}\n{msg.content}".strip()
            await target.send(content=caption, files=files)
            await msg.delete()
            count += 1

    await ctx.send(f"Cleaned up {count} media messages", delete_after=5)

bot.run("MTUzOTYwMDExMzg4MDc5NzE4NA.GvpdW2.-8Q46PgfqtWvMfj-SKPFwvTY0IJ1cEeR0KyxfY")