from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config


# Setting up Chrome Options(Headless mode)
options = Options()
options.headless = True
browser = webdriver.Chrome(options=options)

# Storing last price to avoid duplicate
last_price = None

# Price check interval in seconds
interval = 600

while True:
    # Opening the browser
    browser.get(
        "https://www.jumia.com.gh/?srsltid=AfmBOoq4xDGmgBb_d-Kd3cTNIQRf27Q938MHxVERyo5ykTm_IeFlX-up"
    )
    print("Site:", browser.title)

    # Product page
    browser.get(
        "https://www.jumia.com.gh/samsung-s24-ultra-galaxy-ai-256gb-rom-12gb-ram-50mp-rear12mp-front-5000mah-titanium-black-24-months-warranty-211932373.html"
    )

    # Time for site to load
    WebDriverWait(browser, 15).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "h1.-fs20.-pts.-pbxs, span.-b.-ubpt.-tal.-fs24.-prxs")))

    # extracting product title
    product_element = browser.find_element(
        By.CSS_SELECTOR, "h1.-fs20.-pts.-pbxs")
    product = product_element.text
    print("Product:", product)

    # extracting price element
    price_element = browser.find_element(
        By.CSS_SELECTOR, "span.-b.-ubpt.-tal.-fs24.-prxs")
    price = price_element.text

    # Encoding as UTF8 string before printing(unicode character,cedis)
    sys.stdout.reconfigure(encoding="utf-8")
    print("Current price:", price)

    # check if price has changed
    if price != last_price:
        print("New price:", price)
        last_price = price

        # Sending alert via email
        Email = MIMEMultipart()
        Email["From"] = config.Email_Address
        Email["To"] = "eyramdunyoh4@gmail.com"
        Email["Subject"] = "Price Update🚨!"
        Email.attach(
            MIMEText(f"The current price of {product} just changed.\n\n 💰 New Price: {price}"))
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.ehlo()
                smtp.login(config.Email_Address, config.Email_Password)
                print("Logged in successfully")
                smtp.send_message(Email)
                print("Email sent successfully!")

        except smtplib.SMTPException as e:
            print(f"Error sending email: {e}")

    else:
        print("No price change")

    time.sleep(interval)

browser.quit()
