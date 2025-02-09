import pandas as pd

def extract_data():
    url = "https://docs.google.com/spreadsheets/d/1syH5ntimv_5juHGOZo0LUgLO1Jk2kEQjhno8Kl21jzw/export?format=csv&gid=0"
    data = pd.read_csv(url)
    return data.iloc[0, :].values, data.iloc[1, :].values
