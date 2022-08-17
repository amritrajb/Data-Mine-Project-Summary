import requests
from bs4 import BeautifulSoup
import xlsxwriter
import pandas as pd

def extract_project_data(url):
    project_info_dict = {}
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    text_content = soup.get_text()
    lines = text_content.split("\n")
    project_info_dict["url"] = url
    for index, element in enumerate(lines):
        if "Lecture time:" in element:
            lecture_time = element.split(":",1)
            project_info_dict["Lecture time"] = lecture_time[1:]
        if "Lab time:" in element:
            lab_time = element.split(":",1)
            project_info_dict["Lab time"] = lab_time[1:]
        if "Domain:" in element:
            domain = element.split(":",1)
            project_info_dict["Domain"] = domain[1:]
        if "Keywords:" in element:
            keywords = element.split(":",1)
            project_info_dict["Keywords"] = keywords[1:]
        if "Tools:" in element:
            tools = element.split(":",1)
            project_info_dict["Tools"] = tools[1:]
        if "Citizenship:" in element:
            citizenship = element.split(":",1)
            project_info_dict["Citizenship"] = citizenship[1:]
        if "Summary" in element:
            summary = lines[index + 1]
            project_info_dict["Summary"] = summary
        if "Description" in element:
            description = lines[index + 1]
            project_info_dict["Description"] = description
    return project_info_dict

#print(extract_project_data("https://projects.the-examples-book.com/projects/protect-children-from-accidental-exposure/"))

base_url = 'https://projects.the-examples-book.com/'
url = base_url + "companies/"
reqs = requests.get(url)
soup = BeautifulSoup(reqs.text, 'html.parser')

top_level_urls = [base_url, url, base_url + 'projects/', base_url + 'projects/search']
url_dict = {}
for link in soup.find_all('a'):
    url_name = "https://projects.the-examples-book.com" + link.get('href')
    url_dict[url_name] = []
for url in top_level_urls:
    del url_dict[url]
#print(url_dict)

#counter = 0
for url_name in url_dict:
    print(url_name)
    #counter += 1
    #if counter >= 3:
        #break
    reqs = requests.get(url_name)
    soup = BeautifulSoup(reqs.text, 'html.parser')
 
    for sub_url in soup.find_all('a'):
        sub_url_name = "https://projects.the-examples-book.com" + sub_url.get('href')
        sub_url_data = extract_project_data(sub_url_name)
        url_dict[url_name] = sub_url_data
        
print(url_dict)
exit(1)


# Create a Pandas dataframe from some data.
df = pd.DataFrame.from_dict(url_dict, orient='index')
#print(df.head)

# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('data_mine_projects.xlsx', engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object.
df.to_excel(writer, sheet_name='2022-2023 Projects')

# Close the Pandas Excel writer and output the Excel file.
writer.save()

    
