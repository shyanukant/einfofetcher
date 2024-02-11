import asyncio
from employee_details import lookup_employee_details
from analysis_linkedIn_page import focus_area
from config import employee_data_file, start, end


asyncio.run(lookup_employee_details(start=start, end=end))
focus_area(employee_data_file, start=start, end=end)