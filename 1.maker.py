import csv  # For handling CSV files
from pathlib import Path  # For file system operations
from datetime import datetime  # For timestamped folders and file names
import subprocess  # For executing Git commands
import sys  # For exiting if no Git is available

# Define paths
input_folder = Path("./input")  # Folder containing multiple input CSVs
template_path = Path("./niche/plumber/Website 1/index.html")
output_base_folder = Path("./output")

# Base domain for generated websites (update for GitHub Pages domain)
base_domain = "https://<your-username>.github.io/<repository-name>"

# Define the correct output folder for HTML files
html_output_folder = Path("/Users/ab/Downloads/Code Projects/Prospecting Tools/6. website maker")  # Correct folder for HTML files
html_output_folder.mkdir(parents=True, exist_ok=True)

# Create a single CSV subfolder within the output directory
batch_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
csv_folder = output_base_folder / f"csv_{batch_timestamp}"
csv_folder.mkdir(parents=True, exist_ok=True)

# Ensure global resources exist
css_path = Path("./style.css")
js_path = Path("./script.js")

if not css_path.exists():
    raise FileNotFoundError(f"CSS file not found: {css_path}")
if not js_path.exists():
    raise FileNotFoundError(f"JavaScript file not found: {js_path}")

# Read the template file
with template_path.open("r", encoding="utf-8") as template_file:
    template_content = template_file.read()

# Alternate column names
company_name_alternates = ["Company Name", "BusinessName", "businessname", "Business", "business", "Name", "name"]
company_phone_alternates = ["Company Phone", "phone", "Phone", "Telephone", "telephone", "phone #1", "phone #2"]

# Global set to track used company names
used_company_names = set()

# Process each CSV file in the input folder
for input_csv_path in input_folder.glob("*.csv"):
    print(f"Processing file: {input_csv_path.name}")

    # Create a readable timestamp for the output CSV file name
    csv_file_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_csv_path = csv_folder / f"{input_csv_path.stem}_updated_data_{csv_file_timestamp}.csv"

    # Prepare the output CSV
    with input_csv_path.open("r", encoding="utf-8") as csv_file, output_csv_path.open("w", encoding="utf-8", newline="") as output_csv_file:
        reader = csv.DictReader(csv_file)

        # Normalize headers
        reader.fieldnames = [name.strip() for name in reader.fieldnames]

        # Detect columns dynamically
        company_name_col = next((alt for alt in company_name_alternates if alt in reader.fieldnames), None)
        company_phone_col = next((alt for alt in company_phone_alternates if alt in reader.fieldnames), None)

        if not company_name_col:
            print("No valid column found for company name. Skipping this file.")
            continue
        if not company_phone_col:
            print("No valid column found for company phone. Skipping this file.")
            continue

        fieldnames = reader.fieldnames + ["Website We Made"]  # Add the new column
        writer = csv.DictWriter(output_csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            # Safeguard against missing columns
            company_name = row.get(company_name_col, "").strip()
            company_phone = row.get(company_phone_col, "").strip()

            if not company_name or not company_phone:
                print(f"Skipping row due to missing data: {row}")
                continue

            # Skip duplicates
            if company_name in used_company_names:
                print(f"Skipping duplicate company name: {company_name}")
                continue

            # Mark the name as used
            used_company_names.add(company_name)

            # Replace placeholders with actual data
            updated_content = template_content.replace("{{Company Name}}", company_name)
            updated_content = template_content.replace("{{Company Phone}}", company_phone)

            # Use relative paths for CSS and JS
            updated_content = updated_content.replace(
                "{{CSS Path}}", "./style.css"
            ).replace(
                "{{JS Path}}", "./script.js"
            )

            # Create a safe file name for the HTML file
            safe_name = company_name.replace(" ", "_").replace("/", "-")
            output_file_path = html_output_folder / f"{safe_name}.html"

            # Write the updated content to the new HTML file
            with output_file_path.open("w", encoding="utf-8") as output_file:
                output_file.write(updated_content)

            # Generate the website URL
            website_url = f"{base_domain}/{safe_name}.html"
            row["Website We Made"] = website_url  # Add the URL to the row

            # Write the updated row to the new CSV
            writer.writerow(row)

print(f"HTML files generated in: {html_output_folder}")
print(f"CSV files generated in: {csv_folder}")

# Ask user if they want to commit the changes
commit_decision = input("Do you want to commit the changes to GitHub? (y/n): ").strip().lower()
if commit_decision == "y":
    # Prepare the commit message
    commit_message = f"Auto-commit: Updated batch generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    try:
        # Add all files to Git
        subprocess.run(["git", "add", "."], check=True)
        
        # Commit the changes
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        
        # Push the changes to GitHub
        subprocess.run(["git", "push"], check=True)
        print("Changes committed and pushed to GitHub.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during the Git operation: {e}")
        sys.exit(1)
else:
    print("Commit skipped. You can commit the changes manually later.")