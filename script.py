import os
import zipfile

# Create project directory structure
project_name = "social_media_cyberbullying_detector"
directories = [
    f"{project_name}",
    f"{project_name}/templates",
    f"{project_name}/static",
    f"{project_name}/static/css",
    f"{project_name}/static/js"
]

for directory in directories:
    os.makedirs(directory, exist_ok=True)

print("Project directory structure created!")
print("Directories created:")
for directory in directories:
    print(f"  {directory}")