import argostranslate.package
import argostranslate.translate

# Automatically download & install English to Hindi model if not present
import os
import urllib.request

model_url = "https://www.argosopentech.com/argospm/index.json"
pkg_url = "https://www.argosopentech.com/argospm/packages/en_hi.argosmodel"
pkg_path = "en_hi.argosmodel"

if not os.path.exists(pkg_path):
    urllib.request.urlretrieve(pkg_url, pkg_path)
    package = argostranslate.package.install_from_path(pkg_path)

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/translate", methods=["POST"])
def translate_text():
    data = request.get_json()
    from_code = data.get("from")
    to_code = data.get("to")
    text = data.get("text")

    installed_languages = argostranslate.translate.get_installed_languages()
    from_lang = next((lang for lang in installed_languages if lang.code == from_code), None)
    to_lang = next((lang for lang in installed_languages if lang.code == to_code), None)

    if from_lang and to_lang:
        translation = from_lang.get_translation(to_lang)
        translated_text = translation.translate(text)
        return jsonify({"translated": translated_text})
    else:
        return jsonify({"error": "Language not installed"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
