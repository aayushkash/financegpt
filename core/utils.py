import yaml
import re

# Function to load API keys from config/config.yaml
def load_config():
    with open('config/config.yaml', 'r') as file:
        return yaml.safe_load(file)
    

# Helper functions to parse the recommendation
def get_recommendation(result):
    return result.replace("## Recommendation:", "");


def extract_recommendation(text):

    recommendation = get_recommendation(text)
    """
    Extracts the recommendation (BUY, SELL, HOLD) from a formatted string using switch-case logic.
    Looks for '## Recommendation: Hold', '## Recommendation: Buy', or '## Recommendation: Sell' (case-insensitive).
    Returns:
    - str: extracted recommendation ('BUY', 'SELL', 'HOLD') or 'NA' if not found
    """
    if "## Recommendation: Hold" in text:
        return "HOLD", recommendation
    elif "## Recommendation: Buy" in text:
        return "BUY", recommendation
    elif "## Recommendation: Sell" in text:
        return "SELL" , recommendation
    else:
        return "NA",recommendation

if __name__ == "__main__":
    tag = extract_recommendation("## Recommendation: Hold **Explanation:** Market is")
    print(f"Recommendation: " + {tag})