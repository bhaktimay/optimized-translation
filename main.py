from flask import Flask, request, jsonify
import argostranslate.package
import argostranslate.translate

app = Flask(__name__)

@app.route("/translate", methods=["POST"])
def translate_text():
    data = request.json
    from_lang = data.get("from")
    to_lang = data.get("to")
    text = data.get("text")

    installed_languages = argostranslate.translate.get_installed_languages()
    from_lang_obj = next((lang for lang in installed_languages if lang.code == from_lang), None)
    to_lang_obj = next((lang for lang in installed_languages if lang.code == to_lang), None)

    if not from_lang_obj or not to_lang_obj:
        return jsonify({"error": "Language not installed"}), 400

    translation = from_lang_obj.get_translation(to_lang_obj)
    return jsonify({"translatedText": translation.translate(text)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
