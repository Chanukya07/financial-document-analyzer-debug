## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

from crewai.tools import tool
from crewai_tools import SerperDevTool
from langchain_community.document_loaders import PyPDFLoader

## Creating search tool
search_tool = SerperDevTool()

## Creating custom pdf reader tool
class FinancialDocumentTool():

    @tool("Read Data Tool")
    def read_data_tool(path: str):
        """Tool to read data from a pdf file from a path

        Args:
            path (str): Path of the pdf file.

        Returns:
            str: Full Financial Document file
        """
        try:
            loader = PyPDFLoader(path)
            docs = loader.load()
            
            full_report = ""
            for data in docs:
                # Clean and format the financial document data
                content = data.page_content
                
                # Remove extra whitespaces and format properly
                while "\n\n" in content:
                    content = content.replace("\n\n", "\n")

                full_report += content + "\n"

            return full_report
        except Exception as e:
            return f"Error reading PDF file: {str(e)}"

## Creating Investment Analysis Tool
class InvestmentTool:
    @tool("Analyze Investment Tool")
    def analyze_investment_tool(financial_document_data):
        """Tool to analyze investment opportunities from financial data"""
        # Process and analyze the financial document data
        processed_data = financial_document_data
        
        # Clean up the data format
        i = 0
        while i < len(processed_data):
            if processed_data[i:i+2] == "  ":  # Remove double spaces
                processed_data = processed_data[:i] + processed_data[i+1:]
            else:
                i += 1
                
        # TODO: Implement investment analysis logic here
        return "Investment analysis functionality to be implemented"

## Creating Risk Assessment Tool
class RiskTool:
    @tool("Create Risk Assessment Tool")
    def create_risk_assessment_tool(financial_document_data):
        """Tool to assess risks from financial data"""
        # TODO: Implement risk assessment logic here
        return "Risk assessment functionality to be implemented"
