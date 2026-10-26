
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

''' SEQUENTIAL CHAIN '''

prompt1 = PromptTemplate(
    template="Generate detailed reports on the topic: {topic}.",
    input_variables=["topic"],
)

prompt2 = PromptTemplate(
    template="Generate a summary of the following report: {report}.",
    input_variables=["report"],
)

model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    max_tokens=1000
)

parser = StrOutputParser()
chain = prompt1 | model | parser | prompt2 | model | parser
result = chain.invoke({"topic": "Unemployment trends in the tech industry over the past decade"})

print("Result:\n", result)
chain.get_graph().print_ascii()