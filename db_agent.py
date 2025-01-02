import os

import streamlit as st
from dotenv import find_dotenv, load_dotenv
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
# from langchain_groq import ChatGroq
import pandas as pd


from sqlalchemy import create_engine
##############################
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabase

from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.utilities import SQLDatabase

#######################
### for local use
# model = ChatOpenAI( base_url = "http://localhost:1234/v1" , api_key="not needed" )

load_dotenv(find_dotenv())

openai_key = os.getenv('GROQ_API_KEY')
openai_key = st.secrets["GROQ_API_KEY"]
# model = ChatGroq(temperature=0.8, groq_api_key=openai_key, model_name="llama-3.1-70b-versatile")
model = ChatGroq(temperature=0.8, groq_api_key=openai_key, model_name="gemma2-9b-it")
# model = ChatGroq(temperature=0.8, groq_api_key=openai_key, model_name="llama-3.1-70b-versatile")

df = pd.read_csv('salaries_2023.csv').fillna(value=0)

# create the DB from SQL
database_file_path = "./db/salary.db"
###### make an engine

engine = create_engine(f"sqlite:///{database_file_path}")
file_url = "./salaries_2023.csv"
os.makedirs(os.path.dirname(database_file_path),exist_ok=True)
df.to_sql("salary_2023" , con=engine ,if_exists= "replace" , index=False)
# print(f"Database Created !! {df.head(3)}")

db = SQLDatabase.from_uri(f"sqlite:///{database_file_path}")
toolkit = SQLDatabaseToolkit(db=db , llm=model)

MSSQL_AGENT_PREFIX = """

You are an agent designed to interact with a SQL database.
## Instructions:
- Given an input question, create a syntactically correct {dialect} query
to run, then look at the results of the query and return the answer.
- Unless the user specifies a specific number of examples they wish to
obtain, **ALWAYS** limit your query to at most {top_k} results.


- You MUST double check your query before executing it.If you get an error
while executing a query,rewrite the query and try again.
- DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.)
to the database.

- Your response should be in Markdown. However, **when running  a SQL Query
in "Action Input", do not include the markdown backticks**.
Those are only for formatting the response, not for executing the command.

- If the question does not seem related to the database, just return
"I don\'t know" as the answer.

- as part of your final answer, please include the SQL query you used in json format or code format


"""



MSSQL_AGENT_FORMAT_INSTRUCTIONS = """

## Use the following format:

Question: the input question you must answer.
Thought: you should always think about what to do.
Action: the action to take, should be one of [{tool_names}].
Action Input: the input to the action.
Observation: the result of the action.
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer.
Final Answer: the final answer to the original input question.

Example of Final Answer:
<=== Beginning of example

Action: query_sql_db
Action Input: 
SELECT TOP (10) [base_salary], [grade] 
FROM salaries_2023

WHERE state = 'Division'

Observation:
[(27437.0,), (27088.0,), (26762.0,), (26521.0,), (26472.0,), (26421.0,), (26408.0,)]
Thought:I now know the final answer
Final Answer: There were 27437 workers making 100,000.

Explanation:
I queried the `xyz` table for the `salary` column where the department
is 'IGM' and the date starts with '2020'. The query returned a list of tuples
with the bazse salary for each day in 2020. To answer the question,
I took the sum of all the salaries in the list, which is 27437.
I used the following query

```sql
SELECT [salary] FROM xyztable WHERE department = 'IGM' AND date LIKE '2020%'"
```
===> End of Example

"""


qus = '''
How many employee are in ABS 85 Administrative  Division and what is their average salary?
'''
sql_agent = create_sql_agent(
    prefix=MSSQL_AGENT_PREFIX,
    format_instructions=MSSQL_AGENT_FORMAT_INSTRUCTIONS,
    llm=model,
    toolkit=toolkit,
    top_k=30,
    verbose=True,
)


# res = sql_agent.invoke( qus )
# print(res)


st.title("SQL Query AI Agent")

question = st.text_input("Enter your query:")

if st.button("Run Query"):
    if question:
        res = sql_agent.invoke(question)

        st.markdown(res["output"])
else:
    st.error("Please enter a query.")
