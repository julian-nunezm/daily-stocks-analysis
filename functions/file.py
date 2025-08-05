import csv, os
from datetime import datetime
from pathlib import Path

def get_csv_filepath(filename:str) -> str:
    today = datetime.today().date()
    year_dir = today.strftime("%Y")
    month_dir = today.strftime("%b")
    current_file_path = Path(__file__).resolve()
    root_dir = current_file_path.parent.parent
    # /csv/2025/Aug/
    relative_dir = f"csv/{year_dir}/{month_dir}"
    dir = Path(os.path.join(root_dir, relative_dir))
    # Creates directory and any necessary parent directories
    dir.mkdir(parents=True, exist_ok=True)
    # stocks 2025-08-05.csv
    csv_filename = os.path.join(dir, filename)
    return csv_filename


def create_csv_from_dict(data:list[dict]) -> None:
    print("\nCreating csv file from a dict list...")
    
    # Define the fieldnames (column headers) based on dictionary keys
    fieldnames = data[0].keys()

    # stocks 2025-08-05.csv
    csv_filename = f"stocks-{datetime.today().date()}.csv"
    csv_filepath = get_csv_filepath(csv_filename)

    try:
        with open(csv_filepath, 'w', newline='') as csvfile:
            # Create a DictWriter object
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write the header row
            writer.writeheader()

            # Write the data rows
            writer.writerows(data)
    except Exception as err:
        print(f"Error in {__name__}: {err}")
    else:
        print(f"File successfully created. {csv_filepath}")