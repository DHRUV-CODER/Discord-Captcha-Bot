import os
import discord
from discord.ext import commands
import requests as r
import datetime
import math
import keep_alive
my_secret = os.environ['TOKEN']
intents = discord.Intents().all()
client = commands.Bot(command_prefix='>',
                      description="This is A Captcha Bot",
                      intents=intents)


@client.event
@commands.cooldown(60 * 60, 30 * 30, commands.BucketType.user)
async def on_member_join(member):

    while True:
        verified = discord.utils.get(member.guild.roles, name="Verified")
        res = r.get(
            'https://captcha-image-api.dhruvnation1.repl.co/gimme/some/captcha'
        ).json()
        captcha_answer = res['asked_query']
        embed = discord.Embed(
            title="Answer The Captcha",
            description=
            f"```fix\nHi {member.name}\n{member.name} you wont be able to talk until you finish this\nPlease Type The Follwoing Captcha To Access The Server!!\n\nSteps:\n1)Type The letter Given In BElow Image down Here\n2)Done!!\n```"
        )
        embed.set_image(url=res['img_url'])
        await member.send(embed=embed)
        msg = await client.wait_for("message")
        if msg.content == captcha_answer:
            await member.send("We got To know you Are Human , Thats Great . Now You Will be Able To Talk in Server. Have A Pleasant Stay")
            await member.add_roles(verified, reason="None")
            break
        else:
            await member.send("\n\n__Try Again__\n\n")
            pass


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        # await ctx.send(f"{error} ")
        cooldown_time = str(
            datetime.timedelta(seconds=math.trunc(error.retry_after)))
        if cooldown_time == "0:00:00":
            await ctx.send("ik you are too desperate wait for 1 sec atleast")
        elif cooldown_time == "0:00:01":
            await ctx.send("ik you are too desperate wait for 1 sec atleast")
        else:
            await ctx.send(
                f"Fam You Are On Cooldown . Wait For like  {cooldown_time}")
    else:
        raise error

keep_alive.keep_alive()
client.run(my_secret)
