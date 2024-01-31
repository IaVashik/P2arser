import requests
import aiogram
from aiogram.enums.parse_mode import ParseMode


class Gotify:
    def __init__(self, ip, token, default_name = "gotify"):
        self.url = f"http://{ip}/message?token={token}"
        self.default_name = default_name
        
    def send(self, message, priority = 2, title = None):
        requests.post(self.url, json={
            "message": str(message),
            "priority": priority,
            "title": title or self.default_name
        })
        


class tgBot:
    def __init__(self, token) -> None:
        self.bot = aiogram.Bot(token=token)
        # self.dp = aiogram.Dispatcher(self.bot)
    
        
    async def send(self, chat_id, message, file = None, disable_notif = True):
        messages = await self._process_msg(message)
        if not file:
            await self._send_message(chat_id, messages, disable_notif)
        else:
            await self._send_file(chat_id, messages, file, disable_notif)
    
    
    async def _send_message(self, chat_id, messages, disable_notif):
        for msg in messages:
            await self.bot.send_message(chat_id, text=msg, parse_mode=ParseMode.MARKDOWN,
                                        disable_web_page_preview=True, disable_notification=disable_notif)


    async def _send_file(self, chat_id, messages, file, disable_notif):
        last_msg = messages.pop()
        if len(messages) > 0: # wtf brou
            await self._send_message(messages, chat_id, disable_notif)
            
        document = aiogram.types.FSInputFile(file)
        await self.bot.send_document(chat_id=chat_id, document=document, caption=last_msg, 
                                        parse_mode=ParseMode.MARKDOWN, disable_notification=disable_notif)
    
    
        
    async def _process_msg(_, text):
        if len(text) <= 4000:
            return [text]
        
        result = []
        remaining_text = text

        while len(remaining_text) > 0:
            if len(remaining_text) <= 4000:
                result.append(remaining_text)
                break

            msg_chunk = remaining_text[:4000]
            last_dot_index = msg_chunk.rfind('.')
            
            if last_dot_index != -1:
                substr = msg_chunk[:last_dot_index + 1]
                result.append(substr)
                remaining_text = remaining_text[len(substr):]
            else:
                result.append(msg_chunk)
                remaining_text = remaining_text[len(msg_chunk):]
        
        return result