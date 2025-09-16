import os
from PIL import Image
import imagehash

def calculate_image_resolution(file_path):
    try:
        with Image.open(file_path) as img:
            return img.size  # (width, height)
    except Exception:
        return (0, 0)

def find_and_clean_similar_images(folder_path, hash_size=8, threshold=5):
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']
    hash_map = {}  # image hash -> list of (file_path, file_size, resolution)

    print("🔍 Scanning images and building perceptual hashes...")
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_ext = os.path.splitext(file)[1].lower()
            if file_ext not in image_extensions:
                continue

            file_path = os.path.join(root, file)
            try:
                img = Image.open(file_path)
                img_hash = imagehash.phash(img, hash_size=hash_size)
                file_size = os.path.getsize(file_path)
                resolution = img.size  # (width, height)

                found_similar = False
                for existing_hash in list(hash_map.keys()):
                    if abs(img_hash - existing_hash) <= threshold:
                        hash_map[existing_hash].append((file_path, file_size, resolution))
                        found_similar = True
                        break

                if not found_similar:
                    hash_map[img_hash] = [(file_path, file_size, resolution)]

            except Exception as e:
                print(f"⚠️ Could not process {file_path}: {e}")

    print("\n🗑️ Removing duplicates, keeping the largest image in each group...")

    total_deleted = 0
    for file_list in hash_map.values():
        if len(file_list) > 1:
            # Sort by file size and resolution (width x height), descending
            file_list.sort(key=lambda x: (x[1], x[2][0] * x[2][1]), reverse=True)
            original = file_list[0][0]
            print(f"\n✅ Keeping original: {original}")
            for duplicate in file_list[1:]:
                try:
                    os.remove(duplicate[0])
                    print(f"🗑️ Deleted duplicate: {duplicate[0]}")
                    total_deleted += 1
                except Exception as e:
                    print(f"⚠️ Could not delete {duplicate[0]}: {e}")

    print(f"\n✅ Cleaning complete! Total duplicates deleted: {total_deleted}")

# Example usage
if __name__ == "__main__":
    folder_to_clean = input("📁 Enter full path of folder to scan and clean images: ")
    find_and_clean_similar_images(folder_to_clean)
