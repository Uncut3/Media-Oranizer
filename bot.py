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

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clean(ctx, limit: int = 500):
    await ctx.message.delete()
    target = bot.get_channel(TARGET_ID) or await bot.fetch_channel(TARGET_ID)
Collect all media files first
    media_items = []
    async for msg in ctx.channel.history(limit=limit, oldest_first=True):
        if msg.author.bot:
            continue
        if msg.attachments:
            files = [await att.to_file() for att in msg.attachments]
            caption = f"Uploaded by {msg.author.mention}\n{msg.content}".strip()
            media_items.append((caption, files, msg))
        else:
            await msg.delete()

Re-upload each media item to the target library and delete original
    for caption, files, original_msg in media_items:
        await target.send(content=caption, files=files)
        await original_msg.delete()

bot.run("MTUzOTYwMDExMzg4MDc5NzE4NA.GvpdW2.-8Q46PgfqtWvMfj-SKPFwvTY0IJ1cEeR0KyxfY")