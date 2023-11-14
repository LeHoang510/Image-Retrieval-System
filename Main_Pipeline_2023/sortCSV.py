import os
import shutil

def organize_csv_files(source_folder, destination_folder):
    # Ensure the destination folder exists, or create it if it doesn't
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Iterate through CSV files in the source folder
    for filename in os.listdir(source_folder):
        if filename.endswith(".csv"):
            # Extract the prefix from the filename (e.g., "L01")
            prefix = filename.split("_")[0]

            # Create the corresponding subfolder if it doesn't exist
            subfolder = os.path.join(destination_folder, f"MapKeyframe_{prefix}")
            if not os.path.exists(subfolder):
                os.makedirs(subfolder)

            # Move the CSV file to the subfolder
            source_file = os.path.join(source_folder, filename)
            destination_file = os.path.join(subfolder, filename)
            shutil.move(source_file, destination_file)

if __name__ == "__main__":
    source_folder = "dataset/map-keyframes"  # Replace with the path to your source folder containing CSV files
    destination_folder = "map_frame_id"  # Destination folder to organize CSV files

    organize_csv_files(source_folder, destination_folder)
