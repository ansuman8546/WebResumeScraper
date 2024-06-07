from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import csv
import time

# Initialize Chrome webdriver
driver = webdriver.Chrome()  # Adjust the path to your Chrome driver if necessary

# Base URL of the website
base_url = "https://www.lockheedmartinjobs.com"

# Open CSV file in write mode
with open('job_listingscs.csv', 'w', newline='', encoding='utf-8') as csvfile:
    # Create a CSV writer object
    csv_writer = csv.writer(csvfile)
    
    # Write header row
    csv_writer.writerow(['Title', 'Location', 'Date Posted', 'Job ID', 'Link'])

    # Load the first page
    driver.get(f"{base_url}/search-jobs")
    time.sleep(2)  # Add a delay to ensure the page loads completely

#cookie banner!
    try:
        cookie_banner = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'ccpa-alert')))
        # If it does, click the "Close" button
        cookie_banner.find_element(By.ID, 'ccpa-button').click()
    except TimeoutException:
        print("Cookie consent banner not found or no close button")

    # Click on the "Career Area" dropdown
    career_area_dropdown = driver.find_element(By.ID, 'category-toggle')
    career_area_dropdown.click()
    time.sleep(4)  # Add a delay to ensure the dropdown expands completely
    #Click on the filter checkbox for "Artificial Intelligence"
    filter_checkbox = driver.find_element(By.ID, 'category-filter-2')
    filter_checkbox.click()
    time.sleep(7)
    


    #clicks experience level


    while True:
        # Wait for the applied filters modal to be present
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="search-results-list"]/ul')))

        # Find the section containing job listings
        job_listings = driver.find_elements(By.XPATH, '//*[@id="search-results-list"]/ul')

        # If job listings are found, extract job details
        if job_listings:
            for job in job_listings:
                title = job.find_element(By.CSS_SELECTOR, 'span.job-title').text.strip()
                location = job.find_element(By.CSS_SELECTOR, 'span.job-location').text.strip()
                date_posted = job.find_element(By.CSS_SELECTOR, 'span.job-date-posted').text.strip().replace('Date Posted: ', '')
                job_id = job.find_element(By.CSS_SELECTOR, 'span.job-id').text.strip().replace('Job ID: ', '')
                link = job.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')

                # Write job data to CSV file
                csv_writer.writerow([title, location, date_posted, job_id, link])


                # Write job data to CSV file
                csv_writer.writerow([title, location, date_posted, job_id, link])

        else:
            print("Job listings section not found")
            break
        
        current_page = int(driver.find_element(By.CSS_SELECTOR, 'input.pagination-current').get_attribute('value'))
        print(current_page)

        # Find the "Next" button
        next_button = driver.find_element(By.CSS_SELECTOR, 'a.next')

        if next_button.is_enabled():
            # Wait until the obscuring element is no longer visible
            WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.ID, 'ccpa-alert')))

            # Use JavaScript to click the "Next" button
            driver.execute_script("arguments[0].click();", next_button)

            # Wait for the page to load
            time.sleep(10)

            WebDriverWait(driver, 10).until(lambda d: int(d.find_element(By.CSS_SELECTOR, 'input.pagination-current').get_attribute('value')) > current_page)
        # If there is a "Next" button, update the page number
            new_page = int(driver.find_element(By.CSS_SELECTOR, 'input.pagination-current').get_attribute('value'))
            if new_page <= current_page:
                print("No more pages")
                break
        else:
            print("No more pages")
            break

        # Add a delay to avoid overwhelming the server
        time.sleep(3)

# Close the webdriver
driver.quit()

print("Job listings scraped and saved to job_listings.csv")
