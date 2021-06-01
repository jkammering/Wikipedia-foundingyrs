# Wikipedia-foundingyrs


## Aim of project
This project aimed at scraping founding years from Wikipedia. Specifically from the infobox of these webpages.

## Methods/Libraries used
Matching Wikipedia webpages with supplied data: **WikiMedia (Wikipedia API)** <br />
Scraping infoboxes: **Selenium Webdriver** <br />
Fuzzy Match: **FuzzyWuzzy, Levenshtein** <br />

## Method
The universities names are loaded into a Pandas DataFrame and then parsed through. Therein, the API supplies several results for the search term, a Fuzzy Match is performed to choose the correct page. 75% matching threshold was choosen here from testing with a data set. The webpage is then retrieved by the Selenium Webdriver. If there is an infobox present, we parse the <tr> tags that hold information in of the infobox. The tags are tested for elements that might not be compilable by the Editor (utf-8/ascii) through the .isprintable() Method. If this tag contains "Established" we perform regex on the textelement. This returns the founding year of the university. Results are saved in a dataframe.
  
