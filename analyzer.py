"""from textblob import TextBlob
import pandas as pd
import re
import os

# Load threat keywords with path validation
try:
    keywords_path = os.path.join("data", "suspicious_words", "suspicious_social_media_keywords.csv")
    df_keywords = pd.read_csv(keywords_path)
    keyword_dict = df_keywords.groupby("Category")["Keyword"].apply(list).to_dict()
    THREAT_KEYWORDS = keyword_dict
except FileNotFoundError:
    raise FileNotFoundError(f"Keywords file not found at {os.path.abspath(keywords_path)}")
except Exception as e:
    raise RuntimeError(f"Error loading keywords: {str(e)}")

def analyze_tweets(username):
    print(f"🔍 Analyzing tweets for @{username}...")
    
    # Build CSV path
    csv_dir = os.path.join("data", "csv")
    csv_filename = f"{username}_tweets.csv"
    csv_path = os.path.join(csv_dir, csv_filename)
    
    # Verify CSV exists
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Tweet CSV not found at {os.path.abspath(csv_path)}")
    
    try:
        df = pd.read_csv(csv_path)
        
        # Ensure 'Text' column exists
        if 'Text' not in df.columns:
            raise ValueError("CSV file missing required 'Text' column")
            
        # Perform analysis
        df['Sentiment'] = df['Text'].apply(lambda x: TextBlob(str(x)).sentiment.polarity)
        df['Threats'] = df['Text'].apply(detect_threats)
        df['Threat_Score'] = df['Threats'].apply(score_threats)
        
        return df
        
    except pd.errors.EmptyDataError:
        raise ValueError(f"CSV file {csv_path} is empty")
    except Exception as e:
        raise RuntimeError(f"Analysis failed: {str(e)}")

def detect_threats(text):
    text = str(text).lower()
    threats = []
    for category, keywords in THREAT_KEYWORDS.items():
        found = [kw.lower() for kw in keywords if re.search(rf'\b{re.escape(kw)}\b', text)]
        if found:
            threats.append(f"{category}: {', '.join(found)}")
    return '|'.join(threats) if threats else None

def score_threats(threats):
    if not threats: 
        return 0
    return sum(1 for _ in threats.split('|')) * 2

"""

from textblob import TextBlob
import pandas as pd
import re
import os

# Load threat keywords first
try:
    keywords_path = os.path.join("data", "suspicious_words", "suspicious_social_media_keywords.csv")
    df_keywords = pd.read_csv(keywords_path)
    keyword_dict = df_keywords.groupby("Category")["Keyword"].apply(list).to_dict()
    THREAT_KEYWORDS = keyword_dict
except Exception as e:
    raise RuntimeError(f"Failed to load threat keywords: {str(e)}")

# Define helper functions BEFORE the main analysis function
def detect_threats(text):
    text = str(text).lower()
    threats = []
    for category, keywords in THREAT_KEYWORDS.items():
        found = [kw.lower() for kw in keywords if re.search(rf'\b{re.escape(kw)}\b', text)]
        if found:
            threats.append(f"{category}: {', '.join(found)}")
    return '|'.join(threats) if threats else None

def score_threats(threats):
    if not threats: 
        return 0
    return sum(1 for _ in threats.split('|')) * 2

# Main analysis function comes last
def analyze_tweets(username):
    print(f"🔍 Analyzing tweets for @{username}...")
    
    csv_path = os.path.join("data", "csv", f"{username}_tweets.csv")
    
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Tweet CSV not found at {os.path.abspath(csv_path)}")
    
    try:
        df = pd.read_csv(csv_path)
        
        if 'Text' not in df.columns:
            raise ValueError("CSV missing 'Text' column")
            
        df['Sentiment'] = df['Text'].apply(lambda x: TextBlob(str(x)).sentiment.polarity)
        df['Threats'] = df['Text'].apply(detect_threats)  # Now properly defined
        df['Threat_Score'] = df['Threats'].apply(score_threats)
        
        return df
        
    except Exception as e:
        raise RuntimeError(f"Analysis failed: {str(e)}")