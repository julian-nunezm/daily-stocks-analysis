import json
import pandas as pd

def print_as_json(data:dict, indent:int=4) -> None:
    print(json.dumps(data, indent=indent))

def format_number(number):
    print(f'{number:.2f}')

def cleanse_df(df:pd.DataFrame) -> pd.DataFrame:
    """Cleans the data frame."""
    df = df.dropna()
    df = df.where((df - df.mean()).abs() <= 3 * df.std())      # TODO: What's this?
    print(df.tail())
    return df

def display_df_tail(df:pd.DataFrame, title:str) -> None:
    """Print the given title and the tail of the data frame."""
    print(f"\n{title}")
    print(df.tail())