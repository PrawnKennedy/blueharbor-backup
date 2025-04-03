# webscraper practice
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

def fetch_data():
    url = "https://www.worldometers.info/coronavirus/"
    headers = {"User-Agent": "Mozilla/5.0"}  
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print("failure: could not retrieve data!")
        return None
    
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", id="main_table_countries_today")
    
    if not table:
        print("table not found. check site")
        print(soup.prettify())  
        return None
    
    headers = [header.get_text(strip=True) for header in table.find_all("th")]
    rows = []
    
    for row in table.find("tbody").find_all("tr"):
        cells = row.find_all("td")
        if len(cells) > 1: 
            country = cells[1].get_text(strip=True)  
            row_data = [country] + [cell.get_text(strip=True).replace(',', '') for cell in cells[2:6]]
            rows.append(row_data)
    
    df = pd.DataFrame(rows, columns=["Country", "Total Cases", "New Cases", "Total Deaths", "New Deaths"])
    return df

def clean_data(df):
    df = df[df["Country"].str.contains("Total|World|#", na=False) == False]  
    df.replace({'': '0', 'N/A': '0'}, regex=True, inplace=True)
    
    for col in ["Total Cases", "New Cases", "Total Deaths", "New Deaths"]:
        df[col] = pd.to_numeric(df[col], errors='coerce')  
    
    df = df.dropna().reset_index(drop=True)
    return df

def display_data(df):
    print("\n=== DEBUG: Raw Extracted Data ===")
    print(df.head(20)) 
    
    df_top = df.sort_values(by="Total Cases", ascending=False).head(10)
    print("\n=== DEBUG: Top 10 Countries ===")
    print(df_top)
    
    plt.figure(figsize=(10, 5))
    plt.barh(df_top["Country"], df_top["Total Cases"].astype(int), color='blue')
    plt.xlabel("Total Cases")
    plt.ylabel("Country")
    plt.title("Top 10 Countries with Most COVID-19 Cases")
    plt.gca().invert_yaxis()
    plt.show()

def main():
    print("Fetching data...")
    data = fetch_data()
    
    if data is not None:
        clean_df = clean_data(data)
        display_data(clean_df)
    else:
        print("No data available.")

if __name__ == "__main__":
    main()