import base64
import json
import os
from io import BytesIO

from openai import OpenAI
from PIL import Image

# Initialize OpenAI client
client = OpenAI(api_key="")

# Target file size in bytes (e.g., 500 KB)
TARGET_SIZE = 500 * 1024


def resize_and_compress_image(image_path, target_size):
    with Image.open(image_path) as img:
        # Start with original size
        width, height = img.size
        quality = 95
        output = BytesIO()

        while True:
            # Save image to BytesIO object
            img.save(output, format="JPEG", quality=quality)
            size = output.tell()

            # Check if size is within 10% of target
            if size <= target_size * 1.1:
                break

            # If too big, reduce quality or size
            if quality > 30:
                quality -= 5
            else:
                # Reduce size by 10%
                width = int(width * 0.9)
                height = int(height * 0.9)
                img = img.resize((width, height), Image.LANCZOS)

            output = BytesIO()

        return output.getvalue()


# Encode image to Base64
def encode_image(image_data):
    return base64.b64encode(image_data).decode("utf-8")


# Define the directory containing images
image_directory = r"./dist"

# Output directory for individual JSON files
json_output_directory = r"./json_outputs"

# Ensure output directory exists
os.makedirs(json_output_directory, exist_ok=True)

failed_files = []  # List to track files that caused exceptions

# Loop through all files in the directory
for image_filename in os.listdir(image_directory):
    image_path = os.path.join(image_directory, image_filename)

    # Check if the file is an image
    if not image_path.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp")):
        continue

    try:
        # Resize and compress the image
        resized_image_data = resize_and_compress_image(image_path, TARGET_SIZE)
        base64_image = encode_image(resized_image_data)

        # Make API request to generate Bag of Words
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                        {
                            "type": "text",
                            "text": """Analyze the given image and extract key information as structured JSON data. Ensure that:
                            The "keywords" array contains unique keywords or descriptive phrases (Bag of Words) that best represent the content of the image.
                            Each item in the array should be a string.
                            Exclude words or phrases that do not clearly fit the context.
                            All words should be written in lowercase.
                            Focus on nouns, adjectives, and key phrases that accurately describe the main elements and context of the image.
                            Properly distinguish between singular and plural forms of objects.
                            If applicable, the "instances" object should differentiate between single, few, and many instances of objects, with each entry in the following format:
                            "single": ["object1", "object2", ...]
                            "few": ["object1", "object2", ...]
                            "many": ["object1", "object2", ...]
                            Additionally, extract and clearly label contextual information in the "context" object, with entries for:
                            "time": "morning", "afternoon", "evening", "night" (or similar)
                            "location": "forest", "beach", "city street", etc.
                            "object": "car", "building", "river", etc."
                            "action": "running", "jumping", "sitting", etc." (if applicable)
                            If any contextual element is unclear or cannot be inferred, clearly label it as "unknown" in the "context" object.
                            The output should be a valid JSON object like the example below:

                            {
                              "keywords": ["sky", "tree", "grass", "few clouds", "many rocks"],
                              "instances": {
                                "single": ["tree"],
                                "few": ["clouds"],
                                "many": ["rocks"]
                              },
                              "context": {
                                "time": "evening",
                                "location": "forest",
                                "object": "campfire",
                                "action": "burning"
                              }
                            }""",
                        },
                    ],
                }
            ],
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )

        # Extract JSON data from the response
        response_content = response.choices[0].message.content

        # Check if the response content starts and ends with the code block markers
        if response_content.startswith("```") and response_content.endswith("```"):
            # Remove the code block markers (```json and ```)
            response_content = response_content.strip("```json").strip("```")

        # Parse the JSON data
        bow_json = json.loads(response_content.strip())

        # Define JSON output file path for the current image
        json_output_path = os.path.join(
            json_output_directory, f"{os.path.splitext(image_filename)[0]}.json"
        )

        # Write the JSON data to a file
        with open(json_output_path, "w") as json_file:
            json.dump(bow_json, json_file, indent=4)

        print(f"Output files {json_output_path}")

    except Exception as e:
        print(f"An unexpected error occurred with {image_filename}: {e}")
        failed_files.append(image_filename)  # Track failed files

# Output the list of files that caused exceptions
if failed_files:
    print(f"The following files caused exceptions: {', '.join(failed_files)}")
else:
    print("All images were processed successfully.")

print(f"Bag of Words JSON files have been saved to {json_output_directory}")
