import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TaskPage:
    # 🔹 ЛОКАТОРЫ ДЛЯ СПИСКА ЗАДАЧ
    CREATE_TASK_BUTTON = (By.XPATH, "//button[normalize-space(text()) = 'Создать задачу']")
    TASK_TITLE_INPUT = (By.XPATH, "//input[@id = //label[normalize-space(text()) = 'Название']/@for]")
    TASK_DESCRIPTION_INPUT = (By.XPATH, "//textarea[@id = //label[normalize-space(text()) = 'Описание']/@for]")

    PROJECT_SELECT_BUTTON = (By.XPATH, "(//div[@class='MuiFormControl-root MuiFormControl-fullWidth css-17qa0m8'][.//label[normalize-space(text()) = 'Проект']])[1]//div[@role='combobox']")
    PRIORITY_SELECT_BUTTON = (By.XPATH, "(//div[@class='MuiFormControl-root MuiFormControl-fullWidth css-17qa0m8'][.//label[normalize-space(text()) = 'Приоритет']])[1]//div[@role='combobox']")
    ASSIGNEE_SELECT_BUTTON = (By.XPATH, "(//div[@class='MuiFormControl-root MuiFormControl-fullWidth css-17qa0m8'][.//label[normalize-space(text()) = 'Исполнитель']])[1]//div[@role='combobox']")

    CREATE_BUTTON_IN_FORM = (By.XPATH, "//div[@class='MuiBox-root css-yd8sa2']//button[normalize-space(text()) = 'Создать']")

    # ✅ ФИНАЛЬНЫЙ ЛОКАТОР ФОРМЫ
    EDIT_TASK_FORM_H5 = (By.XPATH, "//h5[normalize-space(.) = 'Редактирование задачи']")

    # ✅ ИСПРАВЛЕННЫЕ ЛОКАТОРЫ ПОЛЕЙ — ИСПОЛЬЗУЕМ //following::div
    TASK_TITLE_INPUT_VALUE = (By.XPATH, "//label[normalize-space(text()) = 'Название']//following::div[@class='MuiInputBase-root']//input[@type='text']")
    TASK_DESCRIPTION_TEXTAREA = (By.XPATH, "//label[normalize-space(text()) = 'Описание']//following::div[@class='MuiInputBase-root']//textarea")
    TASK_PROJECT_SELECT = (By.XPATH, "//label[normalize-space(text()) = 'Проект']//following::div[@role='combobox']")
    TASK_PRIORITY_SELECT = (By.XPATH, "//label[normalize-space(text()) = 'Приоритет']//following::div[@role='combobox']")
    TASK_ASSIGNEE_SELECT = (By.XPATH, "//label[normalize-space(text()) = 'Исполнитель']//following::div[@role='combobox']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get("https://avito-tech-internship-psi.vercel.app/")
        self.wait.until(EC.element_to_be_clickable(self.CREATE_TASK_BUTTON))
        return self

    def create_task(self, title, description=None, project=None, priority=None, assignee=None):
        create_btn = self.wait.until(EC.element_to_be_clickable(self.CREATE_TASK_BUTTON))
        create_btn.click()

        title_input = self.wait.until(EC.presence_of_element_located(self.TASK_TITLE_INPUT))
        title_input.clear()
        title_input.send_keys(title)

        if description:
            description_input = self.wait.until(EC.presence_of_element_located(self.TASK_DESCRIPTION_INPUT))
            description_input.clear()
            description_input.send_keys(description)

        if project:
            self.select_project(project)
        if priority:
            self.select_priority(priority)
        if assignee:
            self.select_assignee(assignee)

        create_btn_in_form = self.wait.until(EC.element_to_be_clickable(self.CREATE_BUTTON_IN_FORM))
        create_btn_in_form.click()

    def select_project(self, project_name):
        btn = self.wait.until(EC.element_to_be_clickable(self.PROJECT_SELECT_BUTTON))
        btn.click()
        option = self.wait.until(EC.element_to_be_clickable(self._get_option_locator(project_name)))
        option.click()
        self.wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "ul.MuiMenu-list")))

    def select_priority(self, priority):
        btn = self.wait.until(EC.element_to_be_clickable(self.PRIORITY_SELECT_BUTTON))
        btn.click()
        option = self.wait.until(EC.element_to_be_clickable(self._get_option_locator(priority)))
        option.click()
        self.wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "ul.MuiMenu-list")))

    def select_assignee(self, name):
        btn = self.wait.until(EC.element_to_be_clickable(self.ASSIGNEE_SELECT_BUTTON))
        btn.click()
        option = self.wait.until(EC.element_to_be_clickable(self._get_option_locator(name)))
        option.click()
        self.wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "ul.MuiMenu-list")))

    def _get_option_locator(self, text):
        return (By.XPATH, f"//li[normalize-space(text()) = '{text}']")

    def scroll_to_element(self, element):
        window_height = self.driver.execute_script("return window.innerHeight;")
        y_position = element.location["y"]
        new_scroll_position = max(y_position - window_height / 2, 0)
        self.driver.execute_script(f"window.scrollTo(0, {new_scroll_position});")
        time.sleep(0.3)

    def get_last_created_task_title(self):
        self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'MuiPaper-root')]//h6[contains(@class, 'MuiTypography-subtitle1')]"))
        )
        last_task_element = self.wait.until(
            EC.presence_of_element_located(self._get_last_task_title_locator())
        )
        self.scroll_to_element(last_task_element)
        return last_task_element.text.strip()

    def _get_last_task_title_locator(self):
        return (By.XPATH, "(//div[contains(@class, 'MuiPaper-root')]//h6[contains(@class, 'MuiTypography-subtitle1')])[last()]")

    # ✅ ФИНАЛЬНЫЙ МЕТОД — ОТКРЫТИЕ ФОРМЫ РЕДАКТИРОВАНИЯ
    def open_task_card(self, task_title):
        self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'MuiPaper-root')]//h6[contains(@class, 'MuiTypography-subtitle1')]"))
        )

        task_locator = (
            By.XPATH,
            f"//div[contains(@class, 'MuiPaper-root')]//h6[contains(@class, 'MuiTypography-subtitle1') and normalize-space(text()) = '{task_title}']"
        )
        task_element = self.wait.until(EC.element_to_be_clickable(task_locator))

        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", task_element)
        time.sleep(0.3)
        task_element.click()

        # Ждём появления формы
        self.wait.until(EC.presence_of_element_located(self.EDIT_TASK_FORM_H5))
        time.sleep(0.5)  # Даем время на загрузку полей

        # ✅ ЧИТАЕМ ПОЛЯ — ЖДЁМ ВИДИМОСТЬ + ЗАПОЛНЕННОСТЬ
        title_element = self.wait.until(EC.visibility_of_element_located(self.TASK_TITLE_INPUT_VALUE))
        self.wait.until(lambda d: title_element.get_attribute("value") != "")  # Ждём, пока значение не появится
        title = title_element.get_attribute("value").strip()

        description_element = self.wait.until(EC.visibility_of_element_located(self.TASK_DESCRIPTION_TEXTAREA))
        self.wait.until(lambda d: description_element.text.strip() != "")
        description = description_element.text.strip()

        project = self.wait.until(EC.visibility_of_element_located(self.TASK_PROJECT_SELECT)).text.strip()
        priority = self.wait.until(EC.visibility_of_element_located(self.TASK_PRIORITY_SELECT)).text.strip()
        assignee = self.wait.until(EC.visibility_of_element_located(self.TASK_ASSIGNEE_SELECT)).text.strip()

        return {
            "title": title,
            "description": description,
            "project": project,
            "priority": priority,
            "assignee": assignee
        }

