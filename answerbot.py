'''
using discord.py version 1.0.0a
'''
import discord
import asyncio
import re
import multiprocessing
import threading
import concurrent

BOT_OWNER_ROLE = 'RUNNER' # change to what you need
  
 

 
oot_channel_id_list = ["713354337539194920","713349059259400243","713398517544255599","714446952586280992","713398517544255599","719509244952576071"]
answer_pattern = re.compile(r'(not|n|e)?([1-3]{1})(\?)?(cnf|cf|sure|s)?(\?)?$', re.IGNORECASE)

apgscore = 2952
nomarkscore = 521
markscore = 289

async def update_scores(content, answer_scores):
    global answer_pattern

    m = answer_pattern.match(content)
    if m is None:
        return False

    ind = int(m[2])-1

    if m[1] is None:
        if m[3] is None:
            if m[4] is None:
                answer_scores[ind] += nomarkscore
            else: # apg
                if m[5] is None:
                    answer_scores[ind] += apgscore
                else:
                    answer_scores[ind] += markscore

        else: # 1? ...
            answer_scores[ind] += markscore

    else: # contains not or n
        if m[3] is None:
            answer_scores[ind] -= nomarkscore
        else:
            answer_scores[ind] -= markscore

    return True

class SelfBot(discord.Client):

    def __init__(self, update_event, answer_scores):
        super().__init__()
        global oot_channel_id_list
        self.oot_channel_id_list = oot_channel_id_list
        self.update_event = update_event
        self.answer_scores = answer_scores

    async def on_ready(self):
        print("======================")
        print("Trivia Self Bot")
        print("Connected to discord.")
        print("User: " + self.user.name)
        print("ID: " + str(self.user.id))

    # @bot.event
    # async def on_message(message):
    #    if message.content.startswith('-debug'):
    #         await message.channel.send('d')

        def is_scores_updated(message):
            if message.guild == None or \
                str(message.channel.id) not in self.oot_channel_id_list:
                return False

            content = message.content.replace(' ', '').replace("'", "")
            m = answer_pattern.match(content)
            if m is None:
                return False

            ind = int(m[2])-1

            if m[1] is None:
                if m[3] is None:
                    if m[4] is None:
                        self.answer_scores[ind] += nomarkscore
                    else: # apg
                        if m[5] is None:
                            self.answer_scores[ind] += apgscore
                        else:
                            self.answer_scores[ind] += markscore

                else: # 1? ...
                    self.answer_scores[ind] += markscore

            else: # contains not or n
                if m[3] is None:
                    self.answer_scores[ind] -= nomarkscore
                else:
                    self.answer_scores[ind] -= markscore

            return True

        while True:
            await self.wait_for('message', check=is_scores_updated)
            self.update_event.set()

class Bot(discord.Client):

    def __init__(self, answer_scores):
        super().__init__()
        self.bot_channel_id_list = []
        self.embed_msg = None
        self.embed_channel_id = None
        self.answer_scores = answer_scores

        # embed creation
        self.embed=discord.Embed(title="__Trivia Support Pro🥒__", description= '```Đã kết nối tới con Mail+...🤖```',colour = discord.Colour.red())
        self.embed.set_author(name ='',url=' ',icon_url='https://cdn.discordapp.com/attachments/699517929435168768/711962977296973864/1589813196193.jpg')
        self.embed.add_field(name="Option 1", value="0", inline=False)
        self.embed.add_field(name="Option 2", value="0", inline=False)
        self.embed.add_field(name="Option 3", value="0", inline=False)
        self.embed.add_field(name="__Answer__",value=":mag:")
        self.embed.set_footer(text='  Trivia Support Pro 🥒 | MADE ♥️ BY TINHHUYNH',icon_url = "https://cdn.discordapp.com/attachments/682520648823603201/689411362304032796/JPEG_20200317_151913.jpg?width=240&height=428")
        self.embed.set_footer(text=f"Tinhhuynh", \
            icon_url="https://cdn.discordapp.com/attachments/578965576651898890/595128602081755136/Lol_question_mark.png")
        self.embed.set_image(url = 'https://cdn.discordapp.com/attachments/539066238870224903/606135147913543693/Tw_1-1-1.gif')
        # await self.bot.add_reaction(embed,':spy:')


    async def clear_results(self):
        for i in range(len(self.answer_scores)):
            self.answer_scores[i]=0

    async def update_embeds(self):

         

        one_check = ""
        two_check = ""
        three_check = ""
        four_check = ""
        

        lst_scores = list(self.answer_scores)

        highest = max(lst_scores)
#         lowest = min(lst_scores)
        answer = lst_scores.index(highest)+1
        best=":mag:"
         

        if highest > 0:
            if answer == 1:
                one_check = " :white_check_mark: "
            else:
                one_check=":x:"
            if answer ==1:
                best=":one:"
            if answer == 2:
                two_check = " :white_check_mark: "
            else:
                two_check= ":x:"
            if answer == 2:
                best=":two:"
            if answer == 3:
                three_check = " :white_check_mark: "
            else:
                three_check= ":x:"
            if answer == 3:
                best=":three:"
            if answer == 4:
              four_check = " :white_check_mark:"
            else:
                four_check=":x:"
            if answer == 4:
                best=":four:"
                
#         if lowest < 0:
#             if answer == 1:
#                 one_check = ":x:"
#             if answer == 2:
#                 two_check = ":x:"
#             if answer == 3:
#                 three_check = ":x:"            
 
        self.embed.set_field_at(0, name="Option 1", value="**{0}**{1}".format(lst_scores[0], one_check))
        self.embed.set_field_at(1, name="Option 2", value="**{0}**{1}".format(lst_scores[1], two_check))
        self.embed.set_field_at(2, name="Option 3", value="**{0}**{1}".format(lst_scores[2],three_check))
      
        self.embed.set_field_at(3,name="__Answer__",value=best)
        self.embed.set_footer(text='  Trivia Support Pro 🥒 | MADE ♥️ BY TINHHUYNH',icon_url = "https://cdn.discordapp.com/attachments/682520648823603201/689411362304032796/JPEG_20200317_151913.jpg?width=240&height=428")
        self.embed.set_thumbnail(url =  'https://cdn.discordapp.com/attachments/707193199151677461/707200954424098866/1588680101537.jpg')
        self.embed.set_image(url = 'https://cdn.discordapp.com/attachments/539066238870224903/606135147913543693/Tw_1-1-1.gif')
        

        if self.embed_msg is not None:
            await self.embed_msg.edit(embed=self.embed)

    async def on_ready(self):
        print("==============")
        print("Nelson Trivia")
        print("Connected to discord.")
        print("User: " + self.user.name)
        print("ID: " + str(self.user.id))

        await self.clear_results()
        await self.update_embeds()
        await self.change_presence(activity=discord.Game(name='command: m'))

    async def on_message(self, message):

        # if message is private
        if message.author == self.user or message.guild == None:
            return

        if message.content.lower() == "m":
            await message.delete()
            if BOT_OWNER_ROLE in [role.name for role in message.author.roles]:
                self.embed_msg = None
                await self.clear_results()
                await self.update_embeds()
                self.embed_msg = \
                    await message.channel.send('',embed=self.embed)
                await self.embed_msg.add_reaction("✅")
                #await self.embed_msg.add_reaction("âœ”")
                await self.embed_msg.add_reaction("❌")
                self.embed_channel_id = message.channel.id
            else:
                await message.channel.send("**Lol** You Not Have permission To Use This **cmd!** :stuck_out_tongue_winking_eye:")
            return

        if message.content.startswith('+extessr'):
          if BOT_OWNER_ROLE in [role.name for role in message.author.roles]:
           embed = discord.Embed(title="Help Commands", description="**How to Run Bot**", color=0x00ff00)
           embed.add_field(name="Support Game", value="**Loco\nBrainbaazi\nPollbaazi\nSwag-iq\nThe-Q\nConfett-India\nCash-Quiz-Live\nHQ\nconfetti Mexico\nte-media\nmocha Vietnam\nconfetti Vietnam\nmomo Vietnam Tivia\n\nJeetoh Answer For `+j`**", inline=False)
           embed.add_field(name="when Question come put command", value="** + is command work for all support game**", inline=False)
           await message.channel.send(embed=embed)

        # process votes
        if message.channel.id == self.embed_channel_id:
            content = message.content.replace(' ', '').replace("'", "")
            updated = await update_scores(content, self.answer_scores)
            if updated:
                await self.update_embeds()

def bot_with_cyclic_update_process(update_event, answer_scores):

    def cyclic_update(bot, update_event):
        f = asyncio.run_coroutine_threadsafe(bot.update_embeds(), bot.loop)
        while True:
            update_event.wait()
            update_event.clear()
            f.cancel()
            f = asyncio.run_coroutine_threadsafe(bot.update_embeds(), bot.loop)
            #res = f.result()

    bot = Bot(answer_scores)

    upd_thread = threading.Thread(target=cyclic_update, args=(bot, update_event))
    upd_thread.start()

    loop = asyncio.get_event_loop()
    loop.create_task(bot.start('NzE0NTE4MjUyNjk2NTAyMzEy.Xsv1Bw.0Bp029hh7tmtpgrV4IWSFXNXDso'))
    loop.run_forever()


def selfbot_process(update_event, answer_scores):

    selfbot = SelfBot(update_event, answer_scores)

    loop = asyncio.get_event_loop()
    loop.create_task(selfbot.start('NTczMzU3OTAzNzQyODk0MDgw.Xsdcdw.rq6kRk3BW08d0qivoRfV5ZPseQo',
                                   bot=False))
    loop.run_forever()

if __name__ == '__main__':

    # running bot and selfbot in separate OS processes

    # shared event for embed update
    update_event = multiprocessing.Event()

    # shared array with answer results
    answer_scores = multiprocessing.Array(typecode_or_type='i', size_or_initializer=4)

    p_bot = multiprocessing.Process(target=bot_with_cyclic_update_process, args=(update_event, answer_scores))
    p_selfbot = multiprocessing.Process(target=selfbot_process, args=(update_event, answer_scores))

    p_bot.start()
    p_selfbot.start()

    p_bot.join()
    p_selfbot.join()
