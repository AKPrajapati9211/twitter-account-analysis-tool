from scraper import scrape_x_profile
from analyzer import analyze_tweets
from report_generator import generate_report
import os

def run_analysis(username="narendramodi", tweet_limit=200):
    # 1. Scrape
    if not os.path.exists(f"{username}_tweets.csv"):
        scrape_x_profile(username, tweet_limit)
    
    # 2. Analyze
    df = analyze_tweets(username)
    
    # 3. Report
    generate_report(username)
    print("✅ Analysis complete!")

if __name__ == "__main__":
    run_analysis('crimeldn')