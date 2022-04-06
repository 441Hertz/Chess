from discord.ext import commands
import discord
from Chess import Chess
from ImageBoard import ImageBoard

class CommandEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_let = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭']
        self.start_num = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣']
        self.final_let = ['A_', 'B_', 'C_', 'D_', 'E_', 'F_', 'G_', 'H_']   
        self.final_num = ['1_', '2_', '3_', '4_', '5_', '6_', '7_', '8_'] 
        self.start_let = ['🇪']
        self.start_num = ['2️⃣']
        self.final_let = ['E_']   
        self.final_num = ['4_']
        self.chess = Chess()
        self.board = ImageBoard(self.chess.board.board)
        
    async def load_reactions(self, board, extra):
        
        self.final_let = self.load_custom_emoji(self.final_let)
        self.final_num = self.load_custom_emoji(self.final_num)
        self.emojis = self.start_let + self.start_num + self.final_let + self.final_num
        
        for emoji in self.start_let:
            await board.add_reaction(emoji)
            
        for emoji in self.start_num:
            await extra.add_reaction(emoji)
            
        for emoji in self.final_let:
            await board.add_reaction(emoji)
            
        for emoji in self.final_num:
            await extra.add_reaction(emoji)
            
    @commands.command(name='play', aliases=['p'])
    async def play_game(self, ctx):
        # TODO 
        # Check for reaction - if in a certain list, such as num or let, check the index, 
        # pass the move to the game, which the game passes the board state to imageboard,
        # save the image, send that image to the chess channel, get that image link, edit the image url
        # reset the reactions
        # then we have to check for errors and how to print that out
        channel = self.bot.get_channel(961025712276525267)
        img = await channel.send(file=discord.File('assets/images/simple/default.png'))
        img_link = img.attachments[0]
        board = await ctx.send(img_link)
        extra = await ctx.send('** **')
        
        await self.load_reactions(board, extra)
        
        def check(reaction, user):
            return user == ctx.author and reaction.emoji in self.emojis
        while self.running():
            reactions = []
            emojis = []
            while not self.valid_reactions(emojis):
                reaction, user = await self.bot.wait_for("reaction_add", check=check)
                reactions.append(reaction)
                emojis.append(reaction.emoji)
                
            # start, final = self.emoji_to_pos(emojis)
            # self.chess.move(start, final)
            # self.board.generate_image(self.chess.board.board)
            # self.chess.board.print_board()
            
            # img = await channel.send(file=discord.File('assets/images/simple/board.png'))
            # img_link = img.attachments[0]
            # await board.edit(content=img_link)
            
            for reaction in reactions:
                await reaction.remove(user)
            await ctx.send('a')
            
    def valid_reactions(self, emojis):
        #TODO 
        #Better algorithm
        if len(emojis) != 4:
            return False
        start_let_count = 0
        start_num_count = 0
        final_let_count = emoji
        final_num_count = 0
        for emoji in emojis:
            start_let_count += self.start_let.count(emoji)
            start_num_count += self.start_num.count(emoji)
            final_let_count += self.final_let.count(emoji)
            final_num_count += self.final_num.count(emoji)
        return start_let_count == 1 and start_num_count == 1 \
            and final_let_count == 1 and start_num_count == 1
                
        
    def load_custom_emoji(self, names):
        emojis = []
        for name in names:
            emoji = discord.utils.get(self.bot.emojis, name=name)
            emojis.append(emoji)
        return emojis
        
        
    def running(self):
        return True
            
    def emoji_to_pos(self, reactions):
        letters = 'abcdefgh'
        numbers = '12345678'
        for reaction in reactions:
            if reaction in self.start_let:
                start_let = letters[self.start_let.index(reaction)]
            if reaction in self.start_num:
                start_num = numbers[self.start_num.index(reaction)]
            if reaction in self.final_let:
                final_let = letters[self.final_let.index(reaction)]
            if reaction in self.final_num:
                final_num = numbers[self.final_num.index(reaction)]
        start = start_let + start_num
        final = final_let + final_num        
        return start, final
        
    @commands.command()
    async def edit(self, ctx):
        await ctx.send("Hi \U0001f642")

    @commands.command()
    async def test(self, ctx):
        channel = self.bot.get_channel(961025712276525267)
        img = await channel.send(file=discord.File('assets/images/simple/default.png'))
        link = img.attachments[0]
        current = await ctx.send(link)
        img = await channel.send(file=discord.File('assets/images/simple/board.png'))
        link = img.attachments[0]
        current = await current.edit(content = link)
    


def setup(bot):
    bot.add_cog(CommandEvents(bot))