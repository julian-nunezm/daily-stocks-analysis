    #!/bin/bash

    # Navigate to your project directory (optional, but good practice if your script relies on relative paths)
    # cd /path/to/your/project/directory
    cd /home/julian/Documents/Dev/daily-stocks-analysis

    # Run the Python script using the virtual environment's Python interpreter
    # Replace 'your_venv_name' and 'your_script.py' with your actual names
    # /path/to/your/venv_name/bin/python /path/to/your/project/directory/your_script.py
    /home/julian/Documents/Dev/daily-stocks-analysis/.venv/bin/python /home/julian/Documents/Dev/daily-stocks-analysis/main.py

    # Optional: Log output or errors
    echo "Script executed at $(date)" >> /home/julian/Documents/Dev/daily-stocks-analysis/.logs/log_file_$(date).log
