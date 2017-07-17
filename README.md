# Alpha-Bot
Everything in one discord bot, written in discord.py

[Click here to invite the bot to your server](https://discordapp.com/oauth2/authorize?client_id=331841835733614603&scope=bot&permissions=201354247)

## Installation

1. Clone this repository
2. Install dependancies with `python -m pip install -r requirements.txt`
(replace 'python' with whatever other command you use to run python e.g. python3.6)
3. Run `main.py` for the first time
4. Edit the generated config.json file with your settings
5. Then you can run `main.py` normally

## Cogs

- [Here is a guide to writing your own cogs](https://twentysix26.github.io/Red-Docs/red_guide_make_cog/)
- Any cogs can be put into the cogs folder and will be loaded when you run the bot.
- The bot should work with most cogs, but just open an issue and I'll be happy to help.
- To load a cog without restarting the bot, run this bot command:

  `!reload cogs.name` where '!' is your bot's prefix and 'name' is the name of the cog file without the extension

## Dependancies

- [Discord.py](https://github.com/Rapptz/discord.py)
- [PrettyOutput](https://github.com/Aareon/prettyoutput)
