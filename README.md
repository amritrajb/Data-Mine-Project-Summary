# Data-Mine-Project-Summary

The Purdue Data Mine is an excellent program helping students to get real-world experience in the data science domain by working on projects with various companies and corporate partners. As a Data Mine student, I wanted a way to summarize all the possible projects to choose from in one file, so I could then eliminate ones that I was less interested in or didnt fit my schedule, and highlight my top choices as well. i figured that putting all the compnay and project data into one file would help with choosing the project that best fit my interests.

This python tool that scrapes the Purdue Data Mine website: https://projects.the-examples-book.com/companies/. It then generates an Excel File which summarizes all the companies and projects for the current year. The tool uses the BeautifulSoup Python library to extract the web contents and XLSXWriter to write to an excel file.

To use the tool, simply run the dm_scraping.py 
