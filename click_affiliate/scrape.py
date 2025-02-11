
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

# from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager
# import subprocess


# def run_browser():
#     command = ['C:\Program Files\Google\Chrome\Application\chrome.exe', '--remote-debugging-port=1010', "--user-data-dir=C:\chrome\1010"]
#     subprocess.Popen(command)

# run_browser()

# chrome_options = Options()
# chrome_options.debugger_address = "127.0.0.1:1010"
# driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)
k = 0
driver.get("https://whop.com/")

while True:
    confirm = input("Did you log in this site(y/n)?")
    if confirm == 'y':
        break
for i in range(943):
    driver.get(f"https://whop.com/discover/c/trading/p/{i}/")
    
    sleep(1)
    for i in range(9):  # Adjust range as needed
        sleep(1)  # Allow page to load

        # Re-find all <a> elements on the page **after navigating back**
        a_tags = driver.find_elements(By.CSS_SELECTOR, 'a.fui-reset.flex.h-full.w-full.flex-col.gap-2.rounded-b-sm.px-2.pb-1.pt-2.outline-none.transition')

        if i >= len(a_tags):  # Prevent out-of-bounds error
            break  

        a_tag = a_tags[i]
        link = a_tag.get_attribute('href')
        print(f"{k}:  Navigating to: {link}")
        k += 1

        # Visit the link
        driver.get(link)
        sleep(1)

        # Optional: Click button inside the new page
        try:
            button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.fui-reset.fui-BaseButton.fui-Button.mx-auto.w-full')))
            button.click()
            print(button.text)
        except Exception as e:
            print("Button not found or not clickable:", e)

        # Go back to the main page
        driver.back()
        sleep(1)  # Allow page to reload

sleep(5)
driver.close()