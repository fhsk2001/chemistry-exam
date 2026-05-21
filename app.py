from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

# Периодична таблица за 8 клас
ELEMENTS = {
    'H': {'name': 'Водород', 'atomic_number': 1, 'mass': 1, 'color': '#FF6B6B'},
    'C': {'name': 'Въглерод', 'atomic_number': 6, 'mass': 12, 'color': '#4ECDC4'},
    'N': {'name': 'Азот', 'atomic_number': 7, 'mass': 14, 'color': '#45B7D1'},
    'O': {'name': 'Кислород', 'atomic_number': 8, 'mass': 16, 'color': '#FFA07A'},
    'Na': {'name': 'Натрий', 'atomic_number': 11, 'mass': 23, 'color': '#FFD93D'},
    'Mg': {'name': 'Магнезий', 'atomic_number': 12, 'mass': 24, 'color': '#6BCB77'},
    'Al': {'name': 'Алуминий', 'atomic_number': 13, 'mass': 27, 'color': '#C7CEEA'},
    'Si': {'name': 'Силиций', 'atomic_number': 14, 'mass': 28, 'color': '#B19CD9'},
    'S': {'name': 'Сяра', 'atomic_number': 16, 'mass': 32, 'color': '#FFFD38'},
    'Cl': {'name': 'Хлор', 'atomic_number': 17, 'mass': 35.5, 'color': '#90EE90'},
    'K': {'name': 'Калий', 'atomic_number': 19, 'mass': 39, 'color': '#FFB6C1'},
    'Ca': {'name': 'Калций', 'atomic_number': 20, 'mass': 40, 'color': '#DDA0DD'},
    'Fe': {'name': 'Желязо', 'atomic_number': 26, 'mass': 56, 'color': '#A9A9A9'},
    'Cu': {'name': 'Медь', 'atomic_number': 29, 'mass': 64, 'color': '#B87333'},
}

# Въпроси за изпит
QUESTIONS = [
    {
        'id': 1,
        'question': 'Какво е атомното число на кислорода?',
        'options': ['6', '7', '8', '9'],
        'correct': 2,
        'explanation': 'Кислородът (O) има атомно число 8'
    },
    {
        'id': 2,
        'question': 'Какъв е химичният символ на натрия?',
        'options': ['S', 'Na', 'N', 'Sn'],
        'correct': 1,
        'explanation': 'Натрият има химичен символ Na'
    },
    {
        'id': 3,
        'question': 'Водородът е...',
        'options': ['Метал', 'Неметал', 'Металоид', 'Благороден газ'],
        'correct': 1,
        'explanation': 'Водородът е неметал и образува газ при нормални условия'
    },
    {
        'id': 4,
        'question': 'Колко валентни електрона има въглеродът?',
        'options': ['2', '4', '6', '8'],
        'correct': 1,
        'explanation': 'Въглеродът има 4 валентни електрона'
    },
    {
        'id': 5,
        'question': 'Какъв е атомния номер на желязото?',
        'options': ['24', '25', '26', '27'],
        'correct': 2,
        'explanation': 'Желязото (Fe) има атомно число 26'
    },
    {
        'id': 6,
        'question': 'Кои елементи образуват вода?',
        'options': ['Кислород и азот', 'Водород и кислород', 'Водород и азот', 'Натрий и кислород'],
        'correct': 1,
        'explanation': 'Водата (H₂O) е образувана от водород и кислород'
    },
    {
        'id': 7,
        'question': 'Какво е молекулното тегло на CO₂?',
        'options': ['28', '32', '44', '48'],
        'correct': 2,
        'explanation': 'CO₂ = 12 + 16×2 = 44'
    },
    {
        'id': 8,
        'question': 'Хлорът е...',
        'options': ['Метал', 'Неметал', 'Газ при стайна температура', 'Б и В са верни'],
        'correct': 3,
        'explanation': 'Хлорът е неметал и газ при стайна температура (жълто-зелено окрасен)'
    },
    {
        'id': 9,
        'question': 'Какъв е периодът на магнезия в периодичната таблица?',
        'options': ['2', '3', '4', '5'],
        'correct': 1,
        'explanation': 'Магнезият е във втория период на периодичната таблица'
    },
    {
        'id': 10,
        'question': 'Мед има химичен символ...',
        'options': ['Co', 'Cu', 'Cd', 'Cn'],
        'correct': 1,
        'explanation': 'Медта има химичен символ Cu (от латински "cuprum")'
    },
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/elements', methods=['GET'])
def get_elements():
    return jsonify(ELEMENTS)

@app.route('/api/quiz', methods=['GET'])
def get_quiz():
    # Връща 5 произволни въпроса
    selected_questions = random.sample(QUESTIONS, min(5, len(QUESTIONS)))
    quiz_data = [{
        'id': q['id'],
        'question': q['question'],
        'options': q['options']
    } for q in selected_questions]
    return jsonify(quiz_data)

@app.route('/api/check-answer', methods=['POST'])
def check_answer():
    data = request.json
    question_id = data.get('question_id')
    user_answer = data.get('answer')
    
    question = next((q for q in QUESTIONS if q['id'] == question_id), None)
    
    if not question:
        return jsonify({'error': 'Question not found'}), 404
    
    is_correct = question['correct'] == user_answer
    return jsonify({
        'correct': is_correct,
        'explanation': question['explanation'],
        'correct_answer': question['correct']
    })

@app.route('/api/get-element', methods=['GET'])
def get_element():
    symbol = request.args.get('symbol', '').upper()
    element = ELEMENTS.get(symbol)
    
    if not element:
        return jsonify({'error': 'Element not found'}), 404
    
    return jsonify({
        'symbol': symbol,
        **element
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
