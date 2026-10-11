import os
from dotenv import load_dotenv
from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langserve import add_routes

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

model = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=os.environ.get("GROQ_API_KEY"),
)

generic_template = "Translate the sentense from englishg to {language}."

prompt = ChatPromptTemplate.from_messages([
    ("system", generic_template),
    ("user", "{text}")
    ])

parser = StrOutputParser()

#create chain
chain = prompt | model | parser

#App Definition
app = FastAPI(
    title="LangServe Example",
    description="This is an example of how to use LangServe with a Groq model.",
    version="0.1.0"
)

add_routes(
    app,
    chain,
    path="/translate"
  
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)




