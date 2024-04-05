from flask import Flask, request, jsonify
import os

from model.openai_model import OpenAIModel
from translator import PDFTranslator

app = Flask(__name__)

# 为上传的文件设置一个目录
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/translate', methods=['POST'])
def file_upload():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']

    if file.filename == '':
        return "No selected file", 400
    model_name = request.form.get('model_name')
    file_format = request.form.get('file_format')
    target_language = request.form.get('target_language')
    api_key = os.environ.get("OPENAI_API_KEY")
    print("OpenAI API Key:", api_key)
    model = OpenAIModel(model=model_name, api_key=api_key)
    translator = PDFTranslator(model)

    if file:
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        response = translator.response_translate_pdf(os.path.join(app.config['UPLOAD_FOLDER'], filename), file_format,
                                            target_language=target_language)
        return response, 200


if __name__ == '__main__':
    app.run(debug=True)
