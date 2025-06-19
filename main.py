from flask import Flask, request, jsonify
import argostranslate.package
import argostranslate.translate

# Load installed languages
installed_languages = argostranslate.translate.get_installed_languages()

app = Flask(__name__)

@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    source_lang_code = data.get("from")
    target_lang_code = data.get("to")
    text = data.get("text")

    if not all([source_lang_code, target_lang_code, text]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        from_lang = next(lang for lang in installed_languages if lang.code == source_lang_code)
        to_lang = next(lang for lang in installed_languages if lang.code == target_lang_code)
        translation = from_lang.get_translation(to_lang)
        translated_text = translation.translate(text)
        return jsonify({"translated": translated_text})
    except StopIteration:
        return jsonify({"error": "Language not installed"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
