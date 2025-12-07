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
    E2E-тест: Открытие карточки задачи (форма редактирования) и проверка содержимого.
    Сценарий:
    1. Открыть страницу с доской (уже есть задачи).
    2. Прокрутить до низа — чтобы загрузились все задачи (lazy load).
    3. Найти задачу по заголовку и кликнуть на неё → открывается форма редактирования.
    4. Прочитать все поля из формы: заголовок, описание, проект, приоритет, исполнитель.
    5. Сравнить прочитанные данные с ожидаемыми.
    6. Прикрепить скриншоты и HTML-дамп для диагностики.
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

    # 🔹 ШАГ 4: НАЙТИ И КЛИКНУТЬ НА ЗАДАЧУ
    logger.info(f"ШАГ 4: Ищем задачу с заголовком: '{task_title}'")
    try:
        task_locator = (
            By.XPATH,
            f"//div[contains(@class, 'MuiPaper-root')]//h6[contains(@class, 'MuiTypography-subtitle1') and normalize-space(text()) = '{task_title}']"
        )
        task_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(task_locator))
        logger.info(f"✅ Задача '{task_title}' найдена и кликабельна")
    except Exception as e:
        logger.error(f"❌ Задача '{task_title}' НЕ найдена!")
        allure.attach(driver.page_source, name="HTML после прокрутки", attachment_type=allure.attachment_type.TEXT)
        driver.save_screenshot(f"screenshots/{task_title.replace(' ', '_')}_task_not_found.png")
        allure.attach.file(f"screenshots/{task_title.replace(' ', '_')}_task_not_found.png", name="Задача не найдена", attachment_type=allure.attachment_type.PNG)
        raise

    # Плавно прокручиваем к элементу
    logger.info("ШАГ 5: Прокручиваем к задаче и кликаем")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", task_element)
    time.sleep(0.3)
    task_element.click()
    logger.info("✅ Клик по задаче выполнен")

    # ✅ Скриншот после клика
    screenshot_after_click = f"screenshots/{task_title.replace(' ', '_')}_after_click.png"
    driver.save_screenshot(screenshot_after_click)
    allure.attach.file(screenshot_after_click, name="После клика на задачу", attachment_type=allure.attachment_type.PNG)
    logger.info(f"Скриншот сохранён: {screenshot_after_click}")

    # 🔹 ШАГ 6: ОЖИДАЕМ ФОРМЫ — С ДИАГНОСТИКОЙ
    logger.info("ШАГ 6: Ожидаем появления формы редактирования (ищем <h5>Редактирование задачи</h5>)")
    try:
        # Ждём появление <h5> с нужным текстом
        h5_locator = (By.XPATH, "//h5[normalize-space(.) = 'Редактирование задачи']")
        h5_element = WebDriverWait(driver, 15).until(EC.presence_of_element_located(h5_locator))
        logger.info("✅ <h5>Редактирование задачи</h5> найден в DOM")
        
        # Дополнительно: Выводим его текст для проверки
        h5_text = h5_element.text.strip()
        logger.info(f"   Текст <h5>: '{h5_text}'")
        allure.attach(f"Текст <h5>: '{h5_text}'", "Текст элемента h5", attachment_type=allure.attachment_type.TEXT)

    except Exception as e:
        logger.error("❌ Форма редактирования НЕ появилась в течение 15 секунд!")
        allure.attach(driver.page_source, name="HTML после клика (форма не появилась)", attachment_type=allure.attachment_type.TEXT)
        driver.save_screenshot(f"screenshots/{task_title.replace(' ', '_')}_form_not_found.png")
        allure.attach.file(f"screenshots/{task_title.replace(' ', '_')}_form_not_found.png", name="Форма не найдена", attachment_type=allure.attachment_type.PNG)
        raise

    # 🔹 ШАГ 7: ЖДЁМ НЕСКОЛЬКО СЕКУНД — ПОТОМУ ЧТО ПОЛЯ МОГУТ ЗАГРУЖАТЬСЯ С ЗАДЕРЖКОЙ
    logger.info("ШАГ 7: Ждём 0.5 секунды на загрузку полей формы")
    time.sleep(0.5)

    # 🔹 ШАГ 8: ЧИТАЕМ ПОЛЯ
    logger.info("ШАГ 8: Чтение данных из формы")
    try:
        title = task_page.wait.until(EC.presence_of_element_located(task_page.TASK_TITLE_INPUT_VALUE)).get_attribute("value").strip()
        description = task_page.wait.until(EC.presence_of_element_located(task_page.TASK_DESCRIPTION_TEXTAREA)).text.strip()
        project = task_page.wait.until(EC.presence_of_element_located(task_page.TASK_PROJECT_SELECT)).text.strip()
        priority = task_page.wait.until(EC.presence_of_element_located(task_page.TASK_PRIORITY_SELECT)).text.strip()
        assignee = task_page.wait.until(EC.presence_of_element_located(task_page.TASK_ASSIGNEE_SELECT)).text.strip()

        logger.info(f"   Заголовок: '{title}'")
        logger.info(f"   Описание: '{description}'")
        logger.info(f"   Проект: '{project}'")
        logger.info(f"   Приоритет: '{priority}'")
        logger.info(f"   Исполнитель: '{assignee}'")

    except Exception as e:
        logger.error(f"❌ Не удалось прочитать поля формы: {str(e)}")
        allure.attach(driver.page_source, name="HTML после загрузки формы", attachment_type=allure.attachment_type.TEXT)
        driver.save_screenshot(f"screenshots/{task_title.replace(' ', '_')}_form_fields_error.png")
        allure.attach.file(f"screenshots/{task_title.replace(' ', '_')}_form_fields_error.png", name="Поля формы не прочитаны", attachment_type=allure.attachment_type.PNG)
        raise

    # ✅ Скриншот после чтения
    screenshot_card = f"screenshots/{task_title.replace(' ', '_')}_form_read.png"
    driver.save_screenshot(screenshot_card)
    allure.attach.file(screenshot_card, name="Данные формы прочитаны", attachment_type=allure.attachment_type.PNG)

    # 🔹 ШАГ 9: ПРОВЕРКА ДАННЫХ
    logger.info("ШАГ 9: Проверка данных")
    with allure.step("Проверка заголовка задачи"):
        assert title == task_title, f"Ожидался заголовок: '{task_title}', получено: '{title}'"
    with allure.step("Проверка описания задачи"):
        assert description == expected_description, f"Ожидалось описание: '{expected_description}', получено: '{description}'"
    with allure.step("Проверка проекта"):
        assert project == expected_project, f"Ожидался проект: '{expected_project}', получено: '{project}'"
    with allure.step("Проверка приоритета"):
        assert priority == expected_priority, f"Ожидался приоритет: '{expected_priority}', получено: '{priority}'"
    with allure.step("Проверка исполнителя"):
        assert assignee == expected_assignee, f"Ожидался исполнитель: '{expected_assignee}', получено: '{assignee}'"

    logger.info("✅ ВСЁ СОВПАЛО — ТЕСТ ПРОШЁЛ!")

    allure.attach("Тест пройден: все поля формы совпали (без статуса)", "Результат", attachment_type=allure.attachment_type.TEXT)

    