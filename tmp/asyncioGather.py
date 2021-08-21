async def fetch_messages(self,data):
    messages = self.get_messages()
    print(messages)
    result = asyncio.gather(messages)
    print(result) # this 
    await result
    print(result) # this 
    content = {
        'command': 'fetch_messages',
        'messages' : self.messages_to_json(messages,data)
    }
    print(content)
    await self.send_message(content)
