from discord.ext import commands
import discord, asyncio
from Chess import Chess
from ImageBoard import ImageBoard

class CommandEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_let = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭']
        self.start_num = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣']
        self.final_let = ['A_', 'B_', 'C_', 'D_', 'E_', 'F_', 'G_', 'H_']   
        self.final_num = ['1_', '2_', '3_', '4_', '5_', '6_', '7_', '8_'] 
        # self.start_let = ['🇪']
        # self.start_num = ['2️⃣']
        # self.final_let = ['E_']   
        # self.final_num = ['4_']
        self.emoji_names = self.start_let + self.start_num + self.final_let + self.final_num
        
    async def load_reactions(self, board, extra):
        """ Loads the global list of emojis in self.emojis and also adds all the 
        required reactions to the 'board' and 'extra' message sent by to the bot    

        Args:
            board (discord.message.Message): The message sent by the bot containing the image of the board 
            extra (discord.message.Message): The message sent by the bot containing an 'empty' string
        """
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
        """ Plays the game by sending the link to the board image, calling the load_reactions() function, 
        checks for the adding and removing of reactions, then updates the board by editing the link of the board image

        Args:
            ctx (ctx): Context of command

        Returns:
            _type_: _description_
        """
        # TODO 
        # then we have to check for errors and how to print that out
        # Maybe add confirmation button?
        
        self.chess = Chess()
        self.board = ImageBoard(self.chess.board.board)
        
        channel = self.bot.get_channel(961025712276525267)
        img = await channel.send(file=discord.File('assets/images/simple/default.png'))
        img_link = img.attachments[0]
        board = await ctx.send(img_link)
        extra = await ctx.send('** **')
        
        await self.load_reactions(board, extra)
        
        def check_add(reaction, user):
            return user == ctx.author and reaction.emoji in self.emojis
        def check_remove(payload):
            user_id = payload.user_id
            return user_id == ctx.author.id and payload.emoji.name in self.emoji_names
            
        embed=discord.Embed(title="** **",
                        color=discord.Color.blue())
        e = await ctx.send(embed=embed)    
            
        running = True
        
        while running:
            reactions = []
            emojis = []
            
            while not self.valid_reactions(emojis):
                add = asyncio.create_task(self.bot.wait_for("reaction_add", check=check_add))
                remove = asyncio.create_task(self.bot.wait_for('raw_reaction_remove', check=check_remove))
                tasks = [add, remove]
                done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
                
                if add in done:
                    # For both standard and custom emojis, reaction contains the Reaction class for that emoji
                    # The emoji attribute of standard emojis are type str, while type Emoji class for custom emojis
                    # STANDARD reaction.emoji = str 
                    # CUSTOM reaction.emoji = Emoji class
                    reaction, user = await add
                    reactions.append(reaction)
                    emojis.append(reaction.emoji)
                elif remove in done:
                    # Should probably add a failsafe in the case where the user adds a reaction before the emojis
                    # have all been loaded, then removes the reaction afterwards
                    payload = await remove
                    emoji = payload.emoji
                    emoji_name = emoji.name
                    index = None
                    # If the reaction removed is custom, emoji = payload.emoji is the Emoji class, which is in emojis
                    if emoji in emojis:
                        index = emojis.index(emoji)
                    # If the reaction removed is standard, emoji_name is type str, which is in emojis
                    elif emoji_name in emojis:
                        index = emojis.index(emoji_name)
                    # Double failsafe against reaction removing problem
                    if index is not None:
                        del reactions[index]
                        del emojis[index]         

            start, final = self.emoji_to_pos(emojis)
            running = self.chess.move(start, final)
            
            # Error that I do not know how to fix: removing gives the same user id as the author (IDK WHY),
            # so if this is at the bottom, the last reaction removed will instantly trigger the,
            # asyncio.wait_for event, causing an index error
            for reaction in reactions:
                await reaction.remove(user)
            
            if self.chess.moved:
                self.board.generate_image(self.chess.board.board)
                self.chess.board.print_board()
                
                img = await channel.send(file=discord.File('assets/images/simple/board.png'))
                img_link = img.attachments[0]
                await board.edit(content=img_link)
                # TODO
                # Edit with custom piece emojis!
                embed=discord.Embed(title=f"{self.chess.msg}",
                        color=discord.Color.blue())
                await e.edit(embed=embed)
            else:
                embed=discord.Embed(title=f"{self.chess.error}",
                        color=discord.Color.blue())
                await e.edit(embed=embed)
            
    def valid_reactions(self, emojis):
        #TODO 
        #Better algorithm
        if len(emojis) != 4:
            return False
        start_let_count = 0
        start_num_count = 0
        final_let_count = 0
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
    async def test1(self, ctx):
        msg = await ctx.send("Hi \U0001f642")
        await msg.add_reaction(self.start_let[0])

    @commands.command()
    async def test2(self, ctx):
        channel = self.bot.get_channel(961025712276525267)
        img = await channel.send(file=discord.File('assets/images/simple/default.png'))
        link = img.attachments[0]
        current = await ctx.send(link)
        img = await channel.send(file=discord.File('assets/images/simple/board.png'))
        link = img.attachments[0]
        current = await current.edit(content = link)
    


def setup(bot):
    bot.add_cog(CommandEvents(bot))