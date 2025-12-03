import time
import allure
import os
from tests.pages.task_page import TaskPage

@allure.title("Создание задачи через интерфейс")
@allure.description("Проверка, что пользователь может создать задачу и она появляется на доске после перезагрузки.")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_task(driver):
    task_page = TaskPage(driver)
    task_title = 'E2E Test last 123'
    description = 'Тетсовое описание'
    project = 'Рефакторинг API'
    priority = 'Low'
    assignee = 'Максим Орлов'

    task_page.open()
    task_page.create_task(
        title=task_title,
        description=description,
        project=project,
        priority=priority,
        assignee=assignee
    )

    screenshot_before = f"screenshots/{task_title.replace(' ', '_')}_created.png"
    os.makedirs("screenshots", exist_ok=True)
    driver.save_screenshot(screenshot_before)
    allure.attach.file(screenshot_before, name="Задача создана", attachment_type=allure.attachment_type.PNG)

    task_page.open()

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(4)

    last_task = task_page.get_last_created_task_title()
    assert last_task == task_title, f"Ожидалось: '{task_title}', получено: '{last_task}'"

    screenshot_after = f"screenshots/{task_title.replace(' ', '_')}_after_reload_and_scroll.png"
    driver.save_screenshot(screenshot_after)
    allure.attach.file(screenshot_after, name="Последняя задача видна", attachment_type=allure.attachment_type.PNG)