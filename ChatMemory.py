class ChatMemory:
    def __init__(self, SystemPrompt: str, window_size: int=7): # 6+1 
        self.window_size=window_size
        self.DictMemory=[]
        self.DictMemory.append({"role": "system", "content": SystemPrompt})

    def BotResp(self,bot_response):
        self.DictMemory.append({"role": "assistant", "content": bot_response})
        if len(self.DictMemory)>self.window_size:
            self.DictMemory.pop(2)
            self.DictMemory.pop(1)

    def UserInp(self, user_input):
        self.DictMemory.append({"role": "user", "content": user_input})


    def get_context(self):
        return self.DictMemory 