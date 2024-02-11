import json
import asyncio
import pandas as pd 
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from datautils import lookup_linkedin_url, build_dataset
from config import ( username, 
                    password, 
                    investment_role_keywords, 
                    crunchbase_data_file, 
                    employee_data_file, 
                    start, end
                    )

# Extract the profile about section
def extract_profile_info(html_content):
    # Parse the HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    # Extract the text from the About section
    about_section = soup.find('div', {'id': 'about'})
    if about_section is None:
        return None
    next_section = about_section.find_next('div', {'class': 'pv-shared-text-with-see-more'})
    about_text = next_section.find('span', {'aria-hidden': 'true'}).text.strip()
    return about_text

# login to linkedin
async def login(page, context, url):
    # load cookies
    try:
        with open('cookies.json', 'r') as f:
            cookies = json.load(f)
        await context.add_cookies(cookies)
    except FileNotFoundError:
        pass

    await page.goto(url, timeout=0)

    # Check if the 'me' button is present
    me_button = await page.query_selector('#ember13')

    # If the 'me' button is not present, log in
    if not me_button:
        # Check if the sign-in button or link is present
        sign_in_button = await page.query_selector('button.sign-in-modal__outlet-btn.cursor-pointer.btn-mbtn-primary')
        sign_in_link = await page.query_selector('p.main__sign-in-container a.main__sign-in-link')
        # If the sign-in button is present, click on it
        if sign_in_button:
            await page.wait_for_timeout(2000)
            await sign_in_button.click()
            await page.wait_for_timeout(2000)
        # If the sign-in link is present, click on it
        elif sign_in_link:
            await page.wait_for_timeout(2000)
            await sign_in_link.click()
            await page.wait_for_timeout(2000)
        # Fill in the login credentials
        await page.fill('input[id="username"]', username)
        await page.fill('input[id="password"]', password)

        # Submit the login form
        await page.click('button[type="submit"]', timeout=0)

        # save cookies
        cookies = await context.cookies()
        with open('cookies.json', 'w') as f:
            json.dump(cookies, f)

# get employee profile details
async def employee_profile_details(context, df, limit=1):
    counter = 0
    new_page = await context.new_page()
    for url in df['Employee URL']:
        try:
            await new_page.goto(url, timeout=0)
            # Get the HTML content of the page
            html_content = await new_page.content()
            # Extract profile about
            profile_about = extract_profile_info(html_content)
        
            df.loc[df['Employee URL'] == url, 'Employee About'] = ''.join(profile_about)
            print('success')
        except Exception as e:
            print(f"Error getting about details: {str(e)}")
            
        counter += 1
        if limit and counter >= limit:
            break
    df.to_csv(employee_data_file, index=False)
    print("Success")
    await asyncio.sleep(10)

# get employee pofiles
async def get_employee_profiles(page, vc_firm_name):
    employee_details = []
    start_index = 0
    while True:
            employee_list = await page.query_selector_all('.org-people-profile-card__profile-info')
            # Extract employee details from the current page
            for i in range(start_index, len(employee_list)):
                employee = employee_list[i]
                job_title_element = await employee.query_selector('.artdeco-entity-lockup__subtitle')
                job_title = await job_title_element.inner_text() if     job_title_element else None
            
                if any(role in job_title.lower() for role in investment_role_keywords):
                    name_element = await employee.query_selector('.org-people-profile-card__profile-title')
                    name = await name_element.inner_text() if name_element else None
                    link_element = await employee.query_selector('.app-aware-link')
                    if name and link_element :
                        # Get the href attribute of the a element
                            link_url = await link_element.get_attribute('href')
                            # If the href attribute exists
                            if link_url:
                                # Add the URL to the list
                                link = link_url.split('?')[0]
                                
                            else :pass
                    else :pass
                else :continue
                print(f"extract details of {name}")
                employee_detail = {'VC Firm Name': vc_firm_name, 'Employee Name':   name, 'Employee Title': job_title, "Employee URL" : link, }
                employee_details.append(employee_detail) 
            start_index = len(employee_list)
            show_more_button = await page.query_selector('.artdeco-button.artdeco-button--muted.artdeco-button--1.artdeco-button--full.artdeco-button--secondary.ember-view.scaffold-finite-scroll__load-button')
            if show_more_button:
                try:
                    await page.wait_for_timeout(2000)
                    await show_more_button.click()
                    await page.wait_for_timeout(4000)
                except Exception as e:
                    print(f"Error: {str(e)}")
                    break
            else:
                print("No more results to load")
                break
    return employee_details

# main function
async def lookup_employee_details(start, end):
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        context = await browser.new_context()
        # Read the CSV file
        df = pd.read_csv(crunchbase_data_file)
        for profile_url in df['Organization/Person Name URL']:
            # Extract the organization permalink from the profile URL
            organization_permalink = profile_url.split('/')[-1]
            # Create a new page
            url, vm_firm_name = lookup_linkedin_url(organization_permalink)
            page = await context.new_page()
            # url = 'https://www.linkedin.com/company/new-enterprise-associates/people'
            await login(page, context, url)
            employee_details = await get_employee_profiles(page, vm_firm_name)
            build_dataset(employee_details)
            if start!= None and end!=None and start!=end:
                start+=1
            elif start!= None and end!=None and start == end:
                break
        df2 = pd.read_csv(employee_data_file)
        await employee_profile_details(context, df2)
        await context.close()

# asyncio.run(main(start=start, end=end))