import imp
from select import select
from flask import Flask, render_template, request, jsonify
from abbreviation_maker import make_abbreviation
from name_generater import generate_name
from consonant_changer import change_consonant
from seed_word import seedword
from vowel_changer import change_vowel

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('generate_name.html')


@app.route('/gn')
def test():
    return render_template('generate_name.html')


@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    selected_sectors = data.get('sector', [])
    selected_brandValues = data.get('brandValue', [])
    selected_trends = data.get('trend', [])
    selected_seedWords = data.get('seedWord', [])
    selected_targets = data.get('target', [])
    selected_languageStyles = data.get('languageStyle', [])
    selected_levels = data.get('level', [])

    result = f"업종-{' '.join(selected_sectors)}, \
        브랜드가치-{' '.join(selected_brandValues)}, \
        트렌드-{' '.join(selected_trends)}, \
        시드단어-{' '.join(selected_seedWords)}, \
        타겟-{' '.join(selected_targets)}, \
        언어스타일-{' '.join(selected_languageStyles)}, \
        레벨-{' '.join(selected_levels)}"

    response = generate_name(result)

    return jsonify({'generated_name': response}), 200


@app.route('/cc')
def form():
    return render_template('transform_name.html')


@app.route('/change_consonant', methods=['POST'])
def handle_change_consonant():
    data = request.get_json()
    word = data.get('word')

    if not word:
        return jsonify({'error': '단어를 입력하세요'}), 400

    # 변경된 단어 가져오기
    changed_word = change_consonant(word)

    return jsonify({'changed_word': changed_word}), 200


@app.route('/change_vowel', methods=['POST'])
def handle_change_vowel():
    data = request.get_json()
    word = data.get('word')

    if not word:
        return jsonify({'error': '단어를 입력하세요'}), 400

    changed_word = change_vowel(word)

    return jsonify({'changed_word': changed_word}), 200


@app.route('/make_abbreviation', methods=['POST'])
def handle_make_abbreviation():
    data = request.get_json()
    word = data.get('word')

    if not word:
        return jsonify({'error': '단어를 입력하세요'}), 400

    changed_word = make_abbreviation(word)

    return jsonify({'changed_word': changed_word}), 200


@app.route('/seedword', methods=['POST'])
def handle_seedword():
    data = request.get_json()
    seed_word = data.get('word')

    if not seed_word:
        return jsonify({'error': '단어를 입력하세요'}), 400

    changed_word = seedword(seed_word)

    return jsonify({'changed_word': changed_word}), 200


if __name__ == '__main__':
    # app.run('127.0.0.1', 5000, debug=True)
    app.run(debug=True)
