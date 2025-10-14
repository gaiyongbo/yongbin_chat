
import gradio as gr
from chat import ChatAgent
def main():


    with gr.Blocks() as demo:
        gr.Markdown("## 📊 Excel 分析助手")
        agent = gr.State(ChatAgent())
        chat_history = gr.State([])  # 用于存储每个用户的对话历史

        # 添加 state 组件来管理状态
  
        with gr.Row():
            chatbot = gr.Chatbot(label="对话记录")

        with gr.Row():
            question_input = gr.Textbox(label="请输入你的问题", placeholder="", lines=2)
            analyze_btn = gr.Button("发送")
            clear = gr.ClearButton(components=[chatbot])

        def clear_fn(agent):
            print(f"hist reset")
            agent.reset()
            return [],[]
            
        clear.click(fn = clear_fn,inputs=[agent], outputs=[chat_history,chatbot])



        ## 点击发送时，多轮对话 + 图表
        def handle_analyze(agent,user_input, chat_history):

                ret = agent.chat(user_input)
                new_chatbot_history = chat_history + [(user_input, ret)]

                for chat in agent.history:
                    print(f"{chat['role']}:\n")
                    print(f"{chat['content']}\n")
                
         
                return new_chatbot_history,new_chatbot_history

        
        analyze_btn.click(handle_analyze, inputs=[agent,question_input, chat_history], outputs=[chatbot, chat_history])
        demo.launch(server_name="0.0.0.0", server_port=50000)


if __name__ == "__main__":
    main()
    

