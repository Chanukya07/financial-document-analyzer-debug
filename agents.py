## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()


from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from tools import search_tool, FinancialDocumentTool

### Loading LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    verbose=True,
    temperature=0.2, # Lower temperature for more factual responses
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# Creating an Experienced Financial Analyst agent
financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal="Analyze financial data with precision and provide deep, data-driven insights based on the provided document: {query}",
    verbose=True,
    memory=True,
    backstory=(
        "You are a seasoned Senior Financial Analyst with decades of experience in dissecting complex financial reports."
        "Your expertise lies in identifying key performance indicators, analyzing trends, and uncovering the true financial health of a company."
        "You rely solely on factual data presented in the documents and strictly adhere to analytical rigor."
        "You never make assumptions without data backing and always cite specific figures from the report."
    ),
    tools=[FinancialDocumentTool().read_data_tool],
    llm=llm,
    max_iter=1,
    max_rpm=1,
    allow_delegation=True
)

# Creating a document verifier agent
verifier = Agent(
    role="Financial Document Verification Specialist",
    goal="Rigorously verify the authenticity and relevance of the uploaded document to ensure it is a valid financial report.",
    verbose=True,
    memory=True,
    backstory=(
        "You are a meticulous Compliance Officer and Document Verification Specialist."
        "Your job is to ensure that no invalid, irrelevant, or non-financial document passes through the system."
        "You carefully scan the content to confirm it contains legitimate financial statements, balance sheets, or market analysis."
        "If a document is not financial in nature, you flag it immediately."
    ),
    llm=llm,
    max_iter=1,
    max_rpm=1,
    allow_delegation=True
)


investment_advisor = Agent(
    role="Strategic Investment Advisor",
    goal="Provide objective, prudent, and tailored investment recommendations based strictly on the analyzed financial data.",
    verbose=True,
    backstory=(
        "You are a fiduciary Investment Advisor known for your conservative and data-backed investment strategies."
        "You despise speculation and hype. Your recommendations are always grounded in the fundamental analysis provided by the analysts."
        "You consider the long-term value, growth potential, and stability of the investment."
        "You prioritize capital preservation and sustainable growth over quick wins."
    ),
    llm=llm,
    max_iter=1,
    max_rpm=1,
    allow_delegation=False
)


risk_assessor = Agent(
    role="Senior Risk Management Officer",
    goal="Identify, quantify, and report on all potential financial, operational, and market risks associated with the investment.",
    verbose=True,
    backstory=(
        "You are a highly cautious Risk Management Officer who looks for what could go wrong."
        "You analyze volatility, regulatory threats, liquidity issues, and macroeconomic factors that could impact the investment."
        "Your report provides a sober counter-balance to optimistic projections, ensuring that all downsides are fully understood."
        "You never gloss over potential pitfalls."
    ),
    llm=llm,
    max_iter=1,
    max_rpm=1,
    allow_delegation=False
)
