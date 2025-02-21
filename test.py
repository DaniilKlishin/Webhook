from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

def add(number_1, number_2):
    return number_1 + number_2

def subtract(number_1, number_2):
    return number_1 - number_2

def multiply(number_1, number_2):
    return number_1 * number_2

def divide(number_1, number_2):
    if number_2 == 0:
        return 'Ошибка: Деление на ноль'
    return number_1 / number_2

def degree(number_1, number_2):
    return number_1 ** number_2

def maximum(number_1, number_2):
    if number_1 > number_2:
        return number_1
    else:
        return number_2

def minimum(number_1, number_2):
    if number_1 < number_2:
        return number_1
    else:
        return number_2

@app.route('/', methods=['GET', 'POST'])
def calculator():
    result = None
    if request.method == 'POST':
        try:
            num1 = float(request.form['num1'])
            num2 = float(request.form['num2'])
            operation = request.form['operation']
            
            operations = {
                '+': add,
                '-': subtract,
                '*': multiply,
                '/': divide,
                '**': degree,
                'max': maximum,
                'min': minimum
            }
            
            if operation in operations:
                result = operations[operation](num1, num2)
            else:
                result = 'Ошибка: Неизвестная операция'
        except ValueError:
            result = 'Ошибка: Введите числа'
    
    return render_template('calculator.html', result=result)

if __name__ == '__main__':
    app.run(debug=True, port=2202, host='0.0.0.0')