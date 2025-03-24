import gradio as gr

# Hàm này giữ nguyên


def greet(name: str) -> str:
    return f"Hello {name}!"


# with gr.Blocks() as demo:
#     # Tự declare textbox đầu vào và textbox đầu ra
#     with gr.Row():
#         name_input = gr.Textbox(label="Enter your name:")
#         greeting_output = gr.Textbox(label="Greeting")

#     # Tạo button, gọi hàm Greet khi click vào button đó
#     greet_button = gr.Button("Greet")
#     greet_button.click(greet, inputs=name_input, outputs=greeting_output)

# demo.launch(share=True)

with gr.Blocks() as demo:
    gr.Markdown("# App Hello World bằng Block")
    # Tự declare textbox đầu vào và textbox đầu ra
    with gr.Row():
        name_input = gr.Textbox(label="Enter your name:")
    with gr.Row():
        greeting_output = gr.Textbox(label="Greeting")

    name_input.change(greet, name_input, greeting_output)

demo.launch(share=True)