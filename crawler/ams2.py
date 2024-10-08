import os
import re
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

# Initialize Selenium settings
chrome_options = Options()
service = Service('D:/chromedriver-win64/chromedriver.exe')
chrome_options.add_argument("--no-first-run")
chrome_options.add_argument("--no-default-browser-check")

# Get the directory where the script is running
current_directory = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the JSON file
json_file_path = os.path.join(current_directory, 'ams_jobs.json')

# Initialize the browser
driver = webdriver.Chrome(service=service, options=chrome_options)

# Define regex pattern to clean job titles
regex_to_remove = r"""
\(
[dmfwx](/?[dmfwx])*    # Matches patterns like (m/w/d), (f/m/d), (m/f/x), etc.
(\s/\*)?               # Optionally matches space followed by "/*"
\)                     # Matches closing parenthesis
|
[:/\*]*in              # Matches combinations of :, /, * followed by "in"
|
\(all genders\)        # Matches the specific pattern "(all genders)"
"""

# Compile the regex with re.VERBOSE and re.IGNORECASE flags for better readability and case insensitivity
compiled_regex = re.compile(regex_to_remove, re.VERBOSE | re.IGNORECASE)

def extract_job_information_from_page(driver):
    all_job_data = []

    try:
        # Locate job elements on the page
        job_list = driver.find_elements(By.XPATH, '/html/body/sn-root/main/sn-search-page/div/div[1]/div[4]/section/sn-job-cards/sn-list-container/div/div/sn-list-item-container')

        for job_element in job_list:
            try:
                # Extract job link and company name
                link_element = job_element.find_element(By.XPATH, './/div/div/div[1]/div[1]/sn-list-item-header/h2/a')
                company_element = job_element.find_element(By.XPATH, './/div/div/div[2]/div[1]/sn-list-item-left/ams-icon-value[1]/div/div[2]/span')
                
                job_position = link_element.text.strip()
                company_name = company_element.text.strip()

                # Clean job title using the regex pattern
                clean_position = compiled_regex.sub('', job_position)

                # Store job information
                job_info = {
                    "URL": link_element.get_attribute('href'),
                    "position": clean_position,
                    "company": company_name
                }
                all_job_data.append(job_info)

            except NoSuchElementException:
                continue

    except NoSuchElementException:
        pass

    return all_job_data

def crawl_ams_jobs():
    page_number = 0

    while True:
        # Construct URL for the current page
        url = f'https://jobs.ams.at/public/emps/jobs?page={page_number}&query=tester&location=wien&JOB_OFFER_TYPE=SB_WKO&JOB_OFFER_TYPE=IJ&JOB_OFFER_TYPE=BA&WORKING_TIME=V&PERIOD=ALL&sortField=_SCORE'
        driver.get(url)
        time.sleep(2)  # Wait for the page to load

        # Check if there are no more pages
        if "error" in driver.current_url:
            print(f"No more pages found. Stopping at page {page_number}.")
            break

        # Extract job data from the current page
        job_data = extract_job_information_from_page(driver)
        if not job_data:
            print(f"No more job listings found. Stopping at page {page_number}.")
            break

        # Read the current JSON file or create a new list
        try:
            with open(json_file_path, 'r+', encoding='utf-8') as file:
                try:
                    jobs = json.load(file)
                except json.JSONDecodeError:
                    jobs = []
                jobs.extend(job_data)
                file.seek(0)
                json.dump(jobs, file, ensure_ascii=False, indent=4)
                file.truncate()
                print(f"Added {len(job_data)} jobs to JSON file.")
        except FileNotFoundError:
            with open('ams_jobs.json', 'w', encoding='utf-8') as file:
                json.dump(job_data, file, ensure_ascii=False, indent=4)
                print(f"Created new JSON file with {len(job_data)} jobs.")

        page_number += 1

    print("Job data extraction and saving completed.")

# Start crawling
crawl_ams_jobs()

# Close the browser
driver.quit()
