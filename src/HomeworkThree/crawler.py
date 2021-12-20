from selenium import webdriver


def get_subject_page_url(browser: webdriver.Firefox):
    subjects = browser.find_elements_by_css_selector("li.medium-up-block > h3:nth-child(1) > a:nth-child(2)")
    results = []
    for subject in subjects:
        link = subject.get_attribute("href")
        temp = subject.text.split("\n")
        title = [0]
        course_count = temp[1].split(" ")[0]
        results.append((title, link, course_count))

    return results


def load_all_course_in_subject(browser: webdriver.Firefox, subject_data):
    print(subject_data)


initial_url = "https://www.classcentral.com/subjects"

driver = webdriver.Firefox()
try:
    driver.get(initial_url)

    subjects_data = get_subject_page_url(driver)
    for temp in subjects_data:
        load_all_course_in_subject(driver, temp)

    driver.close()
except Exception as e:
    print(e)
    driver.close()
    exit(2)
