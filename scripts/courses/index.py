import csv
from prefixes import prefix
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def initialize_driver():
    options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications": 2}
    options.add_experimental_option("prefs", prefs)
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def parseBody(body):
    # name = body.pop(0)
    deparment, course, name = body.pop(0).strip().split(" ",2)
    name = name.split("- ", 1)[1]   
    units = body.pop(0)
    description = next((text for text in body if not text.startswith("Prerequisite(s)") and not text.startswith("Grading: ")), None)
    prereqs = next((text for text in body if text.startswith("Prerequisite(s)") or text.startswith("Pre/Corequisite(s)")), None)
    crosslist = next((text for text in body if text.startswith("Cross-listed ")), None)
    grading = next((text for text in body if text.startswith("Grading: ")), None)
    satisfies = next((text for text in body if text.startswith("Satisfies ")), None)
    repeatable = next((text for text in body if text.startswith("Course may be repeated for credit for up to ")), None)
    sustainability = next((text for text in body if text.startswith("Sustainability")), None)
    notes = next((text for text in body if "Note(s):" in text), None)
    
    return [deparment, course, name,units,description,prereqs,satisfies,grading,repeatable,crosslist,sustainability,notes]

#need this bc the course website sometimes just doesnt load correctly for some reason and needs a refresh
#why is sj's own course website broken
def findRows(driver):
    #try 10 reloads
    for i in range(10):
        try:
            rows = WebDriverWait(driver,5).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME,"width"))
            )
            return rows
        except:
            driver.refresh()
            continue
    return None

def getClassesData(driver,courses):
    rows = findRows(driver)
    if rows is None:
        print('didnt find anything')
        return;    
    for row in rows:
        link = WebDriverWait(row,5).until(
            EC.presence_of_element_located((By.TAG_NAME,"a"))
        ).click()
        title = WebDriverWait(row,5).until(
            EC.presence_of_element_located((By.TAG_NAME,"h3"))
        )
        body = title.find_element(By.XPATH, "..").text
        body= body.split("\n")
        courseInfo = parseBody(body)
        courses.append(courseInfo)


def scrape_courses(prefixes):
    courses= []
    driver = initialize_driver()
    for tag in prefixes:
        driver.get(f'https://catalog.sjsu.edu/content.php?filter[27]={tag}&filter[29]=&filter[keyword]=&filter[32]=1&filter[cpage]=1&cur_cat_oid=14&expand=&navoid=5106&search_database=Filter&filter[exact_match]=1#acalog_template_course_filter')
        print(tag)
        getClassesData(driver,courses)
        try:
        #sometimes the page has a page 2...
            driver.find_element(By.CSS_SELECTOR, '[aria-label="Page 2"]').click()
            getClassesData(driver,courses)
        except:
            continue
    return courses

def save_to_csv(data):
    filename='courses.csv'
    with open(filename, 'w', encoding="utf-8", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Department","Course","Name","Units","Description","Prereqs","Satisfies","Grading","Repeatable","Crosslist","Sustainability","Notes"])
        writer.writerows(data)

courses= scrape_courses(prefix)
save_to_csv(courses)




