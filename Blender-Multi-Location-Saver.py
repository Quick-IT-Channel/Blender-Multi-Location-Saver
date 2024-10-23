# Python Code to save projects in Multiple locations 
import bpy
import shutil
import os
import glob

# Define your backup locations
backup_paths = [
#You can add as many locations needed 
    "G:/Blender_Backup_01/",    # Location 1 where you want to save the backups
    "E:/Blender_Backup_02/"     # Location 2 where you want to save the backups
]

# Function to save Blender project and create backups for all .blend* files
def save_backup():
    # Get the current .blend file path
    current_file = bpy.data.filepath
    
    # Check if the file is already saved
    if current_file:
        # Save the current file
        bpy.ops.wm.save_mainfile()

        # Get the directory and base filename
        blend_dir = os.path.dirname(current_file)
        blend_base = os.path.basename(current_file)

        # Create a pattern to find all .blend* files (including .blend1, .blend2, etc.)
        blend_pattern = os.path.join(blend_dir, blend_base) + "*"
        blend_files = glob.glob(blend_pattern)

        # Copy each .blend* file to the backup locations
        for path in backup_paths:
            # Ensure the backup directory exists, create it if necessary
            if not os.path.exists(path):
                os.makedirs(path)
            
            for blend_file in blend_files:
                # Create the backup file path
                backup_file = os.path.join(path, os.path.basename(blend_file))

                # Copy the .blend* file to the backup location
                shutil.copy(blend_file, backup_file)
                print(f"Backup saved at: {backup_file}")
    else:
        print("The file hasn't been saved yet. Please save the file first.")

# Handler to run save_backup() after saving the file
def on_save(dummy):
    print("File saved. Running backup script...")
    save_backup()

# Register the handler to detect when the user saves the file
bpy.app.handlers.save_post.append(on_save)

print("Backup handler registered. The script will now run after every save.")
