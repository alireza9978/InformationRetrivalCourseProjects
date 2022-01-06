import math

import pandas as pd
from selenium import webdriver


def get_subject_page_url(browser: webdriver.Firefox):
    subjects = browser.find_elements_by_css_selector("li.medium-up-block > h3:nth-child(1) > a:nth-child(2)")
    results = []
    for subject in subjects:
        link = subject.get_attribute("href")
        temp = subject.text.split("\n")
        title = temp[0]
        course_count = temp[1].split(" ")[0]
        results.append((title, link, course_count))

    return results


def load_all_course_in_subject(browser: webdriver.Firefox, subject_data, index):
    columns = ["course_name", "course_instructor_site", "course_site", "course_instructor", "course_cost",
               "course_credential", "course_level", "course_duration", "course_language", "course_caption_languages",
               "overview", "syllabus"]
    subject_df = pd.DataFrame()
    # for i in range(1, 3):
    total_pages = math.ceil(int(subject_data[2]) / 15)
    print(f"total pages is {total_pages} in subject {subject_data[0]}")
    for i in range(index, total_pages):
        temp_page = subject_data[1] + f"?page={i}"
        course_urls = extract_course_urls_from_single_page(browser, temp_page)
        for url in course_urls:
            if url.endswith("/classroom"):
                url = url[:-10]
            temp_course_data = extract_course_info_from_single_page(browser, url)
            temp_course_data = pd.Series(temp_course_data, index=columns)
            subject_df = subject_df.append(temp_course_data, ignore_index=True)
        print(f"{i} from {subject_data[0]} finished")
        subject_df.to_csv(f"temp {subject_data[0]}.csv", index=False)

    subject_df = subject_df[columns]
    subject_df["subject"] = subject_data[0]

    return subject_df


def extract_course_info_from_single_page(browser: webdriver.Firefox, url):
    browser.get(url)

    course_name = None
    course_instructor_site = None
    course_instructor = None

    overview = None
    syllabus = None

    course_site = None
    course_cost = None
    course_language = None
    course_credential = None
    course_level = None
    course_duration = None
    course_caption_languages = None

    try:
        course_name = browser.find_element_by_css_selector(".head-1").text
    except Exception:
        pass

    try:
        course_instructor_site = browser.find_element_by_css_selector("p.text-1:nth-child(4) > a:nth-child(1)").text
    except Exception:
        pass

    try:
        left_section_items = browser.find_element_by_css_selector("div.small-down-padding-medium:nth-child(2)")
        for item in left_section_items.find_elements_by_xpath("*"):
            try:
                section_name = item.find_element_by_css_selector("h2").text
                if section_name == "Overview":
                    for sub_section in item.find_elements_by_css_selector("div"):
                        if sub_section.get_attribute("class").__contains__("wysiwyg"):
                            overview = sub_section.text
                elif section_name == "Syllabus":
                    for sub_section in item.find_elements_by_css_selector("div"):
                        if sub_section.get_attribute("class").__contains__("wysiwyg"):
                            syllabus = sub_section.text
            except Exception:
                try:
                    for sub_section in item.find_elements_by_xpath("*"):
                        if sub_section.find_element_by_css_selector("h3").text == "Taught by":
                            course_instructor = sub_section.find_element_by_css_selector("p").text
                except Exception:
                    pass
    except Exception:
        pass

    try:
        right_section_items = browser.find_element_by_css_selector(
            "div.small-down-padding-medium:nth-child(1) > ul:nth-child(3)")
        for item in right_section_items.find_elements_by_xpath("*"):
            try:
                item_classes = item.find_element_by_css_selector("i").get_attribute("class")
                if item_classes.__contains__("icon-provider-charcoal"):
                    course_site = item.find_element_by_css_selector("a").text
                elif item_classes.__contains__("icon-dollar-charcoal"):
                    course_cost = item.find_element_by_css_selector("span").text
                elif item_classes.__contains__("icon-language-charcoal"):
                    course_language = item.find_element_by_css_selector("a").text
                elif item_classes.__contains__("icon-credential-charcoal"):
                    course_credential = item.find_element_by_css_selector("span").text
                elif item_classes.__contains__("icon-clock-charcoal"):
                    course_duration = item.find_element_by_css_selector("span").text
                elif item_classes.__contains__("icon-subtitles-charcoal"):
                    for inner_item in item.find_elements_by_css_selector("span"):
                        if inner_item.get_attribute("class") == "text-2 margin-left-small line-tight":
                            course_caption_languages = inner_item.text

                elif item_classes.__contains__("icon-level-charcoal"):
                    course_level = item.find_element_by_css_selector("span").text
            except Exception:
                pass
    except Exception:
        pass

    return (course_name,
            course_instructor_site,
            course_site,
            course_instructor,
            course_cost,
            course_credential,
            course_level,
            course_duration,
            course_language,
            course_caption_languages,
            overview,
            syllabus)


def extract_course_urls_from_single_page(browser: webdriver.Firefox, url):
    course_urls = []
    browser.get(url)
    courses_box = browser.find_elements_by_css_selector("li.bg-white")
    for course_box in courses_box:
        if course_box.get_attribute("class").__contains__("course-list-course"):
            temp_div = course_box.find_element_by_css_selector("div:nth-child(1) > div:nth-child(1)")
            if len(temp_div.find_elements_by_xpath("*")) == 1:
                course_urls.append(
                    temp_div.find_element_by_css_selector("div:nth-child(1) > a:nth-child(2)").get_attribute("href"))
            elif len(temp_div.find_elements_by_xpath("*")) == 2:
                course_urls.append(
                    temp_div.find_element_by_css_selector("div:nth-child(2) > a:nth-child(2)").get_attribute("href"))
        else:
            # this course is ADS
            pass

    return course_urls


def crawl():
    initial_url = "https://www.classcentral.com/subjects"
    # driver = webdriver.Chrome("../../res/chromedriver")

    profile = webdriver.FirefoxProfile()
    # 1 - Allow all images
    # 2 - Block all images
    # 3 - Block 3rd party images
    profile.set_preference("permissions.default.image", 2)
    driver = webdriver.Firefox(firefox_profile=profile)

    try:
        dataset = pd.DataFrame()
        driver.get(initial_url)

        start = 1
        subjects_data = get_subject_page_url(driver)
        for data in subjects_data:
            subject_df = load_all_course_in_subject(driver, data, start)
            dataset = pd.concat([dataset, subject_df])
            dataset.to_csv("dataset.csv")

        dataset.to_csv("dataset.csv")
        driver.close()
    except Exception as e:
        print(e)
        driver.close()
        exit(2)


if __name__ == '__main__':
    crawl()
