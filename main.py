import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
from mapLeaderboard import mapLeaderboard, collection
from keep_alive import keep_alive

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

keep_alive()

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

#VARIABLES
mapLeaderboards = {}

def has_administrator(ctx):
    return ctx.author.guild_permissions.administrator

@bot.event
async def on_ready():
    async for doc in collection.find({}):
        map_name = doc['map_leaderboard']
        mapLeaderboards[map_name] = mapLeaderboard(map_name)
    return

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

@bot.command()
async def times(ctx, map_name: str):
    map_name = map_name.lower()
    if map_name not in mapLeaderboards:
        await ctx.send(f"No times for map {map_name}.")
        return
    times = (await mapLeaderboards[map_name].get_times())[:10] # Get top 10 times
    times_str = "\n".join([f"{i+1}. {user}: {time}" for i, (user, time) in enumerate(times)])
    embed = discord.Embed(
        title=f"Times for map {map_name}:",
        description=times_str if times_str else "No times yet."
    )
    await ctx.send(embed=embed)

@bot.command()
async def submit(ctx, map_name: str, time: float):
    map_name = map_name.lower()
    if map_name not in mapLeaderboards:
        # create a new mapLeaderboard instance if it doesn't exist
        mapLeaderboards[map_name] = mapLeaderboard(map_name)
    await mapLeaderboards[map_name].add_time(ctx.author.name, time)
    await ctx.send(f"Time {time} submitted for map {map_name} by {ctx.author.name}.")

@bot.command()
async def maplist(ctx):
    if not mapLeaderboards:
        await ctx.send("No maps exist.")
        return
    maps_list = "\n".join(mapLeaderboards.keys())
    await ctx.send(f"**Maps with recorded times:**\n{maps_list}")

@bot.command()
async def deletemap(ctx, map_name: str):
    if not has_administrator(ctx):
        await ctx.send("You do not have permission to use this command.")
        return
    map_name = map_name.lower()
    if map_name not in mapLeaderboards:
        await ctx.send(f"No map {map_name}.")
        return
    await mapLeaderboards[map_name].delete_file()
    del mapLeaderboards[map_name]
    await ctx.send(f"All times for map {map_name} have been deleted.")

@bot.command()
async def removetime(ctx, map_name: str, index: int):
    if not has_administrator(ctx):
        await ctx.send("You do not have permission to use this command.")
        return
    map_name = map_name.lower()
    if map_name not in mapLeaderboards:
        await ctx.send(f"No map {map_name}.")
        return
    await mapLeaderboards[map_name].remove_time(index - 1)  # Convert to 0-based index
    await ctx.send(f"Time {index}. removed from map {map_name}.")

# Run the bot
bot.run(token, log_handler=handler, log_level=logging.DEBUG)