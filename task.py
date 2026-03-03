## Importing libraries and files
from crewai import Task

from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from tools import search_tool, FinancialDocumentTool

## Creating a task to help solve user's query
analyze_financial_document = Task(
    description="Analyze the provided financial document in detail based on the user's query: {query}.\n\
Your task is to extract key financial metrics, performance indicators, and relevant data points directly from the document at {path}.\n\
Do not make assumptions or fabricate data. Stick strictly to what is presented in the text.\n\
Structure your analysis logically, covering revenue, expenses, profit margins, and any significant financial events mentioned.",

    expected_output="""A comprehensive financial analysis report including:
- Key financial highlights (Revenue, Net Income, EBITDA, etc.) with specific figures.
- Trend analysis based on the document's historical comparisons.
- Identification of major cost drivers and revenue streams.
- A neutral, data-driven summary of the company's financial health.
- No hallucinated data or external URLs.""",

    agent=financial_analyst,
    tools=[FinancialDocumentTool().read_data_tool],
    async_execution=False,
)

## Creating an investment analysis task
investment_analysis = Task(
    description="Based on the financial analysis provided, formulate a professional investment opinion.\n\
Evaluate the company's potential for growth, stability, and value generation.\n\
Consider the user's query: {query} to tailor the advice, but remain objective.\n\
Assess the strengths and weaknesses of the company as an investment opportunity using only the provided data.",

    expected_output="""A professional investment recommendation report:
- A clear 'Buy', 'Hold', or 'Sell' recommendation (or 'Neutral' if data is insufficient) with a solid rationale.
- Analysis of the company's competitive position and market outlook based on the document.
- Evaluation of valuation metrics if available (P/E, EPS, etc.).
- Strategic insights for potential investors.
- Professional tone, devoid of hype or speculative language.""",

    agent=investment_advisor,
    tools=[FinancialDocumentTool().read_data_tool],
    async_execution=False,
)

## Creating a risk assessment task
risk_assessment = Task(
    description="Conduct a thorough risk assessment based on the financial document and the analysis.\n\
Identify all financial, operational, market, and regulatory risks mentioned or implied in the report.\n\
Quantify the potential impact of these risks where possible.\n\
Provide a balanced view of the downside potential to ensure the user is fully informed of the risks.",

    expected_output="""A detailed risk assessment report:
- A categorized list of identified risks (e.g., Market Risk, Operational Risk, Liquidity Risk).
- Analysis of the severity and probability of each key risk factor.
- Evaluation of the company's risk mitigation strategies if mentioned.
- A final summary of the overall risk profile of the investment (Low, Medium, High).""",

    agent=risk_assessor,
    tools=[FinancialDocumentTool().read_data_tool],
    async_execution=False,
)

    
verification = Task(
    description="Verify that the uploaded file at {path} is a legitimate financial document.\n\
Scan the content for key financial statements (Balance Sheet, Income Statement, Cash Flow) or market analysis reports.\n\
If the document is unrelated to finance (e.g., a recipe, a novel, a random text), clearly state that it is invalid.\n\
Do not proceed with deep analysis if the document is not relevant.",

    expected_output="""A verification status report:
- Confirmation of whether the document is a valid financial report (Yes/No).
- A brief description of the document type (e.g., 'Q3 Earnings Report', 'Annual Report', 'Invalid Document').
- If invalid, a clear message explaining why the document cannot be analyzed.""",

    agent=verifier,
    tools=[FinancialDocumentTool().read_data_tool],
    async_execution=False
)
