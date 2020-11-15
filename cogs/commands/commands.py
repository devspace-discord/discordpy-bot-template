from discord.ext import commands


class Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        
    @command.command(name='say')
    async def say_something(self, ctx, *, text):
        """Bot repeats what you put into the command"""
        
        await ctx.send(text)
        
    @command.command(name='latency', aliases=['ping'])
    async def ping_pong(self, ctx):
        """Sends the latency between Discord and the bot"""
        
        await ctx.send(f'Latency: `{round(self.bot.latency*1000, 2)}` ms')


def setup(bot):
    bot.add_cog(Commands(bot))
