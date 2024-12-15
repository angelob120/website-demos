import csv  # For handling CSV files
from pathlib import Path  # For file system operations
from datetime import datetime  # For timestamped folders and file names
import subprocess  # For executing Git commands
import sys  # For exiting if no Git is available

# Define paths
input_folder = Path("./input")  # Folder containing multiple input CSVs
template_path = Path("./niche/plumber/Website 1/index.html")
output_base_folder = Path("./output")

# Base domain for generated websites
base_domain = "easywebstudios.xyz"

# Create a timestamped subfolder in the output directory
batch_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
output_folder = output_base_folder / f"batch_{batch_timestamp}"
output_folder.mkdir(parents=True, exist_ok=True)

# Create a timestamped CSV subfolder in the batch folder
csv_folder_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
csv_folder = output_folder / f"csv_{csv_folder_timestamp}"
csv_folder.mkdir(parents=True, exist_ok=True)

# Ensure global resources exist
css_path = output_base_folder / "style.css"
js_path = output_base_folder / "script.js"

if not css_path.exists():
    raise FileNotFoundError(f"CSS file not found: {css_path}")
if not js_path.exists():
    raise FileNotFoundError(f"JavaScript file not found: {js_path}")

# Read the template file
with template_path.open("r", encoding="utf-8") as template_file:
    template_content = template_file.read()

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
        fieldnames = reader.fieldnames + ["Website We Made"]  # Add the new column
        writer = csv.DictWriter(output_csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            # Safeguard against missing columns
            company_name = row.get("Company Name", "").strip()
            company_phone = row.get("Company Phone", "").strip()

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
            updated_content = updated_content.replace("{{Company Phone}}", company_phone)

            # Use relative paths for CSS and JS
            updated_content = updated_content.replace(
                "{{CSS Path}}", "../style.css"
            ).replace(
                "{{JS Path}}", "../script.js"
            )

            # Create a safe file name for the HTML file
            safe_name = company_name.replace(" ", "_").replace("/", "-")
            output_file_path = output_folder / safe_name / "index.html"
            output_file_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure directory exists

            # Write the updated content to the new HTML file
            with output_file_path.open("w", encoding="utf-8") as output_file:
                output_file.write(updated_content)

            # Generate the website URL
            website_url = f"{base_domain}/{safe_name}"
            row["Website We Made"] = website_url  # Add the URL to the row

            # Write the updated row to the new CSV
            writer.writerow(row)

print(f"HTML files generated in: {output_folder}")
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