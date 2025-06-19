from flask import Flask, request, jsonify
import argostranslate.package
import argostranslate.translate

# Update model file name
argostranslate.package.install_from_path("translate-en_hi-1_1.argosmodel")
installed_languages = argostranslate.translate.get_installed_languages()

app = Flask(__name__)

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()

    from_lang = data.get("from", "en")
    to_lang = data.get("to", "hi")
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    from_lang_obj = next((lang for lang in installed_languages if lang.code == from_lang), None)
    to_lang_obj = next((lang for lang in installed_languages if lang.code == to_lang), None)

    if not from_lang_obj or not to_lang_obj:
        return jsonify({"error": "Language not installed"}), 400

    translated_text = from_lang_obj.get_translation(to_lang_obj).translate(text)
    return jsonify({"translated_text": translated_text})
