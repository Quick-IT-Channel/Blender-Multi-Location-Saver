# Python Code to save projects in Multiple locations 
import bpy
import shutil
import os
import glob

# Define your backup locations
backup_paths = [
    "D:/Blender_Backup_01/",    # Location 1 where you want to save the backups
    "G:/Blender_Backups/Blender_Backup_02/"     # Location 2 where you want to save the backups
]

# Define the maximum number of .blend* backup files to keep
max_backup_files = 1  # Adjust to how many backups you want

# Function to create backups for all .blend* files and manage naming
def save_backup():
    # Get the current .blend file path
    current_file = bpy.data.filepath
    
    # Check if the file is already saved
    if current_file:
        # Get the directory and base filename
        blend_dir = os.path.dirname(current_file)
        blend_base = os.path.basename(current_file)

        # Create a pattern to find all .blend* files (including the current .blend and any backups like .blend1, .blend2, etc.)
        blend_pattern = os.path.join(blend_dir, blend_base) + "*"
        blend_files = glob.glob(blend_pattern)

        # Sort files by modification time, latest first
        blend_files.sort(key=os.path.getmtime, reverse=True)

        # Copy each .blend* file to the backup locations
        for path in backup_paths:
            # Ensure the backup directory exists, create it if necessary
            if not os.path.exists(path):
                os.makedirs(path)

            # Ensure .blend gets backed up and renamed as .blend1 if max backups = 1
            if max_backup_files == 1:
                blend_file = blend_files[0]  # The latest saved file (either .blend or .blend1)
                backup_file = os.path.join(path, os.path.basename(blend_file).replace('.blend', '.blend1'))
                shutil.copy(blend_file, backup_file)
                print(f"Backup saved at: {backup_file}")
            else:
                for i, blend_file in enumerate(blend_files):
                    # Create the backup file path
                    backup_file = os.path.join(path, os.path.basename(blend_file))

                    # Copy the .blend* file to the backup location
                    shutil.copy(blend_file, backup_file)
                    print(f"Backup saved at: {backup_file}")

            # Manage the number of backups to keep
            manage_backups(path, blend_base)
    else:
        print("The file hasn't been saved yet. Please save the file first.")

# Function to manage the number of .blend backups in a location
def manage_backups(path, blend_base):
    # Create a pattern to find all .blend* backup files in the backup location
    backup_pattern = os.path.join(path, blend_base) + "*"
    backup_files = glob.glob(backup_pattern)

    # Sort the backup files by modified time (oldest first)
    backup_files.sort(key=os.path.getmtime)

    # If the number of backups exceeds the limit, delete the oldest files
    if len(backup_files) > max_backup_files:
        files_to_delete = backup_files[:len(backup_files) - max_backup_files]
        for file in files_to_delete:
            os.remove(file)
            print(f"Deleted old backup: {file}")

# Handler to run save_backup() after saving the file
def on_save(dummy):
    print("File saved. Running backup script...")
    save_backup()

# Register the handler to detect when the user saves the file
bpy.app.handlers.save_post.append(on_save)

print("Backup handler registered. The script will now run after every save.")




# This Python script for Blender automates saving your projects and creating backups in multiple locations after each save. The script listens for a save event and then copies the .blend file and its backup versions (.blend1, .blend2, etc.) to specified backup directories.

# Here’s a breakdown of the key steps:

# Backup Paths: You can customize the list of paths where backups are saved by adding new directories in backup_paths.
# Save and Backup: After saving the current .blend file, the script locates all associated .blend* files and copies them to the backup locations.
# Backup Trigger: The script is triggered after each save, thanks to the bpy.app.handlers.save_post.append(on_save) handler.
