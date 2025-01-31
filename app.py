from flask import Flask, render_template, request, redirect, url_for, flash
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

API_URL = 'https://order.drcash.sh/v1/order'  # Замените на реальный URL API


API_TOKEN = 'RLPUUOQAMIKSAB2PSGUECA'

last_submission_time = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    global last_submission_time

    if last_submission_time and datetime.now() - last_submission_time < timedelta(minutes=1):
        return render_template('sorry.html')

    # Получаем данные из формы
    name = request.form.get('name')
    phone = request.form.get('phone')

    # Подготовка тела запроса
    payload = {
        'stream_code': 'vv4uf',
        'client': {
            'phone': phone,
            'name': name
        }
    }

    # Заголовки запроса
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_TOKEN}'
    }

    # Отправка POST-запроса к стороннему сервису
    try:
        response = requests.post(API_URL, headers=headers, json=payload)

        # Проверка успешности запроса
        if response.status_code == 200:
            last_submission_time = datetime.now()  # Обновляем время последней отправки
            return redirect(url_for('thanks'))
        else:
            # Логируем ошибку, если статус код не 200
            print(f"Ошибка: {response.status_code}, Ответ: {response.text}")
            return "Ошибка при отправке данных", 500
    except requests.exceptions.RequestException as e:
        # Логируем исключение, если запрос не удался
        print(f"Ошибка при отправке запроса: {e}")
        return "Ошибка при отправке данных", 500

@app.route('/thanks')
def thanks():
    return render_template('thanks.html')

if __name__ == '__main__':
    app.run(debug=True)