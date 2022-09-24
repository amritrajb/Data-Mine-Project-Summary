import requests
from bs4 import BeautifulSoup
import xlsxwriter
import pandas as pd
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

def url_write(worksheet, row, column, cell_entry, url):
    cell_format = workbook.add_format({'text_wrap': True})
    cell_format.set_align('left')
    cell_format.set_align('vcenter')
    worksheet.set_column(row, column, len(cell_entry))
    worksheet.write_url(row, column, url, string = cell_entry)


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
    #print(url_name)
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

workbook = xlsxwriter.Workbook(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_mine_projects.xlsx"))
worksheet = workbook.add_worksheet()

headings = {"Company Name" : 0, "Project Name" : 0, "Lecture time" : 0, "Lab time" : 0, "Domain" : 0, 
    "Keywords" : 0, "Tools" : 0, "Citizenship" : 0, "Summary" : 0, "Description" : 0}
heading_column = 0
heading_format = workbook.add_format({'bold': True})
for element in headings:
    worksheet.write(0, heading_column, element, heading_format)
    heading_column += 1

row =  1

for k,v in url_dict.items():
    company_name = k.split("/")[-2]
    # Remember the max column name
    #print(headings["Company Name"],"before")
    #print(len(company_name))
    if len(company_name) > headings["Company Name"]:
        headings["Company Name"] = len(company_name)
    #print(len(company_name))
    #print(headings["Company Name"],"after")
    
    url_write(worksheet, row, 0, company_name, k)
    for project in v:
        project_name = project["url"].split("/")[-2]
        # Remember the max column name
        if len(project_name) > headings["Project Name"]:
            headings["Project Name"] = len(project_name)
        cell_write(worksheet, row, 1, project_name)
        column = 2
        for key,value in headings.items():
            if (key != "Company Name") and (key != "Project Name"): 
                cell_entry = project[key]
                # Remember the max column name
                if len(cell_entry) > headings[key]:
                    headings[key] = len(cell_entry)
                cell_write(worksheet, row, column, cell_entry)
                column += 1
        row += 1

# Set column length for heading to match with the longest project name
rows = row
for row in range(rows):
    worksheet.set_column(row, 0, headings["Company Name"])
workbook.close()
