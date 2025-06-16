# import asyncio
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os

def scrape_data(driver):

    driver.get("https://esd.wa.gov/employer-requirements/layoffs-and-employee-notifications/worker-adjustment-and-retraining-notification-warn-layoff-and-closure-database")
    time.sleep(5)
    data = []
    
    # Find the table inside the div
    table = driver.find_element(By.TAG_NAME, "table")
    rows = table.find_elements(By.TAG_NAME, "tr")

    # Extract header
    headers = [th.text.strip() for th in rows[0].find_elements(By.TAG_NAME, "th")]

    # Extract data rows
    for row in rows[1:]:
        cells = row.find_elements(By.TAG_NAME, "td")
        if cells:
            row_data = [cell.text.strip() for cell in cells]
            data.append(row_data)

    # Example: print or return the data
    print(headers)
    for row in data:
        print(row)

    return data

if __name__ == "__main__":
    kernel = get_kernel()
    driver = create_browser()
    scrape_data(driver)