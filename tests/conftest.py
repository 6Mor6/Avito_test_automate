# tests/conftest.py

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service # класс управляет запуском chrome webdriver
from webdriver_manager.chrome import ChromeDriverManager # подбирает нужные драйверы для запуска
from selenium.webdriver.chrome.options import Options # позволяет настраивать поведение браузера перед запуском.


@pytest.fixture(scope='function') # обёртывает функцию и даёт доп. возможности

def driver():
    chrome_options = Options() # объект настройки браузера
    chrome_options.add_argument("--start-maximized") # открытие в полном формате
    chrome_options.add_argument('--disable-notifications') # отключение системы всплывающих окон
    chrome_options.add_argument("--no-sandbox") # Флаг для CI-сред, запуск без прав "сэндбокса"
    chrome_options.add_argument("--disable-dev-shm-usage") # Флаг перенаправления использования системной памяти. Для CI

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options) # единственный код который будет запускать браузер

    driver.implicitly_wait(10) # неявные ожидания, если не будет элемента, будет ждать в течение 10 сек

    yield driver # Возвращаем драйвер тесту

    driver.quit()





 