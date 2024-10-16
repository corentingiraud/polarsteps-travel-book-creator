
# Polarsteps Travel Book Creator

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

### Run the Script

You can now run the main script to process the trip data:

```bash
python src/main.py
```

## Customization of your travel book

<details>
  <summary>Updating the photo order Using the `your_trip_photos_by_pages.txt` file</summary>
  
  The `_photos_by_pages.txt` file is a critical component of managing and updating the layout of photos in your trip. It allows you to control how the photos are grouped by pages for each step of the trip.

  ## Overview of the `_photos_by_pages.txt` File Structure

  The `_photos_by_pages.txt` file consists of a sequence of steps followed by the layout of photos for each step. The format is as follows:

  1. **Step Name**: The name of the step appears on its own line.
  2. **Photo Indexes**: Each subsequent line lists the indices of photos that should be displayed together on a page. The photos for each page are separated by spaces (each index corresponds to a photo in the step).
  3. **Empty Line**: An empty line separates the different steps in the trip.

  ### Example of `_photos_by_pages.txt`

  Here is an example of how the file might look:

  ```
  Step 1: Day at the Beach
  1 2
  4 5

  Step 2: Hiking in the Mountains
  1 2
  3
  4 5
  ```

  - **"Step 1: Day at the Beach"**:
    - The first page contains photos with indices 1, and 2.
    - The second page contains photos with indices 4 and 5.
  - **"Step 2: Hiking in the Mountains"**:
    - The first page contains photos 1 and 2.
    - The second page contains photo 3.
    - The third page contains photos 4, and 5.

  ## How to Update the Photo Layout

  If you want to change the layout of the photos in your trip, you can update the `_photos_by_pages.txt` file directly. Here's how:

  ### 1. Open the File
    - Navigate to the directory where the file is saved (`data/`)
    - Open the `_photos_by_pages.txt` file in a text editor.

  ### 2. Locate the Step
    - Find the step that you want to update by looking for the corresponding step name in the file.

  ### 3. Update the Photo Indices
    - Modify the lines following the step name to adjust the photo layout.
    - Each line represents a page of photos. List the photo indices (starting from 1) that you want on each page, separated by spaces.
    - Make sure to maintain the empty line between steps.

  #### Example Update:

  Suppose you want to change the layout for "Step 1: Day at the Beach" such that:
  - The first page should now have photos 1, and 4.
  - The second page should have photos 2 and 3.

  You would edit the file as follows:

  ```
  Step 1: Day at the Beach
  1 4
  2 3
  ```

  ### 4. Validating Your Changes

  After making changes, ensure that:
  - **No Missing Photos**: Every photo index within a step should be accounted for. Make sure you don’t miss any photos when rearranging the layout.
  - **Correct Indices**: Use the correct photo indices. Photo indices start from 1 (not 0), and they correspond to the order of photos in each step.
  - **Consistent Formatting**: Ensure there are no extra spaces or lines between the photo indices. Each step should be separated by an empty line.

  ### 5. Applying Changes to the Trip

  Once you’ve updated and saved the `_photos_by_pages.txt` file:
  1. Load the trip data in your application.
  2. The photo manager will read the updated `_photos_by_pages.txt` file and apply the new layout to the trip.
  3. If any issues arise (e.g., a photo is missing), the system may revert to the default layout for that step, and you will be notified via console output.

  ### Handling Errors

  - **Missing or Incorrect Photo Indices**: If you provide an index that doesn’t exist for a given step, or if any photos are missing from the layout, the system will use the default layout for the step and notify you with a message.
  - **Invalid File Format**: Ensure the file format follows the described structure. Any deviation may result in errors or unintended behavior.

  ## Conclusion

  Using the `_photos_by_pages.txt` file allows you to have complete control over how your trip photos are displayed. By organizing photo indices into pages, you can customize the photo layout per step, ensuring that your trip is displayed just the way you want it.
</details>
