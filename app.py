import streamlit as st
from pathlib import Path
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from sqlalchemy import create_engine
import sqlite3
from langchain_groq import ChatGroq
import psycopg2

st.set_page_config(page_title="LangChain: Chat with SQL DB", page_icon=":parrot:")
st.title("LangChain: Chat with SQL DB :parrot:")

LOCALDB = "USE_LOCALDB"
POSTGRESDB = "USE_POSTGRESDB"

radio_choice = st.sidebar.radio(label="Select Database to chat with", options=['SQlite3 Local Database', 'Postgres Database'])

if radio_choice == 'Postgres Database':
    db_uri = POSTGRESDB
    postgres_host = st.sidebar.text_input("Postgres Host", value="localhost")
    postgres_port = st.sidebar.text_input("Postgres Port", value="5432")
    postgres_user = st.sidebar.text_input("Postgres User", value="postgres")
    postgres_password = st.sidebar.text_input("Postgres Password", type="password")
    postgres_db = st.sidebar.text_input("Postgres Database", value="postgres")
else:
    db_uri = LOCALDB

api_key = st.sidebar.text_input("Groq API Key", type="password", placeholder="Enter your Groq API key")

if not db_uri:
    st.info("Please enter the datbase information and uri.")
if not api_key:
    st.info("Please enter your Groq API key.")

## LLM model

llm = ChatGroq(groq_api_key=api_key, model="llama-3.3-70b-versatile", streaming=True)

st.cache_resource(ttl="2h")
def configure_db(db_uri, postgres_host=None, postgres_port=None, postgres_user=None, postgres_password=None, postgres_db=None):
    if db_uri == LOCALDB:
        # Connect to SQLite database
        dbfilepath=(Path(__file__).parent/"student.db").absolute()
        creator = lambda: sqlite3.connect(f"file:{dbfilepath}?mode=ro", uri=True)
        return SQLDatabase(create_engine("sqlite:///", creator=creator))
    elif db_uri == POSTGRESDB:
        # Connect to Postgres database
        if not all([postgres_host, postgres_port, postgres_user, postgres_password, postgres_db]):
            st.error("Please provide all Postgres connection details.")
            return None
        engine = create_engine(f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}")
        return SQLDatabase(engine)
    
if db_uri == POSTGRESDB:
    db = configure_db(db_uri, postgres_host, postgres_port, postgres_user, postgres_password, postgres_db)
else:
    db = configure_db(db_uri)

if db is None:
    st.error("Could not connect to the database. Please check your credentials and try again.")
    st.stop()

## SQL Toolkit

toolkit = SQLDatabaseToolkit(db=db, llm=llm)

agent = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

if "messages" not in st.session_state or st.sidebar.button("Clear message history"):
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

user_query = st.chat_input(placeholder="Ask anything from the database: e.g. What are the tables in this database?")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        streamlit_callback = StreamlitCallbackHandler(st.container())
        response = agent.run(user_query,callbacks=[streamlit_callback])
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)