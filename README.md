# Project Documentation

## Project Title: Employee Information Fetcher

This project is designed to fetch and analyze employee information from various organizations. It uses a multi-step process to gather data, analyze it, and filter results based on specific criteria.

### Overview

The project works as follows:

1. Fetches LinkedIn URLs of organizations from the Crunchbase API.
2. Extracts all employee profile URLs from the company's LinkedIn page.
3. Fetches information such as name, job role, and 'About Us' section from each employee's LinkedIn profile.
4. Uses OpenAI to analyze the employee's focus areas and interests.
5. Filters employees who are potential investors or have job roles related to investment, as specified in a configuration file.
6. Uses AnyMail Finder API to find the email of each employee.

### Requirements

To use this project, you need:

- An OpenAI API key
- A Crunchbase API key (free tier)
- A LinkedIn account
- An AnyMail Finder API key
- A .csv input file containing organization names or Crunchbase profile URLs

### Purpose

The main goal of this project is to identify employees who are potential investors or have an interest in investment. This is achieved by analyzing their LinkedIn profiles and their job roles. The results can be used for various purposes, such as targeted marketing, recruitment, or investment sourcing.

### How to Use

To use this project, you need to provide a configuration file that specifies the criteria for filtering employees. The criteria can include job roles, interests, and other relevant factors. The project will fetch and analyze employee data based on these criteria and provide a list of potential investors or employees interested in investment.

Please note that this project is strictly for software development purposes and should be used in compliance with LinkedIn's terms of service and privacy policy.

## Function: match_focus_areas

This function reads a CSV file into a DataFrame and processes each row within a specified range. It checks if any of the person's focus areas match the focus_area_keywords. If a match is found, it converts the dictionary to a DataFrame and appends it to the 'focus_area_employee_file.csv' file.

### Parameters:

- `file_path`: The path to the CSV file to be read.
- `focus_area_keywords`: The keywords to match against the person's focus areas.
- `start` (optional): The starting index of the range of rows to process. If not provided, the function will start from the first row.
- `end` (optional): The ending index of the range of rows to process. If not provided, the function will process up to the last row.

### Usage:

If you want to process all rows, you can call the function without the start and end parameters:

```python
match_focus_areas('employee_details.csv', investment_role_keywords)
```

If you want to process a specific range of rows, you can provide the start and end parameters:

```python
match_focus_areas('employee_details.csv', investment_role_keywords, 0, 10)
```

If you want to process a single row, you can provide the same number for the start and end parameters:

```python
match_focus_areas('employee_details.csv', investment_role_keywords, 1, 1)
```

In this case, it will process the first row of the DataFrame.

---

You can add this to your README file to provide documentation for the `match_focus_areas` function.