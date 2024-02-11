# Description: This file contains all the configuration parameters for the project
import os

# api keys
oepnai_api_key = os.environ.get('OPENAI_API_KEY')
crunchbase_api_key = os.environ.get('CRUNCHBASE_API_KEY')
anymail_finder_api_key = os.environ.get('ANYMAIL_FINDER_API_KEY')

# login credentials
username = os.environ.get('LINKEDIN_USERNAME')
password = os.environ.get('LINKEDIN_PASSWORD')

# search parameters
start=1  # start page
end=1 # end page

# search parameters for linkedin person job title
investment_role_keywords = [
    # Leadership Positions
    "partner",
    "managing director",
    "principal",
    "chief",
    "director",
    "head of",
    "vp of",
    "executive",
    
    # Investment-Related Titles
    "investor",
    "investment manager",
    "investment analyst",
    "venture capitalist",
    "private equity",
    
    # Decision-Making Abilities
    "decision-maker",
    "investment authority",
    "investment decision-maker",
    "investment strategist",
    "investment leader",
    
    # General Business Titles
    "founder",
    "ceo",
    "owner",
    "co-founder",
]


focus_area_keywords = [
    # Open Source
    "open source",
    "contributor to open source projects",
    "open-source advocate",
    "GitHub contributor",
    "open source software development",
    
    # Cloud Infrastructure
    "cloud computing",
    "cloud infrastructure",
    "AWS",
    "Amazon Web Services",
    "Azure",
    "Google Cloud Platform",
    "cloud architecture",
    
    # Developer Tooling
    "developer tools",
    "software development tools",
    "DevOps",
    "continuous integration",
    "continuous deployment",
    "version control",
    
    # General Technology
    "technology enthusiast",
    "software engineering",
    "software development",
    "tech innovation",
    'developer tooling'
    'developer tools'
]


# file names
crunchbase_data_file = 'investors-23-01-2024(1).csv' # input file
employee_data_file = 'employee_details.csv' # output file - intermediate
focus_area_employee_file = 'focus_area_employee_details.csv' # output file - intermediate 2
final_output_file = 'final_output.csv' # output file - final

# prompt template for llm
prompt_template = """ 

    Given the linkedin information about a person, analyze the information to determine their key interest topics or focus areas. The data includes columns such as "Name," "LinkedIn URL," "Current Job," "About,", make sure the final output has to be just one single valid json dictonay without any notes and explanations,
    Your task is to extract insights into the user's interests by considering the following:

    1. Utilize the "About" section to identify any explicit mentions of their interests, skills, or personal preferences.
    2. Examine the current job description for clues about their professional focus areas.

    linkedin_information: ```{linkedin_information}```
    \n

    Make sure the final output has to be just one single valid json dictonay without any notes and explanations,like below format:
    1. 
    {format_instructions}
 """