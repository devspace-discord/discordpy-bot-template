from discord.ext import commands


class Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        
    @command.command(name='say')
    async def say_something(self, ctx, *, text):
        """Bot repeats what you put into the command"""
        
        await ctx.send(text)


def setup(bot):
    bot.add_cog(Commands(bot))
