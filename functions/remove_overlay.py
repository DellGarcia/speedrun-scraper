from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def remove_overlay_for(driver, element_id):
    try:
        overlay_el = driver.find_element(By.ID, element_id)
        driver.execute_script("""var element = arguments[0]; 
                                    element.parentNode.removeChild(element);""", overlay_el)
    except NoSuchElementException:
        pass
