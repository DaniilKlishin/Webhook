import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time

import os
import telebot

BOT_TOKEN = os.environ.get("7788463847:AAHOpEeQofagypCD61gUtwrnla9AJXkJs7w")
CHAT_ID = os.environ.get("1097060498")

bot = telebot.TeleBot(BOT_TOKEN)
test_results = {}


@pytest.fixture(scope="session", autouse=True)
def session_setup(request):
    """Выполняется перед началом и после окончания ВСЕЙ тестовой сессии."""
    global test_results
    test_results['total'] = 0
    test_results['passed'] = 0
    test_results['failed'] = 0
    test_results['skipped'] = 0

    def session_finish():
        """Отправляет сообщение в Telegram после завершения сессии."""
        message = f"Тесты Selenium завершены!\n" \
                  f"Всего тестов: {test_results['total']}\n" \
                  f"Пройдено: {test_results['passed']}\n" \
                  f"Провалено: {test_results['failed']}\n" \
                  f"Пропущено: {test_results['skipped']}"

        try:
            bot.send_message(CHAT_ID, message)
        except Exception as e:
            print(f"Ошибка при отправке сообщения в Telegram: {e}")
    request.addfinalizer(session_finish)
    bot.send_message(CHAT_ID, "Начинаю запуск тестов Selenium...")


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    driver.get("http://127.0.0.1:2202/")
    yield driver
    driver.quit()

@pytest.mark.parametrize("num1, num2, operation, expected", [(10, 2, "-", 8.0),(5, 0, "/", "Ошибка: Деление на ноль"),])

def test_calculator_operations(driver, num1, num2, operation, expected):
    num1_field = driver.find_element(By.NAME, "num1")
    num2_field = driver.find_element(By.NAME, "num2")
    operation_select = Select(driver.find_element(By.NAME, "operation"))
    submit_button = driver.find_element(By.TAG_NAME, "button")

    num1_field.clear()
    num1_field.send_keys(num1)
    num2_field.clear()
    num2_field.send_keys(num2)
    operation_select.select_by_value(operation)
    submit_button.click()

    time.sleep(1)

    result_text = driver.find_element(By.TAG_NAME, "h3").text
    assert f"Результат: {expected}" in result_text
    try:
        assert f"Результат: {expected}" in result_text
        test_results['passed'] += 1  # Увеличиваем счетчик пройденных тестов
    except AssertionError:
        test_results['failed'] += 1  # Увеличиваем счетчик упавших тестов
        print(f"Тест {request.node.name} провален: ожидалось '{expected}', получено '{result_text}'") # Вывод информации о провале
        raise  # Перебрасываем исключение, чтобы pytest зарегистрировал провал

    except Exception as e:
        test_results['failed'] += 1 # Увеличиваем счетчик упавших тестов
        print(f"Тест {request.node.name} завершился с ошибкой: {e}")
        raise