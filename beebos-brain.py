from interactions import listen, slash_command, SlashContext, Button, ButtonStyle, Modal, ModalContext, ShortText, ActionRow
from interactions.api.events import Component, ModalCompletion
from private.config import token
import interactions
import asyncio
import os
import aiohttp
import ast
import random
from interactions.ext.paginators import Paginator
import interactions.client.utils


########## MOVIES ##########


@slash_command(name="add-movie", description="Add a movie to Beebo's brain matrix")
async def my_command_function(ctx: SlashContext):
    my_modal = Modal(
        ShortText(
            label="Movie",
            custom_id="movie_text",
            required=True,
            placeholder="Movie name here",
            max_length=50,
        ),
        title="Movie Suggestion",
    )
    await ctx.send_modal(modal=my_modal)
    modal_ctx: ModalContext = await ctx.bot.wait_for_modal(my_modal)
    movie_text = modal_ctx.responses["movie_text"]
    await modal_ctx.send(f"Movie added by {modal_ctx.author.display_name}: {movie_text}", ephemeral=False, silent=True)
    with open("movie-list5.txt", "r") as f1:
        x = str(random.randint(100, 999))
        movie_list = f1.readlines()
        for i in movie_list:
            if x in i:
                x = str(random.randint(100, 999))
        with open("movie-list5.txt", "a") as f:
            f.write(f"{x}  -  {movie_text}: added by {modal_ctx.author.username}\n")
        with open("movie-users.txt", "r") as f2:
            if str(modal_ctx.author.username) in f2.read():
                print("user already in list")
            else:
                with open("movie-users.txt", "a") as f3:
                    f3.write(f"{modal_ctx.author.username}\n")

@slash_command(name="add-christmas-movie", description="Add a Christmas movie to Beebo's brain matrix")
async def my_command_function(ctx: SlashContext):
    my_modal = Modal(
        ShortText(
            label="Christmas",
            custom_id="christmas_text",
            required=True,
            placeholder="Christmas movie name here",
            max_length=50,
        ),
        title="Christmas Movie Suggestion",
    )
    await ctx.send_modal(modal=my_modal)
    modal_ctx: ModalContext = await ctx.bot.wait_for_modal(my_modal)
    christmas_text = modal_ctx.responses["christmas_text"]
    await modal_ctx.send(f"Christmas movie added by {modal_ctx.author.display_name}: {christmas_text}", ephemeral=False, silent=True)
    with open("movie-list5.txt", "r") as f1:
        x = str(random.randint(100, 999))
        christmas_list = f1.readlines()
        for i in christmas_list:
            if x in i:
                x = str(random.randint(100, 999))
        with open("movie-list5.txt", "a") as f:
            f.write(f"{x}  -  XMAS MOVIE -  {christmas_text}: added by {modal_ctx.author.username}\n")
        with open("christmas-users.txt", "r") as f2:
            if str(modal_ctx.author.username) in f2.read():
                print("user already in list")
            else:
                with open("christmas-users.txt", "a") as f3:
                    f3.write(f"{modal_ctx.author.username}\n")

@slash_command(name="list-movie", description="List all movies in Beebo's brain")
async def movie_list(ctx: SlashContext):
    with open("movie-list5.txt", "r") as f:
        movie_list = f.readlines()
        finallist = "".join(movie_list)
        paginator = Paginator.create_from_string (bot, finallist, page_size=2000)
        await paginator.send(ctx, ephemeral=True, silent=True)

@slash_command(name="roll-movie", description="Extract a movie from Beebo's brain")
async def movie_roll(ctx: SlashContext):
    x = 1
    while x:
        x = False
        randomuser = "x"
        with open("movie-users.txt", "r") as f1:
            user_list = f1.readlines()
            randomuser = random.choice(user_list)
            print(randomuser)
        with open("movie-list5.txt", "r") as f:
            movie_list = f.readlines()
            randomuserslist = []
            for i in movie_list:
                if randomuser in i:
                    randomuserslist.append(i)
            if len(randomuserslist) >= 3:
                randommovie = randomuserslist[random.randint(0, len(randomuserslist)-1)]
                justthemovie = randommovie.split(':')[0]
                await ctx.send(f"From deep within the folds of The Pit, a Selection by {randomuser} is born:\n {justthemovie}")
            else:
                await ctx.send(f"Beebo chose {randomuser}, but they haven't added enough movies (three) to be considered by His grace. Beebo will roll again")
                x = True

@slash_command(name="beebo-my-christmas", description="Extract a Christmas movie from Beebo's brain")
async def movie_roll(ctx: SlashContext):
    with open("christmas-users.txt", "r") as f1:
            user_list = f1.readlines()
            randomuser = random.choice(user_list)
            print(randomuser)
    with open("movie-list5.txt", "r") as f:
            movie_list = f.readlines()
            randomuserslist = []
            for i in movie_list:
                if randomuser in i and "XMAS MOVIE" in i:
                    randomuserslist.append(i)
            randommovie = randomuserslist[random.randint(0, len(randomuserslist)-1)]
            justthemovie = randommovie.split(':')[0]
            await ctx.send(f"From deep within the folds of The Pit, a Christmas Miracle by {randomuser} is born:\n {justthemovie}")

@slash_command(name="del-movie", description="Partially lobotomize Beebo")
async def delete_movie(ctx: SlashContext):
    my_modal = Modal(
        ShortText(
            label="Delete Movie",
            custom_id="movie_remove",
            required=True,
            placeholder="The # of the movie to delete. Use /list-movie to get #.",
            max_length=3,
        ),
        title="Movie # to Delete",
    )
    await ctx.send_modal(modal=my_modal)
    modal_ctx: ModalContext = await ctx.bot.wait_for_modal(my_modal)
    movie_remove = modal_ctx.responses["movie_remove"]
    with open("movie-list5.txt", "r") as f:
        lines= f.readlines()
        f.close()
        themovieinquestion = "x"
        for line in lines:
            if movie_remove in line:
                themovieinquestion = line
                moviestring=themovieinquestion[0:themovieinquestion.find(':')]
                if modal_ctx.author.username in themovieinquestion:
                    with open(r"movie-list5.txt", "w") as f:
                        for line in lines:
                         if line != themovieinquestion:
                             f.write(line)
                    await modal_ctx.send(f"Movie deleted by {modal_ctx.author.display_name}: {moviestring}", ephemeral=False, silent=True)
                else:
                    await modal_ctx.send(f"{modal_ctx.author.display_name} tried to remove {moviestring}, which does not belong to them. Shame them!", ephemeral=False, silent=True)
            f.close()

@slash_command(name="archive-movie", description="Archive a watched movie")
async def delete_movie(ctx: SlashContext):
    my_modal = Modal(
        ShortText(
            label="Archive Movie",
            custom_id="movie_archive",
            required=True,
            placeholder="The # of the movie to delete. Use /list-movie or /search to get #.",
            max_length=3,
        ),
        title="Movie # to Archive",
    )
    await ctx.send_modal(modal=my_modal)
    modal_ctx: ModalContext = await ctx.bot.wait_for_modal(my_modal)
    movie_remove = modal_ctx.responses["movie_archive"]
    with open("movie-list5.txt", "r") as f:
        lines= f.readlines()
        f.close()
        themovieinquestion = "x"
        for line in lines:
            if movie_remove in line:
                themovieinquestion = line
                moviestring=themovieinquestion[0:themovieinquestion.find(':')]
                with open("archive.txt", "a") as f1:
                    f1.write(themovieinquestion)
                    f1.close()
                with open(r"movie-list5.txt", "w") as f:
                    for line in lines:
                        if line != themovieinquestion:
                            f.write(line)
                await modal_ctx.send(f"Movie archived by {modal_ctx.author.display_name}: {moviestring}", ephemeral=False, silent=True)
            f.close()

########## GAMES ##########


@slash_command(name="add-game", description="Add a game to Beebo's brain matrix")
async def add_game(ctx: SlashContext):
    my_modal = Modal(
        ShortText(
            label="Game",
            custom_id="game_text",
            required=True,
            placeholder="Game name here",
            max_length=25,
        ),
        title="Game Suggestion",
    )
    await ctx.send_modal(modal=my_modal)
    modal_ctx: ModalContext = await ctx.bot.wait_for_modal(my_modal)
    game_text = modal_ctx.responses["game_text"]
    await modal_ctx.send(f"Game added by {modal_ctx.author.display_name}: {game_text}", ephemeral=False, silent=True)
    with open("game-list.txt", "r") as f:
        x = str(random.randint(100, 999))
        game_list = f.readlines()
        for i in game_list:
            if x in i:
                x = str(random.randint(100, 999))
        with open("game-list.txt", "a") as f:
            f.write(f"{x}  -  {game_text}: added by {modal_ctx.author.username}\n")
        with open("game-users.txt", "r") as f2:
            if str(modal_ctx.author.username) in f2.read():
                print("user already in list")
            else:
                with open("game-users.txt", "a") as f3:
                    f3.write(f"{modal_ctx.author.username}\n")

@slash_command(name="list-game", description="List all games in Beebo's brain")
async def game_list(ctx: SlashContext):
    with open("game-list.txt", "r") as f:
        game_list = f.readlines()
        finallist = "".join(game_list)
        paginator = Paginator.create_from_string (bot, finallist, page_size=2000)
        await paginator.send(ctx, ephemeral=True, silent=True)

@slash_command(name="roll-game", description="Extract a game from Beebo's brain")
async def game_roll(ctx: SlashContext):
    randomuser = "x"
    with open("game-users.txt", "r") as f1:
        user_list = f1.readlines()
        randomuser = random.choice(user_list)
    with open("game-list.txt", "r") as f:
        game_list = f.readlines()
        randomuserslist = []
        for i in game_list:
            if randomuser in i:
                randomuserslist.append(i)
        randomgame = randomuserslist[random.randint(0, len(randomuserslist)-1)]
        justthegame = randomgame.split(':')[0]
        await ctx.send(f"From deep within the folds of The Pit, a Selection by {randomuser} is born:\n {justthegame}") 

@slash_command(name="del-game", description="Partially lobotomize Beebo")
async def delete_game(ctx: SlashContext):
    my_modal = Modal(
        ShortText(
            label="Delete Game",
            custom_id="game_remove",
            required=True,
            placeholder="The # of the game to delete. Use /list-game to get #.",
            max_length=3,
        ),
        title="Game # to Delete",
    )
    await ctx.send_modal(modal=my_modal)
    modal_ctx: ModalContext = await ctx.bot.wait_for_modal(my_modal)
    game_remove = modal_ctx.responses["game_remove"]
    with open("game-list.txt", "r") as f:
        lines= f.readlines()
        f.close()
    thegameinquestion = "x"
    for line in lines:
        if game_remove in line:
            thegameinquestion = line
            gamestring=thegameinquestion[0:thegameinquestion.find(':')]
            if modal_ctx.author.username in thegameinquestion:
                with open(r"game-list.txt", "w") as f:
                    for line in lines:
                     if line != thegameinquestion:
                         f.write(line)
                await modal_ctx.send(f"Game deleted by {modal_ctx.author.display_name}: {gamestring}", ephemeral=False, silent=True)
            else:
                await modal_ctx.send(f"{modal_ctx.author.display_name} tried to remove {gamestring}, which does not belong to them. Shame them!", ephemeral=False, silent=True)
        f.close()


########## MISCELLANEOUS ##########

# This function I used to move existing movies without unique IDs 
## to a new file while giving each movie a unique ID
# Keep this here in case I need to do it again

#@slash_command(name="transfer-movie", description="import new movies")
#async def transfermovie(ctx: SlashContext):
    #with open("movie-list.txt", "r") as f:
        #movie_list = f.readlines()
        #for i in movie_list:
            #x = str(random.randint(100, 999))
            #while x in i:
                #x = str(random.randint(100, 999))
            #with open("movie-list5.txt", "a") as f:
                #f.write(f"{x}  - " + i)


@slash_command(name="escape-the-pit", description="button")
async def my_button_function2(channel: SlashContext):
    buttons: list[ActionRow] = [
        ActionRow(
            Button(
                style=ButtonStyle.GREEN,
                label="I'd like to leave",
                custom_id="leave",
            ),
            Button(
                style=ButtonStyle.RED,
                label="Succomb to my Fate",
                custom_id="stay",
            )
        )
    ]
    buttonsdisabled: list[ActionRow] = [
        ActionRow(
            Button(
                style=ButtonStyle.GREEN,
                label="I'd like to leave",
                disabled=True
            ),
            Button(
                style=ButtonStyle.RED,
                label="Succumb to my Fate",
                disabled=True
            )
        )
    ]
    message = await channel.send("You're stuck in Beebo's folds!", components=buttons, silent=True)
    async def check(component: Component) -> bool:
        if component.ctx.custom_id == "leave" :
            await component.ctx.send(component.ctx.author.display_name + " narrowly escapes with their life", silent=True)
            component.ctx.customid("stay").disabled = True
            return False
        elif component.ctx.custom_id == "stay" :
            await component.ctx.send(component.ctx.author.display_name + " is enveloped in His love", silent=True)
            component.ctx.customid("leave").disabled = True
            return False
    try:
        buttons: Component = await bot.wait_for_component(components=buttons,check=check,timeout=15)
    except BaseException:
        print("Timed Out!")
        await message.edit(components=buttonsdisabled)

@slash_command(name="touch", description="button")
async def my_button_function(channel: SlashContext):
  # need to defer it, otherwise, it fails
  button = Button(
      custom_id="my_button_id",
      style=ButtonStyle.GREEN,
      label="touch me",
  )
  message = await channel.send("Click my button", components=button, silent=True)
  async def check(component: Component) -> bool:
    if component.ctx.author.username.__contains__("lkjasldkfjlkjsdf"):
      await component.ctx.send("Fuck you " + component.ctx.author.display_name, silent=True)
      return False
    else:
      await component.ctx.send("I love you " + component.ctx.author.display_name, silent=True)
      return False
  try:
    component: Component = await bot.wait_for_component(components=button,
                                                             check=check,
                                                             timeout=5)
  except BaseException:
    print("Timed Out!")
    button.disabled = True
    await message.edit(components=button)

@slash_command(name="search", description="Retrieve pointed data from Beebo's mind-meat-matricies")
async def lookup_stuff(ctx: SlashContext):
    my_modal = Modal(
        ShortText(
            label="search",
            custom_id="find_this",
            required=True,
            placeholder="Search for a movie or game",
            max_length=25,
        ),
        title="Lookup Something",
    )
    await ctx.send_modal(modal=my_modal)
    modal_ctx: ModalContext = await ctx.bot.wait_for_modal(my_modal)
    find_this = modal_ctx.responses["find_this"]
    with open("game-list.txt", "r") as f:
        gameslines= f.readlines()
        f.close()
    with open("movie-list5.txt", "r") as d:
        movieslines = d.readlines()
        d.close()
    biglist = []
    for line in gameslines:
        if find_this.lower() in line.lower():
            biglist.append(line)
            #await modal_ctx.send(f"Game: {line}", ephemeral=False, silent=True)
    for line in movieslines:
        if find_this.lower() in line.lower():
            biglist.append(line)
            #await modal_ctx.send(f"Movie: {line}", ephemeral=False, silent=True)
    finallist = "".join(biglist)
    paginator = Paginator.create_from_string (bot, finallist, page_size=4000)
    if not biglist:
        await modal_ctx.send(f"Couldn't find: {find_this}", ephemeral=True, silent=True)
    else:
        await modal_ctx.send(f"Recods containing: {find_this}", ephemeral=True, silent=True)
        await paginator.send(ctx, ephemeral=True, silent=True)


    

########## BOT START ##########

print('starting bot...')
bot = interactions.Client(token=token,
                          intents=interactions.Intents.MESSAGES)
bot.start()
