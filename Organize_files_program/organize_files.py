import os
import shutil

# Define file type categories
FILE_TYPES = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'],
    'Audio': ['.mp3', '.wav', '.aac', '.flac', '.ogg'],
    'Documents': ['.pdf', '.doc', '.docx', '.txt', '.xls', '.xlsx', '.ppt', '.pptx'],
    'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.flv'],
    'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz']
}

# Threshold size in bytes (e.g., 10 KB)
SMALL_FILE_THRESHOLD = 10 * 1024

def organize_folder(folder_path):
    folder_path = folder_path.strip()
    if not folder_path:
        print("Error: No folder path provided.")
        return

    if not os.path.exists(folder_path):
        print(f"Error: Folder not found: {folder_path}")
        return

    try:
        # Create category folders if they do not exist
        for category in FILE_TYPES.keys():
            os.makedirs(os.path.join(folder_path, category), exist_ok=True)
        os.makedirs(os.path.join(folder_path, 'Others'), exist_ok=True)
    except Exception as e:
        print(f"Error creating category folders: {e}")
        return

    # Process all files in the folder
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)

        # Skip directories
        if os.path.isdir(item_path):
            continue

        try:
            file_ext = os.path.splitext(item)[1].lower()
            file_size = os.path.getsize(item_path)

            moved = False

            # Small files go to Others
            if file_size <= SMALL_FILE_THRESHOLD:
                target_folder = 'Others'
                moved = True
            else:
                # Check file type and move accordingly
                for category, extensions in FILE_TYPES.items():
                    if file_ext in extensions:
                        target_folder = category
                        moved = True
                        break

            # If no matching type, treat as Others
            if not moved:
                target_folder = 'Others'

            dest_path = os.path.join(folder_path, target_folder, item)

            # Handle file name collisions by adding a numeric suffix
            base_name, ext = os.path.splitext(item)
            counter = 1
            while os.path.exists(dest_path):
                dest_path = os.path.join(folder_path, target_folder, f"{base_name}_{counter}{ext}")
                counter += 1

            shutil.move(item_path, dest_path)
            print(f"Moved: {item} --> {target_folder}/")

        except PermissionError:
            print(f"Permission denied: {item_path}")
        except Exception as e:
            print(f"Error processing {item}: {e}")

    print("\n✅ Organization complete!")

if __name__ == "__main__":
    folder_to_organize = input("📁 Enter the full path of the folder to organize: ")
    organize_folder(folder_to_organize)
