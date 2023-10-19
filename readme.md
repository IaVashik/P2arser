# P2ARCER

## Description:
Steam Workshop parser for Portal 2 to search for specified words in new and updated maps.


## Installation 

1. Clone the repository:

```
git clone https://github.com/IaVashik/P2arser.git
```

2. Install requirements:

```
pip install -r requirements.txt
```

3. Rename `config.json_example` to `config.json`

4. Populate config.json with:

Key | Description
--|--
API_KEY | Steam API key
Tg_bot_token | Telegram bot API token 
Tg_chat_id | Telegram chat ID to send notifications
delay | Workshop check interval in seconds
Check_map_content | Search words in map content (true/false)
Check_map_description | Search words in map description (true/false)
desired_content | List of words to search for
DEBUG | Enable debug logging (true/false)

5. Run the bot:

```
python main.py
```

It will periodically check Portal 2 workshop for updates and send maps containing searched words to Telegram.

## Usage

- Specify words to search for in desired_content
- Run main.py for continuous monitoring
- Get Telegram notifications when matching maps are found

## Steam API Key Information
In order to use this code, you need to provide your own Steam API key (for WorkshopMetadataExtract). To obtain an API key, visit the [Steam API Key registration page](https://steamcommunity.com/dev/apikey). Please note that due to Valve's policies, a Steam API key is mandatory. Additionally, if you want to download content from the workshop, you must have a copy of the game associated with the workshop file on your account :<

## License
WME is licensed under the [MIT License](https://github.com/example/project/blob/main/LICENSE). You are free to use, modify and share this library under the terms of the MIT License. The only condition is keeping the copyright notice, and stating whether or not the code was modified.