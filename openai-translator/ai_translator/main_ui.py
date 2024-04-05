import gradio as gr
import os

from model.openai_model import OpenAIModel
from translator import PDFTranslator


def greet(pdf_file_path, target_language, model_name, file_format):
    api_key = os.environ.get("OPENAI_API_KEY")
    print("OpenAI API Key:", api_key)
    model = OpenAIModel(model=model_name, api_key=api_key)
    translator = PDFTranslator(model)
    response = translator.response_translate_pdf(pdf_file_path, file_format, target_language=target_language)
    return response


if __name__ == "__main__":
    demo = gr.Interface(
        fn=greet,
        inputs=[
            "file",
            gr.Dropdown(["中文", "日语"], label="目标语言"),
            gr.Dropdown(["gpt-3.5-turbo", "gpt-4-0613"], label="翻译模型"),
            gr.Dropdown(["markdown", "txt"], label="输出格式")
        ],
        outputs="text"
    )

    demo.launch()
