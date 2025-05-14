import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helpers import retrieve_phone_code


class UrbanRoutesPage:
    FROM_LOCATOR = (By.ID, 'from')
    TO_LOCATOR = (By.ID, 'to')
    SELECT_SUPPORTIVE_PLAN = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[1]/div[5]/div[2]')
    SELECTED_TARIFF = (By.XPATH, '//div[contains(@class,"selected")]//div[contains(text(), "Supportive")]')
    CALL_TAXI_BUTTON = (By.XPATH, '//button[contains(text(), "Call a taxi")]')

    CLICK_PHONE_NUMBER = (By.XPATH, '//div[@class="np-text"]')
    ENTER_PHONE_NUMBER = (By.XPATH, '//*[@id="phone"]')
    CLICK_NEXT = (By.XPATH, '//button[@type="submit" and text()="Next"]')
    ENTER_SMS_CODE = (By.XPATH, '//*[@id="code"]')
    CLICK_CONFIRM = (By.XPATH, '//button[@type="submit" and text()="Confirm"]')

    CLICK_PAYMENT_METHOD = (By.XPATH, '//div[contains(@class, "pp-text") and text()="Payment method"]')
    CLICK_ADD_CARD = (By.XPATH, '//div[contains(@class, "pp-title") and text()="Add card"]')
    ENTER_CARD_NUMBER = (By.XPATH, '//input[@type="text" and @id="number" and @placeholder="1234 0000 4321"]')
    ENTER_CARD_CODE = (By.XPATH, '//input[@type="text" and @id="code" and @placeholder="12"]')
    CLICK_LINK_BUTTON = (By.XPATH, '//button[@type="submit" and @class="button full" and text()="Link"]')

    COMMENT_INPUT = (By.XPATH, '//input[@class="input" and @placeholder="Get some whiskey"]')
    CLICK_ORDER_REQUIREMENT = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[1]/div[2]/img')
    CLICK_RIGHT_ARROW = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[2]/div/div[2]/div')
    BLANKET_ICON = (By.CLASS_NAME, "switch")
    BLANKET_SELECTED = (By.CLASS_NAME, "switch-input")
    ICE_CREAM_ICON = (By.XPATH, '(//div[@class="counter-plus"])[1]')
    ICE_CREAM_COUNTER = (By.XPATH, '(//div[@class="counter-value"])[1]')
    ORDER_TAXI_BUTTON = (By.XPATH, '//span[@class="smart-button-main" and text()="Enter the number and order"]')
    CAR_SEARCH_MODEL = (By.XPATH, '//*[@id="root"]/div/div[5]/div[2]/div[1]/div/div[1]')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def set_route(self, from_address, to_address):
        self.driver.find_element(*self.FROM_LOCATOR).send_keys(from_address)
        self.driver.find_element(*self.TO_LOCATOR).send_keys(to_address)
        self.click_call_taxi_button()

    def get_from(self):
        return self.driver.find_element(*self.FROM_LOCATOR).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.TO_LOCATOR).get_property('value')

    def click_call_taxi_button(self):
        WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located(self.CALL_TAXI_BUTTON))
        self.driver.find_element(*self.CALL_TAXI_BUTTON).click()

    def click_order_taxi_button(self):
        WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located(self.ORDER_TAXI_BUTTON))
        self.driver.find_element(*self.ORDER_TAXI_BUTTON).click()

    def select_supportive_plan(self):
        if not self.driver.find_elements(*self.SELECTED_TARIFF):
            self.driver.find_element(*self.SELECT_SUPPORTIVE_PLAN).click()

    def fill_phone_number(self, number):
        self.driver.find_element(*self.CLICK_PHONE_NUMBER).click()
        self.driver.find_element(*self.ENTER_PHONE_NUMBER).send_keys(number)
        self.driver.find_element(*self.CLICK_NEXT).click()
        code = retrieve_phone_code(self.driver)
        self.driver.find_element(*self.ENTER_SMS_CODE).send_keys(code)
        self.driver.find_element(*self.CLICK_CONFIRM).click()

    def fill_card(self, number, cvv):
        self.driver.find_element(*self.CLICK_PAYMENT_METHOD).click()
        self.driver.find_element(*self.CLICK_ADD_CARD).click()
        self.driver.find_element(*self.ENTER_CARD_NUMBER).send_keys(number)
        cvv_input = self.driver.find_element(*self.ENTER_CARD_CODE)
        cvv_input.send_keys(cvv)
        cvv_input.send_keys(Keys.TAB)
        time.sleep(1)
        self.driver.find_element(*self.CLICK_LINK_BUTTON).click()

    def comment_for_driver(self, message):
        self.driver.find_element(*self.COMMENT_INPUT).send_keys(message)


    def order_blanket_and_handkerchiefs(self):
        switches = self.driver.find_elements(*self.BLANKET_ICON)
        switches[0].click()
        self.is_blanket_and_handkerchiefs_selected()

    def order_ice_cream(self):
        self.driver.find_element(*self.ICE_CREAM_ICON).click()

    def verify_ice_cream_order(self):
        return self.driver.find_element(*self.ICE_CREAM_COUNTER).text


    def click_call_taxi(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.CALL_TAXI_BUTTON)
        ).click()

    def is_car_search_model_visible(self):
        try:
            popup_element = self.driver.find_element(By.XPATH, '//div[@class="order-header-title" and text()="Car search"]')
            return popup_element.is_displayed()
        except Exception:
            return False

    def get_selected_plan(self):
        return self.driver.find_element(*self.SELECT_SUPPORTIVE_PLAN).text

    def get_entered_phone_number(self):
        return self.driver.find_element(*self.ENTER_PHONE_NUMBER).get_attribute('value')

    def get_entered_card_number(self):
        return self.driver.find_element(*self.ENTER_CARD_NUMBER).get_attribute('value')

    def get_entered_card_code(self):
        return self.driver.find_element(*self.ENTER_CARD_CODE).get_attribute('value')

    def get_entered_driver_comment(self):
        return self.driver.find_element(*self.COMMENT_INPUT).get_attribute('value')

    def is_blanket_and_handkerchiefs_selected(self):
        switches = self.driver.find_elements(*self.BLANKET_SELECTED)
        return switches[0].get_property('checked')




