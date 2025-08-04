import json

def print_as_json(data:dict, indent:int=4) -> None:
    print(json.dumps(data, indent=indent))

def format_number(number):
    print(f'{number:.2f}')