from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch,RunnableLambda
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Literal

load_dotenv()

''' CONDITIONAL CHAIN '''

model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    max_tokens=1000
)

parser = StrOutputParser()

class SentimentResponse(BaseModel):
    sentiment: Literal["positive", "negative"] = Field(..., description="The sentiment of the text.")

parser2 = PydanticOutputParser(pydantic_object=SentimentResponse)

prompt1 = PromptTemplate(
    template="Classify the sentiment of the following text as positive or negative: {feedback}. \n {format_instructions}",
    input_variables=["feedback"],
    partial_variables={"format_instructions": parser2.get_format_instructions()},
)

classification_chain = prompt1 | model | parser2

'''result = classification_chain.invoke({"feedback": "I love the new features in this product!"}).sentiment
print(result)'''



prompt2 = PromptTemplate(
    template="Generate an appropriate response to the positive feedback: {feedback}.", 
    input_variables=["feedback"],
)

prompt3 = PromptTemplate(
    template="Generate an appropriate response to the negative feedback: {feedback}.",
    input_variables=["feedback"],
)


branch_chain = RunnableBranch(
    (lambda x: x.sentiment == "positive", prompt2 | model | parser),
    (lambda x: x.sentiment == "negative", prompt3 | model | parser),
    RunnableLambda(lambda x: "Could not classify the sentiment of the feedback.")

)

chain = classification_chain | branch_chain

result = chain.invoke({"feedback": "I love the new features in this product!"})
print("Result:\n", result)
chain.get_graph().print_ascii()
