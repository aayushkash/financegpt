import os
import google.generativeai as genai
from dotenv import load_dotenv

def build_gmail_search_query(natural_question: str) -> str:
    """
    Generates a simulated Gmail search query based on a natural language question.

    In a real-world application, this function would leverage the Gemini API to
    intelligently craft a precise Gmail API search query based on the user's
    natural language input, considering dates, senders, and keywords.
    For this example, it returns a hardcoded, illustrative query.

    Args:
        natural_question (str): The user's query in natural language.

    Returns:
        str: A simulated Gmail search query string.
    """
    # This part would typically use a Gemini model to convert natural language
    # into a precise Gmail search query syntax.
    # For this example, we'll return a hardcoded, relevant query.

    # model = genai.GenerativeModel("gemini-1.5-flash")
    # system_prompt = f"""
    # You are an AI expert at writing Gmail search queries.
    # Convert the following user question into a Gmail search query syntax.
    # Only output the Gmail query string. Do not explain anything.

    # IMPORTANT RULES:
    # 1. For "this month" queries in May 2025, ALWAYS use exactly:
    #    after:2025/05/01 before:2025/05/31
    # 2. Include the ENTIRE day in date ranges
    # 3. Never skip any days in the range

    # Examples:
    # "Zomato orders this month" -> "Zomato after:2025/05/01 before:2025/05/31"
    # "Flight orders this month" -> "flight after:2025/05/01 before:2025/05/31"
    # "IRCTC last week" -> "IRCTC after:2025/05/10 before:2025/05/17"
    # "OTP from Axis bank yesterday" -> "OTP Axis after:2025/05/17 before:2025/05/18"
    # "Job updates" -> "job updates after:2025/05/17 before:2025/05/18"


    # User Query:
    # {natural_question}
    # """
    # response = model.generate_content(system_prompt)
    # return response.text.strip().strip('"')

    # Simulated output for "financial data for BSE Trades, Investments and spends for this month"
    # This query would target emails from brokerage firms, investment platforms, and transaction alerts.
    return 'from:zerodha.com OR from:groww.in OR from:icicidirect.com OR subject:"BSE Trade" OR subject:"Investment Update" OR subject:"Payment Confirmation" after:2025/05/01 before:2025/05/31'

def summarize_financial_data(user_query: str, email_snippets: list[str]) -> str:
    """
    Analyzes a list of email snippets using the Gemini API to extract and summarize
    financial transactions (BSE trades, investments, and spends).

    Args:
        user_query (str): The original natural language question from the user.
        email_snippets (list[str]): A list of short text summaries (snippets) from emails.

    Returns:
        str: A structured summary of the financial data extracted by the Gemini model.
    """
    # Initialize the GenerativeModel with the desired model (gemini-1.5-flash is good for speed)
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Combine all email snippets into a single string for the prompt
    combined_emails = "\n\n---EMAIL_SEPARATOR---\n\n".join(email_snippets)

    # Craft a detailed prompt for the Gemini model to ensure accurate extraction and formatting
    prompt = f"""
    You are a highly analytical financial assistant designed to process email snippets and extract specific financial details.
    Your task is to identify and summarize all **BSE Trades**, **Investments**, and **Spends** from the provided email content.
    For each identified item, clearly state the **date**, **type** (BSE Trade, Investment, or Spend), and the **amount**.
    After listing all relevant items by category, provide a **total amount for 'Spends'**.

    Pay close attention to dates to ensure all transactions within the specified period are included.
    If an amount is in INR (Indian Rupees), specify it as '₹'.

    EMAIL SNIPPETS:
    {combined_emails}

    USER QUESTION:
    {user_query}

    Instructions for your output:
    - Start with a clear heading for each category (BSE Trades, Investments, Spends).
    - List each transaction with its date and amount.
    - Calculate and state the 'Total Spends' at the end.
    - If a category has no items, state "No [Category] found."
    - Be precise and only use information explicitly stated in the snippets.
    """

    # Generate content using the Gemini model
    response = model.generate_content(prompt)

    # Return the structured text response from the model
    return response.text.strip()

#---------------------------------------------------------------------------------------------------

def main():
    """
    Main function to orchestrate the financial data extraction process.
    It loads the API key, generates a Gmail search query, simulates email retrieval,
    and then uses Gemini to summarize the financial data.
    """
    print("🚀 Initializing financial data agent...\n")

    # Load environment variables from .env file
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    # Check if the API key is loaded correctly
    if not api_key:
        print("❌ Error: GEMINI_API_KEY not found in your .env file.")
        print("Please create a .env file in the same directory and add your API key:")
        print("GEMINI_API_KEY=YOUR_ACTUAL_GEMINI_API_KEY")
        return

    # Configure the Google Gemini API with the loaded key
    genai.configure(api_key=api_key)
    print("✅ Gemini API configured successfully.\n")

    # Define the user's natural language query for financial data
    user_question = "financial data for BSE Trades, Investments and spends for this month"
    print(f"User's query: '{user_question}'\n")

    # Step 1: Generate a simulated Gmail search query based on the user's question
    # In a real application, this would involve a call to a Gemini model trained
    # to convert natural language to Gmail search syntax.
    print("🔍 Generating simulated Gmail search query...")
    gmail_search_query = build_gmail_search_query(user_question)
    print(f"Simulated Gmail Query: '{gmail_search_query}'\n")

    # Step 2: Simulate fetching email snippets from Gmail
    # In a live system, you would use the Google Gmail API to fetch emails
    # matching the 'gmail_search_query'. For this example, we use predefined snippets
    # that are typical of financial communications.
    print("📧 Simulating retrieval of email snippets from Gmail...")
    sample_email_snippets = [
        "Dear Customer, your equity trade for 15 shares of Reliance Industries Ltd. (BSE: 500325) valued at ₹37,500.00 was executed on 2025-05-12. Transaction ID: RIL12345.",
        "Your mutual fund investment of ₹7,000.00 into Axis Bluechip Fund was successfully processed on May 05, 2025. Ref: MF7890.",
        "A debit of ₹550.00 for your Swiggy order (ID: SWG9876) was made on 2025-05-03. Enjoy your meal!",
        "Your monthly SIP of ₹10,000.00 for ICICI Prudential Long Term Equity Fund was debited on 2025-05-07. Thank you for your continued investment.",
        "Online purchase from Flipkart: Order FPKL6789. Amount: ₹3,200.00. Date: May 18, 2025.",
        "Your payment of ₹250.00 to Google Pay for a taxi ride was confirmed on 2025-05-22. Ref: TXI456.",
        "BSE delivery trade confirmation: You bought 5 shares of Tata Motors Ltd. (BSE: 500570) for ₹3,000.00 on 2025-05-25. Order#: TTM001.",
        "Electricity Bill Payment of ₹1,800.00 processed on May 28, 2025. Account: 123456789.",
        "Invested ₹2,500.00 in a new bond fund via your brokerage account on May 30, 2025. Confirmation ID: BND876."
    ]
    print(f"Retrieved {len(sample_email_snippets)} sample email snippets.\n")

    # Step 3: Use Gemini to summarize the financial data from the snippets
    print("✨ Analyzing and summarizing financial data using Gemini...\n")
    financial_summary = summarize_financial_data(user_question, sample_email_snippets)

    # Step 4: Print the final summarized financial data
    print("--- 💰 FINANCIAL DATA SUMMARY (MAY 2025) 💰 ---")
    print(financial_summary)
    print("-------------------------------------------------")

# Ensure the main function runs when the script is executed
if __name__ == "__main__":
    main()