"""
Bot codes
"""


import os
from dotenv import load_dotenv

# saving df to image
import dataframe_image as dfi

# Discord
import discord
from discord.ext import commands

# Riot util func.
from riot import get_summoner_rank, previous_match

intents = discord.Intents.default()
intents.members = True  # Subscribe to the privileged members intent.

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
LOCAL_BOT_PREFIX = os.getenv("LOCAL_BOT_PREFIX")

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(LOCAL_BOT_PREFIX), intents=intents
)


@bot.event
async def on_ready():
    """Prints that the bot is connected"""
    print(f"{bot.user.name} has connected to Discord!")


@bot.event
async def on_member_join(member):
    """Sends personal discord message to the membed who join"""
    # create a direct message channel.
    await member.create_dm()
    # Send welcome msg.
    await member.dm_channel.send(f"Hi {member.name}, welcome to 관전남 월드!")


# TODO: Issues #5 help command.
# remove default help command to use our help command
bot.remove_command("help")

# Custom help command
@bot.command(name="help", help="This is help command")
async def help(ctx):
    # Create to display help command in embedded format
    helpEmbed = discord.Embed(
        title=f"How to use {bot.user.name}",
        description=f"<@!{bot.user.id}> <command>",
        color=discord.Color.gold(),
    )

    # ADD author to embed (URL and Image can be changed whatever we want eg.our website and logo)
    # helpEmbed.set_author(
    #     name=f"{bot.user.name}",
    #     icon_url="https://i.imgur.com/KE9LBHL.png",
    # )

    # ADD thumbnail (Image can be changed whatever we want. eg.our logo)
    helpEmbed.set_thumbnail(url="https://emoji.gg/assets/emoji/3907_lol.png")

    # ADD fields
    # helpEmbed.add_field(name="How to mention", value=f"<@!{bot.user.id}>", inline=False)
    # helpEmbed.add_field(
    #     name="** **", value="** **", inline=False
    # )  # This line for line spacing

    # helpEmbed.add_field(
    #     name="** **",
    #     value=f"<@!{bot.user.id}> <command>",
    #     inline=False,
    # )

    helpEmbed.add_field(
        name="** **",
        value="**The list of command examples**",
        inline=False,
    )

    helpEmbed.add_field(
        name="** **",
        value=f"`1.{help.name}` \n {help.help}",
        inline=False,
    )

    # Add empty field to keep formatting neat (1 per 2 fields)
    # helpEmbed.add_field(name="\b", value="\b", inline=True)

    helpEmbed.add_field(
        name="** **",
        value=f"`2.{get_command_description.name}` \n {get_command_description.help}",
        inline=False,
    )

    helpEmbed.add_field(
        name="** **",
        value=f"`3.{get_rank.name} [userID]` \n {get_rank.help}",
        inline=False,
    )

    # helpEmbed.add_field(name="\b", value="\b", inline=True)

    helpEmbed.add_field(
        name="** **",
        value=f"`4.{get_last_match.name} [userID]` \n {get_last_match.help}",
        inline=False,
    )

    # ADD footer with line spacing
    # helpEmbed.add_field(name="\u200B", value="\u200B", inline=False)
    # helpEmbed.set_footer(
    #     text="This is footer:{}".format(bot.user.name),
    #     icon_url="https://i.imgur.com/KE9LBHL.png",
    # )
    await ctx.send(embed=helpEmbed)


# Create commands command for a description of all of the commands
@bot.command(name="commands", help="Description of all of the commands")
async def get_command_description(ctx):
    embed = discord.Embed(
        title="All of the commands",
        description="Detailed explanation of each command",
        color=discord.Color.dark_teal(),
    )
    embed.add_field(name="** **", value="** **", inline=False)

    embed.add_field(
        name=f"`{help.name}`",
        value=f"**Description** : {help.help}\n **Syntax** : ```@{bot.user.name} {help.name}```",
        inline=False,
    )
    embed.add_field(name="** **", value="** **", inline=False)

    embed.add_field(
        name=f"`{get_command_description.name}`",
        value=f"**Description** : {get_command_description.help}\n **Syntax** : ```@{bot.user.name} {get_command_description.name}```",
        inline=False,
    )
    embed.add_field(name="** **", value="** **", inline=False)

    embed.add_field(
        name=f"`{get_rank.name}`",
        value=f"**Description** : {get_rank.help}\n **Syntax** : ```@{bot.user.name} {get_rank.name} [userID]```",
        inline=False,
    )
    embed.add_field(name="** **", value="** **", inline=False)

    embed.add_field(
        name=f"`{get_last_match.name}`",
        value=f"**Description** : {get_last_match.help}\n **Syntax** : ```@{bot.user.name} {get_last_match.name} [userID]```",
        inline=False,
    )
    embed.add_field(name="** **", value="** **", inline=False)

    await ctx.send(embed=embed)


@bot.command(name="rank", help="Get rank of summoner")
async def get_rank(ctx, name: str):
    """Sends the summoner's rank information to the bot"""
    summoner_info = get_summoner_rank(name)

    embed = discord.Embed(title="Solo/Duo Rank", color=discord.Color.dark_gray())

    summoner_name = summoner_info["user_name"]

    # Removing space of the summoner name to access op.gg url of the summoner
    summoner_name_opgg = summoner_name.replace(" ", "")
    print(summoner_info["summoner_icon_image_url"])
    # Add author, thumbnail, fields, and footer to the embed
    embed.set_author(
        name=summoner_name,
        url=f"https://na.op.gg/summoner/userName={summoner_name_opgg}",
        icon_url=summoner_info["summoner_icon_image_url"],
    )

    # Get image of tier by path
    tier_image = summoner_info["tier_image"]
    file = discord.File(tier_image)
    # Need to get the filename in order to attach to the thumbnail
    tier_image_filename = tier_image.replace("ranked-emblems/", "")
    # Embed thumbnail image of tier at the side of the embed
    embed.set_thumbnail(url=f"attachment://{tier_image_filename}")

    # Setting variables for summoner information to display as field
    summoner_rank = summoner_info["tier"]
    solo_win = summoner_info["solo_win"]
    solo_loss = summoner_info["solo_loss"]
    summoner_total_game = solo_win + solo_loss
    solo_rank_percentage = int(solo_win / summoner_total_game * 100)

    embed.add_field(
        name=summoner_rank,
        value="Total Games Played:"
        + f"{summoner_total_game}\n{solo_win}W \
          {solo_loss}L {solo_rank_percentage}%",
        inline=False,
    )
    await ctx.send(file=file, embed=embed)


@bot.command(name="last_match", help="Get last match history")
async def get_last_match(ctx, name: str):
    """Sends the summoner's last match information to the bot"""
    last_match_info = previous_match(name)
    dfi.export(last_match_info, "df_styled.png")
    file = discord.File("df_styled.png")
    embed = discord.Embed()
    embed.set_image(url="attachment://df_styled.png")
    await ctx.send(embed=embed, file=file)
    os.remove("df_styled.png")


@bot.event
async def on_command_error(ctx, error):
    """Checks error and sends error message if exists"""
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send("You do not have the correct role for this command.")


bot.run(TOKEN)
