import re
import wikipedia
import pandas as pd
import Levenshtein as lev
from fuzzywuzzy import process, fuzz
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

unassigned = []

filep = r'FILLWITH_FILEPATH'
df = pd.read_excel(filep, sheet_name=0, usecols='A')
result_df = pd.DataFrame(columns=('search-name', 'Wikipedia-page', 'year-founded','request'))

standard_url = 'https://en.wikipedia.org/wiki/{uni}'

path_chromedriver = r'C:User\chromedriver.exe'
options = Options()
#options.add_argument('--headless')
driver = webdriver.Chrome(path_chromedriver, options=options)
rounds = 0

for i in range(0, len(df)):
    rounds += 1
    print('\t'+df['names'][i]+' request# '+str(rounds) + ' ('+str(round((100*(rounds/len(df))),2))+'%)')
    # API performs a wikipedia search:
    university = df['names'][i]
    results = wikipedia.search(university)
    # FuzzyWuzzy picks one result of the results by fuzzy match
    partly = []
    for i in range(0, len(results)):
        ratio = lev.ratio(results[i].lower(), university.lower())
        if ratio > 0.75:
            partly.append(results[i])
        else:
            pass
    result = process.extractOne(university, partly)
    if result is not None:
        try:
            result_fit = result[0].replace(' ','_')
            driver.get(standard_url.format(uni=result_fit))
            try:
                area = WebDriverWait(driver,15).until(
                    EC.visibility_of_element_located((By.ID,'mw-content-text'))
                )
                if (len(driver.find_elements_by_class_name('infobox vcard')) > 0) or (len(driver.find_elements_by_class_name('infobox')) > 0):
                    opts = driver.find_elements_by_tag_name('tr') #infobox.find_elements_by_class_name('infobox-label')
                    for topic in opts:
                        topix = topic.get_attribute('textContent')
                        if topix.isprintable() == True:
                            topic = topic.text
                        else:
                            topic = topix.replace("\r"," ").replace('\n', ' ')
                        estab = topic[:11].lower().strip()
                        if estab == 'established':
                            pattern = re.compile(r'\d\d\d\d')
                            match = pattern.search(topic)
                            year = match[0]
                            print(year)
                            sed = [university, result, year, standard_url.format(uni=result_fit)]
                            result_df.loc[len(result_df)] = sed
                        else:
                            pass
                else:
                    pass
                    print('no infobox found')
            except BaseException as error:
                print(error)
        except wikipedia.exceptions.DisambiguationError as error:
            print(error)
        except  BaseException as error:
            print(error)
        finally:
            year = ''
    else:
        pass
        print('no match on Wikipedia')
        unassigned.append(university)