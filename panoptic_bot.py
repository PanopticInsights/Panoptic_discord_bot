from discord.ext import commands
import discord
import datetime as dt
from gsvi.connection import GoogleConnection
from gsvi.timeseries import SVSeries
import matplotlib.pyplot as plt


def Token_read():
    with open('Token.txt', 'r') as f:
        lines = f.readlines()
        return lines[0].strip()


Token = Token_read()

client = commands.Bot(command_prefix='$')


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f"Hey {member.name}, welcome to the panoptic channel,"
                                 f"we provide data analytics and market insights ,"
                                 f"to access market trends and and visualization please type"
                                 f"$trends in the general trends")

    for channel in member.guild.channels:
        if str(channel) == "general":
            await channel.send(f"welcome to the server {member.mention}")


@client.event
async def on_member_remove(member):
    for channel in member.guild.channels:
        if str(channel) == "general":
            await channel.send(f"{member.mention} has left")


@client.command()
async def trends(ctx):
    await ctx.send(f"enter start year")
    message_response = await client.wait_for('message')
    start_year = int(message_response.content)
    print(start_year)

    await ctx.send(f"enter end year")
    message_response = await client.wait_for('message')
    end_year = int(message_response.content)
    print(end_year)

    await ctx.send(f"enter start month from range 1-12")
    message_response = await client.wait_for('message')
    start_month = int(message_response.content)
    print(start_month)

    await ctx.send(f"enter end month  range 1-12 ")
    message_response = await client.wait_for('message')
    end_month = int(message_response.content)
    print(end_month)

    await ctx.send(f"enter start day  range 1 - 30")
    message_response = await client.wait_for('message')
    start_day = int(message_response.content)
    print(start_day)

    await ctx.send(f"enter end day  1 - 30")
    message_response = await client.wait_for('message')
    end_day = int(message_response.content)
    print(end_day)

    await ctx.send(f"enter search word")
    message_response = await client.wait_for('message')
    search_word = str(message_response.content)
    print(search_word)

    await ctx.send(f"enter region")
    message_response = await client.wait_for('message')
    region = str(message_response.content)
    print(region)

    start = dt.datetime(year=start_year, month=start_month, day=start_day)
    end = dt.datetime(year=end_year, month=end_month, day=end_day)

    connection = GoogleConnection()
    series = SVSeries.univariate(
        connection=connection,
        query={'key': search_word, 'geo': region},
        start=start, end=end, granularity='MONTH'
    )

    google_data = series.get_data()

    plt.plot(google_data)
    plt.savefig("pic.jpeg")


@client.command()
async def viz(ctx):
    file = discord.File("pic.jpeg", filename="pic.jpeg")
    await ctx.send("pic.jpeg", file=file)


client.run(Token)
