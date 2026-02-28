
from openai import OpenAI

llm_cfg = {
    #qwen3-235b-a22b-instruct-2507
    # Use your own model service compatible with OpenAI API by vLLM/SGLang:
    #'model': 'qwen3-235b-a22b-instruct-2507',
    'model':'deepseek-v3.2',
    #'model':'qwen3-coder-480b-a35b-instruct',
    #'model':'claude_sonnet4',
    #'api_key': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoic2Z0X2RhdGFfZ2VuZXJhdGlvbiJ9.VtDrSb_71ft3cJMjBw0H6lsUfRLrrOm-wKiZBreOwxg',
    "api_key":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoibGxtLXNmdC1ldmFsdWF0aW9uIn0.Tzapgz5p2X_fpKsf02hpAPFxuvy9ALmSoDES5sj3Tvk",
    "base_url":"https://llm-chat-api.alibaba-inc.com/openai",

    'generate_cfg': {
        # When using vLLM/SGLang OAI API, pass the parameter of whether to enable thinking mode in this way
        'max_input_tokens': 200000,
        "temperature": 0.5,
        "top_p": 0.9,
            'extra_body': {
            "app": "text_creation",
            "quota_id": "90e2fbc6-aa97-4baf-957d-9c4e7cc56d18",
            "user_id": '121536',
            "access_key": 'a08af2e29e177f838d270a71be1a1a45',
            },

    }
}

prompt = """你是一个牙科诊所的销售， 以下是牙科诊所的参考话术。用户正在通过电话向你咨询问题， 请回复用户的问题，注意不要啰嗦重点是吸引用户。"""
class ChatAgent:

    def __init__(self, hos_name="未知",user_info="未知", hos_info="未知"):
        self.history = [] 

        #self.base = "https://llm-chat-api.alibaba-inc.com/openai"
        self.base = "https://dashscope.aliyuncs.com/compatible-mode/v1"
        #base = "http://33.41.0.138:9000/v1"
        #self.model = '/root/ckpt'
        self.model = 'qwen3-235b-a22b-instruct-2507'
        #self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoic2Z0X2RhdGFfZ2VuZXJhdGlvbiJ9.VtDrSb_71ft3cJMjBw0H6lsUfRLrrOm-wKiZBreOwxg'
        self.token = 'sk-a48f248a97b441f49413199446bb8fbf'
        #token = "None"
        
       
        self.system_prompt = self.get_sys().format(hos_name=hos_name,user_info=user_info,hos_info=hos_info)
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
        self.client = OpenAI(api_key=llm_cfg['api_key'], base_url=llm_cfg['base_url'])
        response = self.client.chat.completions.create(model=llm_cfg['model'], messages=messages, max_tokens=2048, extra_body=llm_cfg['generate_cfg']['extra_body'])
        return response.choices[0].message.content