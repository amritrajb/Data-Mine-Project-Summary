import requests
from bs4 import BeautifulSoup
import xlsxwriter
import pandas as pd
import pprint
import os

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
            project_info_dict["Lecture time"] = lecture_time[1:][0]
        if "Lab time:" in element:
            lab_time = element.split(":",1)
            project_info_dict["Lab time"] = lab_time[1:][0]
        if "Domain:" in element:
            domain = element.split(":",1)
            project_info_dict["Domain"] = domain[1:][0]
        if "Keywords:" in element:
            keywords = element.split(":",1)
            project_info_dict["Keywords"] = keywords[1:][0]
        if "Tools:" in element:
            tools = element.split(":",1)
            project_info_dict["Tools"] = tools[1:][0]
        if "Citizenship:" in element:
            citizenship = element.split(":",1)
            project_info_dict["Citizenship"] = citizenship[1:][0]
        if "Summary" in element:
            summary = lines[index + 1]
            project_info_dict["Summary"] = summary
        if "Description" in element:
            description = lines[index + 1]
            project_info_dict["Description"] = description
    return project_info_dict

def cell_write(worksheet, row, column, cell_entry):
    cell_format = workbook.add_format({'text_wrap': True})
    cell_format.set_align('left')
    cell_format.set_align('vcenter')
    worksheet.set_column(row, column, len(cell_entry))
    worksheet.write(row, column, cell_entry, cell_format)

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

counter = 0
for url_name in url_dict:
    print(url_name)
    # counter += 1
    # if counter >= 5:
    #     break
    reqs = requests.get(url_name)
    soup = BeautifulSoup(reqs.text, 'html.parser')
 
    sub_url_data_list = []
    for sub_url in soup.find_all('a'):
        #print(sub_url)
        if not "<a class=" in str(sub_url):
            #print(sub_url)
            sub_url_name = "https://projects.the-examples-book.com" + sub_url.get('href')
            sub_url_data = extract_project_data(sub_url_name)
            sub_url_data_list.append(sub_url_data)

    url_dict[url_name] = sub_url_data_list
        
#pprint.pprint(url_dict)

workbook = xlsxwriter.Workbook(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_mine_projects.xlsx"))
worksheet = workbook.add_worksheet()

headings = ["Company Name", "Project Name", "Lecture time", "Lab time", "Domain", 
    "Keywords", "Tools", "Citizenship", "Summary", "Description"]
heading_column = 0
heading_format = workbook.add_format({'bold': True})
for element in headings:
    worksheet.write(0, heading_column, element, heading_format)
    heading_column += 1

row =  1

for k,v in url_dict.items():
    company_name = k.split("/")[-2]
    cell_write(worksheet, row, 0, company_name)
    for project in v:
        project_name = project["url"].split("/")[-2]
        cell_write(worksheet, row, 1, project_name)
        column = 2
        for element in headings:
            if (element != "Company Name") and (element != "Project Name"): 
                cell_entry = project[element]
                #print(cell_entry)
                cell_write(worksheet, row, column, cell_entry)
                column += 1
        row += 1

workbook.close()

# # Create a Pandas dataframe from some data.
# df = pd.DataFrame.from_dict(url_dict, orient='index')
# #print(df.head)

# # Create a Pandas Excel writer using XlsxWriter as the engine.
# writer = pd.ExcelWriter('data_mine_projects.xlsx', engine='xlsxwriter')

# # Convert the dataframe to an XlsxWriter Excel object.
# df.to_excel(writer, sheet_name='2022-2023 Projects')

# # Close the Pandas Excel writer and output the Excel file.
# writer.save()

    
