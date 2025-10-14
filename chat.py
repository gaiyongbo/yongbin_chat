
from openai import OpenAI

llm_cfg = {
    #qwen3-235b-a22b-instruct-2507
    # Use your own model service compatible with OpenAI API by vLLM/SGLang:
    'model': 'qwen3-235b-a22b-instruct-2507',
    #'model':'qwen3-coder-480b-a35b-instruct',
    #'model':'claude_sonnet4',
    'model_server': 'https://llm-chat-api.alibaba-inc.com/openai',  # api_base
    'api_key': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoic2Z0X2RhdGFfZ2VuZXJhdGlvbiJ9.VtDrSb_71ft3cJMjBw0H6lsUfRLrrOm-wKiZBreOwxg',

    'generate_cfg': {
        # When using vLLM/SGLang OAI API, pass the parameter of whether to enable thinking mode in this way
        'max_input_tokens': 200000,
        "temperature": 0.5,
        "top_p": 0.9,
            'extra_body': {
            "app": "text_creation",
            "quota_id": "c965474c-549c-4306-bf1f-265d0e4cb86b"
            },

    }
}

prompt = """你是一个牙科诊所的销售， 以下是牙科诊所的参考话术。用户正在通过电话向你咨询问题， 请回复用户的问题，注意不要啰嗦重点是吸引用户。"""
class ChatAgent:

    def __init__(self):
        self.history = [] 

        #self.base = "https://llm-chat-api.alibaba-inc.com/openai"
        self.base = "https://dashscope.aliyuncs.com/compatible-mode/v1"
        #base = "http://33.41.0.138:9000/v1"
        #self.model = '/root/ckpt'
        self.model = 'qwen3-235b-a22b-instruct-2507'
        #self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoic2Z0X2RhdGFfZ2VuZXJhdGlvbiJ9.VtDrSb_71ft3cJMjBw0H6lsUfRLrrOm-wKiZBreOwxg'
        self.token = 'sk-a48f248a97b441f49413199446bb8fbf'
        #token = "None"
        
       
        self.system_prompt = self.get_sys()
        self.history = [{'role':'system','content':self.system_prompt}]
        #self.history = []

    def chat(self, query):
        self.history.append({'role':'user','content':query}) 
        res =  self.call_llm(self.history)
        self.history.append({'role':'assistant','content':res})
        return res
    
    def reset(self):

        self.history = [{'role':'system','content':self.system_prompt}]

    def get_ref(self):

        with open('resource/get_phones.md') as f:
            line = f.read()
        
        return line
    
    def get_sys(self):
        with open('resource/sys_prompt.md') as f:
            line = f.read()
        
        return line


    def call_llm(self,messages):   
        self.client = OpenAI(api_key=self.token, base_url=self.base)
        response = self.client.chat.completions.create(model=self.model, messages=messages, max_tokens=512)

        self.client.completions.create()
        return response.choices[0].message.content