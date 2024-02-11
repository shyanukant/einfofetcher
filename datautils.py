import os
import requests
import pandas as pd
from config import crunchbase_api_key, employee_data_file, anymail_finder_api_key

# Get the LinkedIn URL for an organization
def lookup_linkedin_url(organization_permalink):
    # Send a GET request to the Crunchbase API
    response = requests.get(
        f"https://api.crunchbase.com/api/v4/entities/organizations/{organization_permalink}?field_ids=linkedin,website",
        params={'user_key': crunchbase_api_key}
        )
    # Parse the JSON response
    data = response.json()
    # Get the LinkedIn URL
    linkedin_url = data['properties']['linkedin']['value'] + '/people'
    vm_firm_name = data['properties']['identifier']['value']
    print(f"Organization LinkedIn Url : {linkedin_url}")
    return linkedin_url, vm_firm_name

# ceate employee details dataset
def build_dataset(employee_details):
    filename = employee_data_file
    employee_df = pd.DataFrame(employee_details)
    if os.path.isfile(filename):
        existing_df = pd.read_csv(filename)
        employee_df = pd.concat([existing_df, employee_df])
    employee_df.to_csv(filename, index=False)
    employee_df.drop_duplicates(inplace=True)
    print(f"Employee Details Successfully stored in {filename}")

# Define a function to login to LinkedIn
def find_email_address(name, company_name):
    # Use Anymail Finder to identify the email address
    response = requests.post(
    'https://api.anymailfinder.com/v5.0/search/person.json',
    params={'full_name':name, 'company': company_name},
    headers={'X-API-KEY': anymail_finder_api_key}
    )

    # Get the email address
    email_address = response.json()
    return email_address