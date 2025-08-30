# sql_agents.py
import sqlite3 # For SQLite connection
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


# ----------------------------
# step 1: Connect to NorthWind DB
# ----------------------------
db = SQLDatabase.from_uri("sqlite:///northwind.sqlite")

# Initialize LLM
OPENAI_API_KEY="your_openai_api_key_heresk-proj-pciaipanacyxnxgAPdu5EqvARqZdt6ThS4UOXkYP0JCdjaokwi6_etCRBUm2JdoNtiL0wttC4aT3BlbkFJ3Pb_6jUUvaPTjUyemjvJh3BHaBIxCkAnWlUeJ49Yexal1qhpoYWYLBDeZ4743rMdyYCHHlcuEA"
llm = ChatOpenAI(temperature=0, model="gpt-4", openai_api_key=OPENAI_API_KEY)


# ----------------------------
# step 2: Create Agent 1
# ----------------------------
sql_agent= create_sql_agent(llm ,db , verbose=True)

# Example query
query="Get the top 5 customers by total order amount."
response = sql_agent.run(query)
print(response)

# ----------------------------
# step 3: Create NL-to-SQL Agent 2
# ----------------------------
schema= db.get_table_info()

prompt_template = PromptTemplate(
    input_vsriables =["schema", "question"],
    template="""
You are an expert SQL agent. Given the following database schema:
{schema}
Convert the following natural language into a SQL query:
{question}
    """
)

nl_to_sql= LLMChain(llm=llm ,prompt=prompt_template)

def generate_sql(question:str) :
    sql = nl_to_sql.run({"schema":schema, "question":question})
    return sql

# Example query 
natural_language_query = generate_sql("List all products with a price greater than 20.")
print(natural_language_query)

# ----------------------------
# step 4: Integrated Pipeline
# ----------------------------
def ask_database(question: str):
    """Generate SQL from NL, execute it, and return results."""
    sql_query = generate_sql(question)
    print("Generated SQL:", sql_query)
    
    try:
        answer = db.run(sql_query)   # Agent 1 executes the SQL
        return answer
    except Exception as e:
        return f"Error executing SQL: {e}"
    
