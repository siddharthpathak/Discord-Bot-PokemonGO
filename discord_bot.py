import discord
from discord.ext import commands
from datetime import datetime, timedelta
import json

bot = commands.Bot(command_prefix='?',
                   description="Bot to help PokemonGO players"
                   )


@bot.event
async def on_ready():
    print('Ready')


@bot.event
async def on_member_join(member):
    """
        Greets a new user with a custom message
    """

    await bot.send_message(bot.get_channel(config_json['discord']['general_id']),
                           "Hello " + member.mention +
                           ". Welcome to the test server for Pokemon Go bot. Once features are tried and tested " 
                           "by some users we plan to move the bot to the main " 
                           "server on feature by feature basis. To start "
                           "testing and get more info about commands type ?help."
                           )


@bot.command(pass_context=True)
async def greet(ctx):
    """
        Greets the user with a classic Hello!
    """
    await bot.say("Hello " + ctx.message.author.mention + ":wave:")


@bot.command(pass_context=True)
async def role(ctx, *args):
    """
        Adds specified role to the user. Used to add Trainer role after user
        has read all the instructions,
        he/she can assign the role to unlock other channels
        Usage: ?role <role_name>
    """

    if len(args) != 1:

        await bot.say("Wrong usage. Try ?help role for help")

        role = discord.utils.get(ctx.message.author.server.roles, name=args[0])

        if role is not None:
            await bot.add_roles(ctx.message.author, role)
            await bot.say("Role added successfully")
        else:
            await bot.say("Invalid role entered")


@bot.command(pass_context=True)
async def report(ctx, *args):
    """
      To report a raid.
      Usage: ?report <egg_level> <location> <hatches/starts/pops> <time_left_to_start_in_mins>
      Usage: ?report <Pokemon> <location> <started/ends/popped/left/hatched> <time_left_in_mins>
      To report a raid about to start in 25 mins
      ?report Kyogre Innovation Center ends 25
    """

    try:

        report_time = args[-1]
        pokemon = args[0]

        if args[-2] in ["hatches", "starts", "pops"]:
            # reported time is the time remaining for the raid to start
            # add the reported time to current time, then add 45 mins to get the end time
            start_time = datetime.now() + timedelta(minutes=int(report_time))
            end_time = start_time + timedelta(minutes=45)
            await bot.add_reaction(ctx.message, "👍")
            await bot.send_message(bot.get_channel(config_json['discord']['etpo_id']), "Level " + pokemon + " at " +
                                   " ".join(args[1:-2]) + " - " + str(start_time.hour) + ":" + str(start_time.minute) +
                                   "-" + str(end_time.hour) + ":" + str(end_time.minute))

        elif args[-2] in ["ends", "hatched", "started", "popped", "left"]:
            # then it is time remaining
            # Add the reported time to current time
            end_time = datetime.now() + timedelta(minutes=int(report_time))
            await bot.add_reaction(ctx.message, "👍")
            await bot.send_message(bot.get_channel(config_json['discord']['etpo_id']), pokemon + " at "
                                   + " ".join(args[1:-2]) + " ends at " + str(end_time.hour) + ":"
                                   + str(end_time.minute) + "(in " + report_time + ")")

    except:
        # send out error
        await bot.add_reaction(ctx.message, "👎")
        await bot.say("Usage: ?report <egg_level> <location> <hatches/starts/pops> <time left to start>" +
                      "\nUsage: ?report <Pokemon> <location> <started/ends/popped/left/hatched> <time_left>" +
                      "\n?report Registeel Innovation Center hatches 25")


@bot.command(pass_context=True)
async def gym(ctx, *args):
    """
    Replies with the gym's location.
    Usage: ?gym <location>. Currently data is only for Innovation Center, Ruth Lily, and Disability Institute.

    """
    try:
        gym = "_".join(args).lower()
        await bot.say(" ".join(args) + ": " + config_json['gym_locations'][gym])
    except:
        await bot.say("Usage: ?gym <location>. "
                      "Currently data is only available for Innovation Center, Ruth Lily, and Disability Institute."
                      )

with open('config.json') as f:
    config_json = json.load(f)

bot.run(config_json['discord']['token'])


