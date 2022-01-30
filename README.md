# [How to use the OTP Bot to receive verification-codes & more](http://discord.verify.gay)

Please Note, that you should create your own instance and not ask someone to setup it for you. The Bot store your API-Key inside a Database so the owner can see all added keys and that is the main reason, why you not should trust anyone that connect the bot with a own Database.


__Requirements:__
- Python installed on your OS
- 5sim.net account with some Founds on it
- MongoDB Account
- Discord Bot with commands. Application & all intents enabled (https://discord.dev)

__Setup the Discord-Bot:__
- enable required intents:
![image](https://user-images.githubusercontent.com/94435104/151340237-4945cffd-5a8b-46fb-9aac-d78470e5669c.png)

- check all required checkboxes:
![image](https://user-images.githubusercontent.com/94435104/151340371-7cac600d-818c-49bf-b371-301c78ad7dab.png)

- Open the file called `app.json`
- Edit the 3 description values inside the env option
- Database URL (e.g. mongodb://localhost:27017) get this one from the MongoDB Website
- Whitelist your Public IP for accessing the MongoDB Database
- Collection Name (Name of the Collection where Users and their API is stored)
- Discord Token (Your Bot token so the Program can login in the Bot account)
- Invite the Bot to your Server
- Type `/` to see all commands you can use and choose the one you like to use 

5sim.net is a service, that offer you temp phonenumbers for otp verification. 
It include a lot of countries you can choose from. 
I might add vak-sms.com as this is the cheapest solution at the moment!
The Project use the API to get numbers, check for verifycodes & more. It is added within a discordbot and uses slashcommands
Slashcommands working similar to usual ones but are more integraded within Discord so typing / will suggest possible avaible commands and shows what args are needed
Its more easy to use then using a custom prefix like ! and run a helpcommand to list all commands. It is secure and will only show the responses on your side in a hidden embed.
This embed will only be shown to you so its not possible for the owner to login into the bot and see the secret stuff. 
You can run these commands in Guilds or DMs with no risk of the data being leaked

I am looking for Suggestions to keep this Project updated. Any suggestion or feature you might want me to add you can tell me by clicking on issues and choose the suggestion. Or you can use the Discordlink above to suggest things. i try to be more active, push out more opensouce projects and so on. I like to help you guys out with anything that is related to coding on my Discordserver.)
