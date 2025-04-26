import os
import time

# from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from linkedin_credentials import accounts


from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Initialize chrome driver

options = Options()
options.add_argument("--headless=new")  # Required for printToPDF
options.add_argument("--disable-gpu")
options.add_argument("--disable-gpu")
options.add_argument("--disable-webrtc")



# load_dotenv()
EMAIL = accounts.keys()
PASSWORD = accounts.values()


def login_linkedin(driver):
    try:
        login_form_ = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "form-toggle"))
        )
        login_form_.click()
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "session_key"))
        )
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "session_password"))
        )

        if EMAIL:
            email_field.send_keys(EMAIL)
        else:
            raise ValueError("WTF PUT THE EMAIL IN THE .env FILE BRUV.")

        if PASSWORD:
            password_field.send_keys(PASSWORD)
        else:
            raise ValueError("WTF PUT THE PASSWORD IN THE .env FILE BRUV.")

        password_field.send_keys(Keys.RETURN)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "global-nav__me"))
        )
        print("SUCESSS")
    except Exception as e:
        print(f"{e} happened trying again.")
        driver.quit()
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.chrome(options=options)
        login_linkedin(driver)

    finally:
        return driver



import os
import base64

def print_page(driver, domain, output_folder=r"C:\Users\nidal\OneDrive\Masaüstü\MyCode\Bocconi\Bocconi ai\Linkedin stuff\pdf_profiles"):
    # Create folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    driver.get(f"https://{domain}")
    
    WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.ID, "education"))
        )
    
    filename = domain.strip("/").split("/")[-1] + ".pdf"  # e.g., magzhanov.pdf
    filepath = os.path.join(output_folder, filename)

    pdf = driver.execute_cdp_cmd("Page.printToPDF", {
        "printBackground": True
    })

    with open(filepath, "wb") as f:
        f.write(base64.b64decode(pdf['data']))

    print(f"Saved PDF to {filepath}")
    return driver




import pandas as pd 
data = pd.read_csv(r"C:\Users\nidal\Downloads\linkedin_profiles_2000_2024_2.csv")

for domain in data.iloc[:5, 0]:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Register the CDP command for printing
    driver.command_executor._commands["send_command"] = (
        "POST",
        "/session/$sessionId/chromium/send_command"
    )
    try:
        domain = domain.strip().replace("https://", "").replace("http://", "")
        url = f"https://{domain}"
        print(f"Accessing: {url}")

        driver.get(url)
        driver.refresh()

        driver = login_linkedin(driver)
        driver = print_page(driver, domain)
    except Exception as e:
        print(f"Error processing {domain}: {e}")
    
    driver.quit()


# driver.quit()
