import os
import pandas as pd
from typing import List
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from config import (oepnai_api_key, 
                    employee_data_file, 
                    focus_area_keywords, 
                    focus_area_employee_file, 
                    prompt_template, start, end)

# Define a Pydantic model for the PersonProfile
class PersonProfile(BaseModel):
    vc_firm_name: str = Field(description="The name of the VC firm")
    employee_name: str = Field(description="The name of the person")
    employee_title: str = Field(description="The title of the person")
    focus_area: List[str] = Field(description="a list of topics that may interest the person")

    def to_dict(self):
        return {
            "VC Firm Name": self.vc_firm_name,
            "Employee Name": self.employee_name,
            "Employee_Title": self.employee_title,
            "Focus Area": self.focus_area,
            
        }

# Define a function to match the focus areas of a person
def match_focus_areas(result):
    # Get the focus areas of the person
    person_focus_area = result["Focus Area"]

    # Check if any of the person's focus areas match the focus_area_keywords
    if any(focus_area in focus_area_keywords for focus_area in person_focus_area):
    # If a match is found, append the row to the matching_df DataFrame
        print('match found')
        result_df = pd.DataFrame([result])
        if os.path.isfile(focus_area_employee_file):
        # Write the matching_df DataFrame to a new CSV file
            result_df.to_csv(focus_area_employee_file, mode='a', header=False, index=False)
        else:
            result_df.to_csv(focus_area_employee_file, mode='w', index=False)
    else:
        print("Not Match")

# Define a function to run the LLM
def focus_area(file_path, start, end):
    try: 
        # Read the CSV file into a DataFrame
        person_parser=PydanticOutputParser(pydantic_object=PersonProfile)
        linkedIn_prompt_template = PromptTemplate(
        template=prompt_template,
        input_variables = ["linkedin_information"],
        partial_variables={
            "format_instructions": person_parser.get_format_instructions()
        }
        )
        df = pd.read_csv(file_path)
        # If start and end are not provided, process all rows
        if start is None or end is None:
            start, end = 0, len(df)
        else:
            start = start - 1
        # llm 
        llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", api_key=oepnai_api_key)
        chain = LLMChain(llm=llm, prompt=linkedIn_prompt_template)

        # Iterate over each row in the DataFrame within the specified range
        for index, row in df.iloc[start:end].iterrows():
            # Convert the row to a dictionary
            linkedin_data = row.to_dict()
            results = chain.run(linkedin_information = linkedin_data)
            finalresult = person_parser.parse(results)
            formattedResult = finalresult.to_dict()
            match_focus_areas(formattedResult)
        # return formattedResult

    except FileNotFoundError:
        print(f"Error: File {file_path} not found")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        print("Done")

# focus_area(employee_data_file, start=start, end=end)