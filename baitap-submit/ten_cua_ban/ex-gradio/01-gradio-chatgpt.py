import gradio as gr
from openai import OpenAI

# https://platform.openai.com/api-keys
client = OpenAI(
    api_key='sk-proj-XXXXX',
)


def chat_logic(message, chat_history):
    '''
    message: Tin nhắn của user (string)
    chat_history: Lịch sử chat (list gồm nhiều tin nhắn, mỗi tin nhắn là một list [message, bot_message])
    '''

    # Chuyển lịch sử chat thành dạng OpenAI có thể đọc
    messages = []
    for user_message, bot_message in chat_history:
        messages.append({"role": "user", "content": user_message})
        messages.append({"role": "assistant", "content": bot_message})

    # Thêm tin nhắn mới của user
    messages.append({"role": "user", "content": message})

    # Thêm tin nhắn "Đang chờ..." vào lịch sử chat và hiển thị
    chat_history.append([message, "Waiting..."])
    yield "", chat_history

    # Gửi lịch sử chat lên OpenAI để nhận tin nhắn trả lời
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="gpt-4o-mini",
        stream=True
    )

    chat_history[-1][1] = ""
    # Hiển thị tin nhắn trả lời từ OpenAI, stream dần dần thay vì chờ tất cả kết quả mới trả lời
    for chunk in chat_completion:
        delta = chunk.choices[0].delta.content or ""

        # Update tin nhắn cuối cùng trong lịch sử chat
        chat_history[-1][1] += delta
        # Hàm `yield` trả về kết quả dạng generator, giúp Gradio hiển thị kết quả dần dần
        yield "", chat_history

    return "", chat_history


with gr.Blocks() as demo:
    gr.Markdown("# Chatbot bằng ChatGPT")
    message = gr.Textbox(label="Nhập tin nhắn của bạn:")
    chatbot = gr.Chatbot(label="Chat Bot siêu thông minh", height=600)
    message.submit(chat_logic, [message, chatbot], [message, chatbot])

demo.launch()