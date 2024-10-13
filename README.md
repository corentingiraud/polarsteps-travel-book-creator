
# Polarsteps Trip Data Processor

This project processes trip data exported from [Polarsteps](https://support.polarsteps.com/article/124-how-can-i-export-a-copy-of-my-data).

## Setup Instructions

### 0. Python Version

Ensure you are using Python version `3.12`. You can check your Python version with:

```bash
python --version
```

### 1. Create a Virtual Environment

Before running the project, create a virtual environment to manage dependencies:

```bash
python -m venv env
source env/bin/activate
```

### 2. Install Dependencies

Once the virtual environment is active, install the required packages:

```bash
pip install -r requirements.txt
```

### 3. Export Polarsteps Data

Export your data from Polarsteps by following [these instructions](https://support.polarsteps.com/article/124-how-can-i-export-a-copy-of-my-data).

### 5. Add Trip Data

Once you have your Polarsteps data, copy **only the trip data** into the `data/polarsteps-trip` folder. Ensure the file named `trip.json` is located as follows:

```
data/polarsteps-trip/trip.json
```

### 6. Run the Script

You can now run the main script to process the trip data:

```bash
python src/main.py
```
