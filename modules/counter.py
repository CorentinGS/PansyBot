import asyncio
from datetime import datetime

import discord

from utils.essentials import sql


async def scheduler(bot):
    while True:
        now = datetime.now()
        new_date = datetime(now.year, now.month, now.day + 1, 0, 0)
        time = (now - new_date).microseconds
        await asyncio.sleep(time)
        await send_daily_embed(bot)
        await get_winner(bot)
        await send_embed(bot)


async def send_embed(bot):
    final = ""
    x = 0
    channel = bot.get_channel(674702745772752905)
    em = discord.Embed(
        title="MAL Top Winners",
        colour=0xeb8034,
    )
    scoreboard = sql.fetch_counter_leaderboard()
    for user in scoreboard:
        member = bot.get_user(user)
        points = sql.fetch_points(user)
        x += 1
        desc = f"`{x}. `**Points:**{points}{member.name}#{member.discriminator}\n"
        final = final + desc
    em.description = final
    await channel.send(embed=em)


async def send_daily_embed(bot):
    channel = bot.get_channel(674702745772752905)
    main_winner, global_winner, cotd_winner = sql.get_winners()

    em = discord.Embed(
        title="MAL Top Winners",
        colour=0xeb8034,
    )
    member = bot.get_user(main_winner)
    points = sql.get_main_counter(main_winner)
    em.add_field(name="Main Chat Winner!",
                 value=f"Congratulations {member.mention}, you're our winner for main chat today!\nYou've sent the most {points} messages in #main chat")

    member = bot.get_user(global_winner)
    points = sql.get_main_counter(global_winner)
    em.add_field(name="Global Chat Winner!",
                 value=f"Congratulations {member.mention}, you're our winner for main chat today!\nYou've sent the most {points} messages in every chat")

    member = bot.get_user(cotd_winner)
    points = sql.get_main_counter(cotd_winner)
    em.add_field(name="Cotd Chat Winner!",
                 value=f"Congratulations {member.mention}, you're our winner for main chat today!\nYou've sent the most {points} messages in #cotd chat")
    await channel.send(embed=em)


async def get_winner(bot):
    main_winner, global_winner, cotd_winner = sql.get_winners()
    list_users = [main_winner, global_winner, cotd_winner]
    sql.update_counter_leaderboard(main_winner)
    sql.update_counter_leaderboard(global_winner)
    sql.update_counter_leaderboard(cotd_winner)
    guild: discord.Guild = bot.get_guild(540784184470274069)
    role = guild.get_role(677296412882370590)
    for member in role.members:
        await member.remove_roles(role)
    for m in list_users:
        member: discord.Member = guild.get_member(m)
        await member.add_roles(role)
    sql.reset_data()
