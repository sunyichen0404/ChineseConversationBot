import json
import subprocess

# Load the JSON file
with open('data/config.json', 'r') as f:
    config = json.load(f)

   # Change directory to SadTalker

# Loop through each set of values
for set_values in config:
    # Extract the values from the set
    driven_audio = set_values['driven_audio']
    source_image = set_values['source_image']
    result_dir = set_values['result_dir']

    # Build the command with the extracted values
    command = f"conda activate chinese_video_bot &cd C:\\Users\\sunyi\\PycharmProjects\\chinese_video_bot\\SadTalker& python inference.py --driven_audio {driven_audio} --source_image {source_image} --result_dir {result_dir} --still --preprocess crop --enhancer gfpgan"

    # Run the command in the terminal
    subprocess.run(command, shell=True)