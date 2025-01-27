
# Polarsteps Travel Book Creator

A Python tool that takes your Polarsteps data export and converts it into a beautifully formatted PDF, ready to be printed as a travel book. Perfect for preserving your travel memories!

## Setup Instructions

Ensure you are using Python version `3.13.x`. You can check your Python version with:

```bash
python --version
```

Before running the project, create a virtual environment to manage dependencies:

```bash
python -m venv env
source env/bin/activate
```

Once the virtual environment is active, install the required packages:

```bash
pip install -r requirements.txt
```

This project utilizes [Playwright](https://playwright.dev/python/) to generate PDFs with a headless browser. It may require additional dependencies depending on your operating system. Use the following command to install them:

```bash
source env/bin/activate
playwright install
```

Export your data from Polarsteps by following [these instructions](https://support.polarsteps.com/article/124-how-can-i-export-a-copy-of-my-data). Then, copy **only the trip data** into the `data/polarsteps-trip` folder. Ensure the file named `trip.json` is located in `data/polarsteps-trip/trip.json`.

You can now run the main script to process the trip data:

```bash
python src/main.py
```

You can ajust the script behaviour using the following options:

- `--debug`: Activates debug mode when included (e.g., --debug).
- `--step_ranges`: Specifies a range or list of steps to be generated, such as "1-20" for steps 1 to 20, or multip ranges separated by commas (e.g., "1-5,10,15-20").
- `--no-pdf`: Prevents PDF generation if specified (e.g., --no-pdf). Usefull to quickly test and update your travel book layout.
- `--paper_format`: Sets the paper format for the PDF output, defaulting to "A4" but can be changed to other forma (e.g., --paper_format="Letter").

The output files are located in the `travel_book` folder. The two most important files are:
- `travel_book.html` wich is the HTML file used to generate the PDF.
- `travel_book.pdf`

## Notes about default layout

Some descisions have been made for the default behaviour of the script:
- If the step description is not too long (<= 800 characters), an **cover photo** will be automatically choosen and placed in the step first page.
- Space saving is the priority for each page of the travel book. It means that the algorithm will compute the default pages layout following these priorities:
  - *Priority 1*: 4 landscape photos
  - *Priority 2*: 3 photos, must be 2 landscape + 1 portrait
  - *Priority 3*: 2 photos, must be 2 portrait
  - *Priority 4*: 1 photo

## Customization of your travel book

<details>
  <summary>Translate country / weather</summary>

You can translate countries and weather condition by editing the file `src/translations.py`. PR are welcome for better translation managment.
</details>

<details>
  <summary>Changing photo order</summary>

The `travel_book/photos_by_pages.txt` file is a critical component of managing and updating the layout of photos in your trip. It allows you to control how the photos are grouped by pages for each step of the trip. It consists of a sequence of steps followed by the layout of photos for each step. Here is an example of how the file might look:

```
Step 1: Day at the Beach
Cover photo: 1
2 3
4 5

Step 2: Hiking in the Mountains
1 2 3
4 5
```

- **"Step 1: Day at the Beach"**:
  - The cover photo is photo indice 1 (the step description is < 800 characters)
  - The second page contains photos with indices 2 and 3
  - The second page contains photos with indices 4 and 5
- **"Step 2: Hiking in the Mountains"**:
  - No cover photo
  - The first page contains photos 1, 2 and 3
  - The second page contains photo 4 and 5

To get the photo indices, open the `travel_book.html` file in your favorite browser. 

After making changes to this file, ensure that:
- **No Missing Photos**: Every photo index within a step should be accounted for. Make sure you don’t miss any photos when rearranging the layout.
- **Correct Indices**: Use the correct photo indices. Photo indices start from 1 (not 0), and they correspond to the order of photos in each step.
- **Consistent Formatting**: Ensure there are no extra spaces or lines between the photo indices. Each step should be separated by an empty line.

If any issues arise (e.g., a photo is missing), the script reverts to the default layout for that step, and you will be notified via console output.

To generate the travel book with the updated layout, relaunch the script. 
</details>
