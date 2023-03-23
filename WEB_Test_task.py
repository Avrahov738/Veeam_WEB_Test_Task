#Instruction to run: python3 WEB_Test_task.py --expected_vacancies_count 9
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import argparse

def assert_vacancies_count(expected_vacancies_count: int) -> None:
    browser = webdriver.Chrome()
    browser.maximize_window()
    browser.get("https://cz.careers.veeam.com/vacancies")
    delay = 5  # seconds
    try:
        WebDriverWait(browser, delay).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.form-group .select .dropdown')))
    except TimeoutException:
        raise ValueError("Loading took too much time!")

    try:
        browser.find_element(By.ID, 'cookiescript_accept').click()
        browser.find_element(By.ID, 'cookiescript_close').click()
        browser.implicitly_wait(2)
    except:
        print('No cookies modal window.')

    filter_selectors = browser.find_elements(by=By.CLASS_NAME, value="form-group")
    dep_selector = filter_selectors[1]
    lang_selector = filter_selectors[2]

    # department selector clicks
    dep_button = dep_selector.find_element(By.CSS_SELECTOR, value=".select .dropdown #sl")
    dep_button.click()

    rd_button = dep_selector.find_elements(By.CSS_SELECTOR, value=".select .dropdown .dropdown-menu .dropdown-item")[2]
    rd_button.click()

    browser.implicitly_wait(2)

    # language selector clicks
    lang_button = lang_selector.find_element(By.CSS_SELECTOR, value=".dropdown #sl")
    lang_button.click()

    eng_lang_button = lang_selector.find_element(By.CSS_SELECTOR,
                                                 value=".dropdown .dropdown-menu .custom-checkbox .custom-control-input")
    eng_lang_button.click()
    lang_button.click()  # close language dropdown

    # get vacancies count
    vacancies = browser.find_elements(By.CLASS_NAME, 'card')
    vacancies_count = len(vacancies)

    print("Actual vacancies count = ", vacancies_count)
    assert vacancies_count == expected_vacancies_count, "Invalid actual vacancies count"
    print("Successfully finished test")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--expected_vacancies_count',
                        dest='expected_vacancies_count',
                        type=int,
                        help='Expected number of vacancies under R&D department',
                        required=True)
    args = parser.parse_args()
    assert_vacancies_count(expected_vacancies_count=args.expected_vacancies_count)
