import os

root_directory = "."   # Change this if needed
prefix = "_OceanofPDF.com_"

for root, dirs, files in os.walk(root_directory):
    for filename in files:
        if filename.startswith(prefix):
            new_filename = filename[len(prefix):]

            old_path = os.path.join(root, filename)
            new_path = os.path.join(root, new_filename)

            os.rename(old_path, new_path)

            print(f"Renamed: {old_path} -> {new_path}")

print("Done.")
