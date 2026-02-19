from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
from langchain_core.runnables import RunnableLambda

from prompts import *
from schemas import *

load_dotenv(".env")
KEY = os.environ.get("GEMINI_API_KEY")

try:
    llm1 = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
        google_api_key=KEY,
        max_tokens=None,
        timeout=None,
        max_retries=2, 
    ).with_structured_output(Schema1)

    llm2 = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
        google_api_key=KEY,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    ).with_structured_output(Schema2)

    explaination_prompt = PromptTemplate(
        template=prompt1, input_variables=["query"]
    )

    summary_prompt = PromptTemplate(
        template=prompt2, input_variables=["title", "headline", "content"])

    def map_schema1_to_prompt2_input(schema1_obj: Schema1):
        return {"title": schema1_obj.title, "headline": schema1_obj.headline}

    # parser = StrOutputParser()

    # chain = explaination_prompt | llm1 | parser | summary_prompt | llm2 | parser

    # result = chain.invoke({"query": "Generative AI"})
    # print(result)
    # Build the chain properly without StrOutputParser

    # First stage: generate title and headline
    stage1 = explaination_prompt | llm1  # returns Schema1 object

    # Second stage: feed title/headline into prompt2 -> llm2

    stage2 = RunnableLambda(map_schema1_to_prompt2_input) | summary_prompt | llm2
 
    chain = stage1 | stage2

    # Run the chain
    result = chain.invoke({"query": "Generative AI"})
    print(result)

except Exception as e:
    print(" -----> ", e)
