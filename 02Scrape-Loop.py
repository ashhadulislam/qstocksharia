#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
sys.path.append("/Users/dr.ashhadulislam/projects/social/musaffaScraper")
import config
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle


# In[2]:


print(config.qat_company_categorised)


# In[3]:


print(config.qat_categories)


# In[4]:


import os
import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException



# Setup Firefox (headless optional)
options = Options()
# options.add_argument("--headless")  # remove this if you want to see the browser

driver = webdriver.Firefox(options=options)



# In[5]:


driver.get("https://musaffa.com/authentication/login")

# Wait for the markers to appear (wait up to 10 seconds)
wait = WebDriverWait(driver, 10)


# In[6]:


# sign_in_button = driver.find_element(By.LINK_TEXT, "Sign In")


# In[7]:


# sign_in_button.click()


# In[8]:


email_id = driver.find_element(By.ID, "email")
email_id.clear()
email_id.send_keys("fazlursyarif77@gmail.com")

passwd = driver.find_element(By.ID, "password")
passwd.clear()
passwd.send_keys("Bismillah@123.")
login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
time.sleep(3)
login_button.click()


# In[9]:


## considering that we logged in and we have a subscription
## we want to get the first level shariah compliance info


# In[10]:


company_name="ZHCD.QA"



url=f"https://musaffa.com/stock/{company_name}"
driver.get(url)

# Wait for the markers to appear (wait up to 10 seconds)
wait = WebDriverWait(driver, 10)


# In[11]:


shariah_compliance_info_level1 = {}

try:
    # Title
    shariah_compliance_info_level1["Title"] = driver.find_element(By.CSS_SELECTOR, "h4.header-h4").text.strip()

    # Screening Methodology
    shariah_compliance_info_level1["Screening Methodology"] = driver.find_element(By.CSS_SELECTOR, ".header-para span.fw-600").text.strip()

    # Compliance Status (HALAL / NOT HALAL)
    status_element = driver.find_elements(By.CSS_SELECTOR, ".compliance-chip h5.status-text")
    shariah_compliance_info_level1["Compliance Status"] = status_element[0].text.strip() if status_element else "N/A"

    # Rating (optional)
    rating_element = driver.find_elements(By.CSS_SELECTOR, ".rating_grade_status")
    shariah_compliance_info_level1["Rating"] = rating_element[0].text.strip() if rating_element else "N/A"

    # Last Updated (optional)
    updated_element = driver.find_elements(By.XPATH, "//p[contains(text(), 'Last Updated')]/span")
    shariah_compliance_info_level1["Last Updated"] = updated_element[0].text.strip() if updated_element else "N/A"

    # Report Source (optional)
    report_source_element = driver.find_elements(By.XPATH, "//p[contains(text(), 'Report Source')]/span")
    shariah_compliance_info_level1["Report Source"] = report_source_element[0].text.strip() if report_source_element else "N/A"

    # View Compliance History Button (optional)
    try:
        history_btn = driver.find_element(By.XPATH, "//button//span[contains(text(), 'View Compliance History')]")
        shariah_compliance_info_level1["History Link"] = history_btn.text.strip()
    except:
        shariah_compliance_info_level1["History Link"] = "N/A"

    # Action Button (optional)
    try:
        action_btn = driver.find_element(By.CSS_SELECTOR, "button.card-btn span")
        shariah_compliance_info_level1["Action Button"] = action_btn.text.strip()
    except:
        shariah_compliance_info_level1["Action Button"] = "N/A"

except Exception as e:
    shariah_compliance_info_level1["Error"] = str(e)

print(shariah_compliance_info_level1)


# In[12]:


## click on view detailed report


# In[ ]:





# In[13]:


button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[span[text()='View Detailed Report']]"))
    )
button.click()
print("Clicked 'View Detailed Report' button.")
wait = WebDriverWait(driver, 10)


# # Detail report

# ## Business screening

# ### Business activity

# In[14]:


time.sleep(3)
# Locate the Business Activity tab
business_activity_tab = driver.find_element(
    By.XPATH,
    "//a[contains(@class, 'tab-btn') and .//span[text()='Business Activity']]"
)

# Get the status text (e.g., "Pass" or "Fail")
status_text = business_activity_tab.find_element(By.CLASS_NAME, "tabs-badge").text.strip()

# Store in dictionary
business_screening = {
    "business_activity": status_text  # "Pass" or "Fail"
}

# Print result
print(business_screening)


# ### get the absolute values

# ### click on calculation drop down

# In[15]:


# driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.SPACE)
# # Wait until the button is clickable
# try:
#     calc_dropdown_btn = WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((
#             By.XPATH, "//button[.//span[text()='Calculation']]"
#         ))
#     )
#     calc_dropdown_btn.click()
#     print("Calculation dropdown clicked.")
# except Exception as e:
#     print("Failed to click Calculation dropdown:", e)

try:
    # Wait for element to be present
    calc_dropdown_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((
            By.XPATH, "//button[.//span[text()='Calculation']]"
        ))
    )

    # Scroll it into view (align to center)
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", calc_dropdown_btn)

    # Wait briefly for scroll to complete/rendering
    WebDriverWait(driver, 2).until(EC.element_to_be_clickable((
        By.XPATH, "//button[.//span[text()='Calculation']]"
    )))

    # Click using JavaScript (bypasses viewport issues)
    driver.execute_script("arguments[0].click();", calc_dropdown_btn)
    print("Calculation dropdown clicked via JS.")

except Exception as e:
    print("Failed to click Calculation dropdown:", e)


# In[16]:


time.sleep(3)
switch = driver.find_element(By.CSS_SELECTOR, "label.toggle-switch")
switch.click()


# In[17]:


# Wait for the content to load
WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, "calculation-line-item-title"))
)

# Build the dictionary
absolute_halal_calculation = {
    "Halal Sales & Income": driver.find_element(By.XPATH, "//p[contains(text(), 'Halal Sales')]/following-sibling::span").text.strip(),
    "Doubtful Sales & Income": driver.find_element(By.XPATH, "//p[contains(text(), 'Doubtful Sales')]/following-sibling::span").text.strip(),
    "Non Halal Sales & Income": driver.find_element(By.XPATH, "//p[contains(text(), 'Non Halal Sales')]/following-sibling::span").text.strip(),
    "Total Revenue": driver.find_element(By.XPATH, "//p[contains(text(), 'Total Revenue')]/following-sibling::span").text.strip(),
}

print(absolute_halal_calculation)


# ### click on detailed report

# In[18]:


try:
    # Wait for element to be present
    calc_dropdown_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((
            By.XPATH, "//button[.//span[text()='Detailed Report']]"
        ))
    )

    # Scroll it into view (align to center)
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", calc_dropdown_btn)

    # Wait briefly for scroll to complete/rendering
    WebDriverWait(driver, 2).until(EC.element_to_be_clickable((
        By.XPATH, "//button[.//span[text()='Detailed Report']]"
    )))

    # Click using JavaScript (bypasses viewport issues)
    driver.execute_script("arguments[0].click();", calc_dropdown_btn)
    print("Detailed Report dropdown clicked via JS.")

except Exception as e:
    print("Failed to click Detailed Report dropdown:", e)


# In[19]:


# time.sleep(2)
# driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.SPACE)
# try:
#     calc_dropdown_btn = WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((
#             By.XPATH, "//button[.//span[text()='Detailed Report']]"
#         ))
#     )
#     calc_dropdown_btn.click()
#     print("Detailed Report clicked.")
# except Exception as e:
#     print("Failed to click Detailed Report:", e)


# In[20]:


# Find all income blocks
blocks = driver.find_elements(By.CSS_SELECTOR, "div.breakdown-card")


# In[21]:


detailed_report = {}

for block in blocks:
    # Get the top-level label (e.g., Halal Revenue)
    title = block.find_element(By.CSS_SELECTOR, "span.title").text.strip()
    total = block.find_element(By.CSS_SELECTOR, "span.percent").text.strip()

    detailed_report[title] = {"_total": total}

    # Look for all breakdown buttons
    buttons = block.find_elements(By.CSS_SELECTOR, "button[ngbpaneltoggle]")

    for btn in buttons:
        try:
            sub_label = btn.find_element(By.CLASS_NAME, "accordion-btn-title").text.strip()
            sub_value = btn.find_element(By.CLASS_NAME, "accordion-btn-val").text.strip()
            detailed_report[title][sub_label] = sub_value
        except:
            continue  # Skip if any part is missing





# In[22]:


print(detailed_report)


# ## End of Business Screening

# ## Financial Screening

# In[23]:


# Find all tabs
tabs = driver.find_elements(By.CSS_SELECTOR, "a.tab-btn")

# Initialize dictionary
financial_screening = {}

# Loop through the tabs to find the ones related to Financial Screening
for tab in tabs:
    label = tab.text.lower()
    status = tab.find_element(By.CLASS_NAME, "tabs-badge").text.strip()
    
    if "interest-bearing" in label and "securities" in label:
        financial_screening["interest_bearing_securities_and_assets"] = status
    elif "interest-bearing" in label and "debt" in label:
        financial_screening["interest_bearing_debt"] = status

# Print result
print(financial_screening)


# ### interest bearing securities and assets

# In[24]:


time.sleep(1)
driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.HOME)
time.sleep(2)
buttons = driver.find_elements(By.CSS_SELECTOR, "a.tab-btn")
for btn in buttons:
    if "Interest-bearing" in btn.text and "securities" in btn.text:
        btn.click()
        break


# In[27]:


try:
    # Wait for element to be present
    calc_dropdown_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((
            By.XPATH, "//button[.//span[text()='Calculation']]"
        ))
    )

    # Scroll it into view (align to center)
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", calc_dropdown_btn)

    # Wait briefly for scroll to complete/rendering
    WebDriverWait(driver, 2).until(EC.element_to_be_clickable((
        By.XPATH, "//button[.//span[text()='Calculation']]"
    )))

    # Click using JavaScript (bypasses viewport issues)
    driver.execute_script("arguments[0].click();", calc_dropdown_btn)
    print("Calculation dropdown clicked via JS.")

except Exception as e:
    print("Failed to click Calculation dropdown:", e)


# In[28]:


# Initialize the result dictionary
time.sleep(3)
interest_bearing_percentage = {}

# Find all blocks containing interest-bearing calculation lines
blocks = driver.find_elements(By.CSS_SELECTOR, "div.col-md-6")

for block in blocks:
    titles = block.find_elements(By.CSS_SELECTOR, ".calculation-line-item-title")
    values = block.find_elements(By.CSS_SELECTOR, ".calculation-line-item-val")

    if len(titles) == 3 and "Interest-bearing securities and assets" in titles[2].text:
        interest_bearing_percentage = {
            titles[0].text.strip(): values[0].text.strip(),
            titles[1].text.strip(): values[1].text.strip(),
            titles[2].text.strip(): values[2].text.strip()
        }
        break  # Exit loop once found

print(interest_bearing_percentage)


# In[29]:


time.sleep(2)
switch = driver.find_element(By.CSS_SELECTOR, "label.toggle-switch")
switch.click()


# In[30]:


time.sleep(2)
### now get the absolute values
# Initialize the result dictionary
interest_bearing_absolute = {}

# Find all blocks containing interest-bearing calculation lines
blocks = driver.find_elements(By.CSS_SELECTOR, "div.col-md-6")

for block in blocks:
    titles = block.find_elements(By.CSS_SELECTOR, ".calculation-line-item-title")
    values = block.find_elements(By.CSS_SELECTOR, ".calculation-line-item-val")

    if len(titles) == 3 and "Interest-bearing securities and assets" in titles[2].text:
        interest_bearing_absolute = {
            titles[0].text.strip(): values[0].text.strip(),
            titles[1].text.strip(): values[1].text.strip(),
            titles[2].text.strip(): values[2].text.strip()
        }
        break  # Exit loop once found

print(interest_bearing_absolute)


# In[31]:


# now get the Trailing 36-month average market capitalization

# Find all percentage calculation blocks
percentage_blocks = driver.find_elements(By.CSS_SELECTOR, "div.calc-percent.text-center")

# Initialize the output variable
trailing_36_month_avg_market_cap = None

# Loop through and extract the denominator
for block in percentage_blocks:
    try:
        fraction_spans = block.find_elements(By.CSS_SELECTOR, "div.d-flex.flex-column.align-items-center span")
        if len(fraction_spans) == 2:
            trailing_36_month_avg_market_cap = fraction_spans[1].text.strip()
            break
    except Exception as e:
        print("Error extracting market cap:", e)

print("Trailing 36-month average market capitalization:", trailing_36_month_avg_market_cap)


# ### interest bearing debt

# In[32]:


driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.HOME)
time.sleep(2)
buttons = driver.find_elements(By.CSS_SELECTOR, "a.tab-btn")
for btn in buttons:
    if "Interest-bearing" in btn.text and "debt" in btn.text:
        btn.click()
        break


# In[ ]:


# driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.SPACE)


# In[33]:


time.sleep(2)
try:
    # Wait for element to be present
    calc_dropdown_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((
            By.XPATH, "//button[.//span[text()='Calculation']]"
        ))
    )

    # Scroll it into view (align to center)
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", calc_dropdown_btn)

    # Wait briefly for scroll to complete/rendering
    WebDriverWait(driver, 2).until(EC.element_to_be_clickable((
        By.XPATH, "//button[.//span[text()='Calculation']]"
    )))

    # Click using JavaScript (bypasses viewport issues)
    driver.execute_script("arguments[0].click();", calc_dropdown_btn)
    print("Calculation dropdown clicked via JS.")

except Exception as e:
    print("Failed to click Calculation dropdown:", e)


# In[34]:


time.sleep(3)
# Initialize the result dictionary
interest_bearing_debt_percentage = {}

# Find all blocks containing interest-bearing calculation lines
blocks = driver.find_elements(By.CSS_SELECTOR, "div.col-md-6")

for block in blocks:
    titles = block.find_elements(By.CSS_SELECTOR, ".calculation-line-item-title")
    values = block.find_elements(By.CSS_SELECTOR, ".calculation-line-item-val")

    if len(titles) == 3 and "Total Interest-bearing debt" in titles[2].text:
        interest_bearing_debt_percentage = {
            titles[0].text.strip(): values[0].text.strip(),
            titles[1].text.strip(): values[1].text.strip(),
            titles[2].text.strip(): values[2].text.strip()
        }
        break  # Exit loop once found

print(interest_bearing_debt_percentage)


# In[35]:


switch = driver.find_element(By.CSS_SELECTOR, "label.toggle-switch")
switch.click()


# In[36]:


time.sleep(2)
# Initialize the result dictionary
interest_bearing_debt_absolute = {}

# Find all blocks containing interest-bearing calculation lines
blocks = driver.find_elements(By.CSS_SELECTOR, "div.col-md-6")

for block in blocks:
    titles = block.find_elements(By.CSS_SELECTOR, ".calculation-line-item-title")
    values = block.find_elements(By.CSS_SELECTOR, ".calculation-line-item-val")

    if len(titles) == 3 and "Total Interest-bearing debt" in titles[2].text:
        interest_bearing_debt_absolute = {
            titles[0].text.strip(): values[0].text.strip(),
            titles[1].text.strip(): values[1].text.strip(),
            titles[2].text.strip(): values[2].text.strip()
        }
        break  # Exit loop once found

print(interest_bearing_debt_absolute)


# ## Compliance history

# In[37]:


try:
    # Wait until any button with "View Compliance History" text appears
    history_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((
            By.XPATH, "//button[.//span[normalize-space(text())='View Compliance History']]"
        ))
    )

    # Scroll it into view
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", history_button)

    # Wait a little to ensure scroll is complete
    WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((
            By.XPATH, "//button[.//span[normalize-space(text())='View Compliance History']]"
        ))
    )

    # Click using JavaScript for robustness
    driver.execute_script("arguments[0].click();", history_button)
    print("Clicked 'View Compliance History' button.")

except Exception as e:
    print("Failed to click 'View Compliance History':", e)


# In[38]:


# Ensure you're at the compliance history section
try:
    container = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.history-list-container"))
    )
    
    # Scroll the container multiple times to ensure full list is loaded
    for _ in range(10):  # Adjust this if needed
        driver.execute_script("arguments[0].scrollBy(0, 300);", container)
        time.sleep(0.3)

    # Extract all compliance history items
    history_items = driver.find_elements(By.CSS_SELECTOR, "li.compliance-history-item")

    compliance_history = []
    for item in history_items:
        try:
            date_range = item.find_element(By.CSS_SELECTOR, ".year-span").text.strip()
            report_source = item.find_element(By.CSS_SELECTOR, ".quarter-text").text.replace("Report Source:", "").strip()
            status = item.find_element(By.CSS_SELECTOR, ".history-chip").text.strip()

            compliance_history.append({
                "date_range": date_range,
                "report_source": report_source,
                "status": status
            })
        except Exception as e:
            print("Skipping one item due to error:", e)
            continue

    print("Extracted Compliance History:")
    for entry in compliance_history:
        print(entry)

except Exception as e:
    print("Failed to extract compliance history:", e)


# ## Save it all

# In[39]:


# Aggregate everything into one dictionary
full_report = {
    "shariah_compliance_info_level1": shariah_compliance_info_level1,
    "business_screening": business_screening,
    "absolute_halal_calculation": absolute_halal_calculation,
    "detailed_report": detailed_report,
    "financial_screening": financial_screening,
    "interest_bearing_percentage": interest_bearing_percentage,
    "interest_bearing_absolute": interest_bearing_absolute,
    "trailing_36_month_avg_market_cap": trailing_36_month_avg_market_cap,
    "interest_bearing_debt_percentage": interest_bearing_debt_percentage,
    "interest_bearing_debt_absolute": interest_bearing_debt_absolute,
    "compliance_history":compliance_history
}

# Create a valid filename from company name
filename = f"reports/{company_name.replace('.', '_')}.pkl"

# Save as pickle file
with open(filename, 'wb') as f:
    pickle.dump(full_report, f)

print(f"Saved report to {filename}")


# In[40]:


full_report


# In[ ]:




