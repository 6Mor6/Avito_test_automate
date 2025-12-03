
import time
import allure
import os
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.pages.task_page import TaskPage

# Настройка логгера
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@allure.title("Открытие карточки задачи через форму редактирования и проверка данных")
@allure.description("Проверка, что при клике на задачу открывается форма редактирования с корректными данными: заголовок, описание, проект, приоритет, исполнитель.")
@allure.severity(allure.severity_level.CRITICAL)
def test_open_task_card(driver):
    """
    E2E-тест:
    1. Открыть страницу с доской (уже есть задачи).
    2. Прокрутить до низа — чтобы загрузились все задачи (lazy load).
    """

    task_title = 'E2E Test last'
    expected_description = 'Тетсовое описание'
    expected_project = 'Рефакторинг API'
    expected_priority = 'Low'
    expected_assignee = 'Максим Орлов'

    task_page = TaskPage(driver)

    # 🔹 ШАГ 1: Открываем страницу
    logger.info("ШАГ 1: Открываем страницу")
    task_page.open()

    # ✅ Скриншот до прокрутки
    screenshot_before_scroll = f"screenshots/{task_title.replace(' ', '_')}_before_scroll.png"
    os.makedirs("screenshots", exist_ok=True)
    driver.save_screenshot(screenshot_before_scroll)
    allure.attach.file(screenshot_before_scroll, name="Доска до прокрутки", attachment_type=allure.attachment_type.PNG)
    logger.info(f"Скриншот сохранён: {screenshot_before_scroll}")

    # 🔹 ШАГ 2: ПРОКРУТКА — ОБЯЗАТЕЛЬНА! (lazy load)
    logger.info("ШАГ 2: Прокручиваем страницу вниз (lazy load)")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)

    # ✅ Скриншот после прокрутки
    screenshot_after_scroll = f"screenshots/{task_title.replace(' ', '_')}_after_scroll.png"
    driver.save_screenshot(screenshot_after_scroll)
    allure.attach.file(screenshot_after_scroll, name="Доска после прокрутки", attachment_type=allure.attachment_type.PNG)
    logger.info(f"Скриншот сохранён: {screenshot_after_scroll}")

    # 🔹 ШАГ 3: УБЕДИМСЯ, ЧТО ЗАДАЧИ ЗАГРУЖЕНЫ
    logger.info("ШАГ 3: Ожидаем появления задач на доске")
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'MuiPaper-root')]//h6[contains(@class, 'MuiTypography-subtitle1')]"))
        )
        logger.info("✅ Задачи найдены на доске")
    except Exception as e:
        logger.error("❌ Задачи НЕ найдены на доске!")
        allure.attach(driver.page_source, name="HTML до прокрутки", attachment_type=allure.attachment_type.TEXT)
        raise