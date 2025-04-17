import json
import os

def extract_model_content_to_md(json_file_path, output_md_path):
    """
    Extracts model-generated content from a JSON conversation structure
    and saves it to a Markdown file.

    Skips user prompts and model "thought" chunks.

    Args:
        json_file_path (str): Path to the input JSON file.
        output_md_path (str): Path for the output Markdown file.
    """
    print(f"Attempting to process JSON file: {json_file_path}")

    if not os.path.exists(json_file_path):
        print(f"Error: Input JSON file not found at {json_file_path}")
        return

    all_content_parts = []
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Navigate to the chunks list
        if 'chunkedPrompt' in data and 'chunks' in data['chunkedPrompt']:
            chunks = data['chunkedPrompt']['chunks']
            print(f"Found {len(chunks)} chunks in the JSON.")

            for i, chunk in enumerate(chunks):
                # Check conditions: role must be 'model' and isThought must not be True
                is_model = chunk.get('role') == 'model'
                is_thought = chunk.get('isThought', False) # Default to False if key missing

                if is_model and not is_thought:
                    print(f"  - Including content from chunk {i} (Role: Model, IsThought: {is_thought})")
                    content = chunk.get('text', '') # Get text, default to empty string if missing
                    if content:
                        all_content_parts.append(content)
                else:
                     print(f"  - Skipping chunk {i} (Role: {chunk.get('role')}, IsThought: {is_thought})")


        else:
            print("Error: Could not find 'chunkedPrompt' or 'chunks' key in the JSON structure.")
            return

        if not all_content_parts:
            print("Warning: No suitable model content found to extract.")
            # Decide if you want to create an empty file or just stop
            # Creating an empty file for consistency:
            with open(output_md_path, 'w', encoding='utf-8') as f_out:
                 f_out.write("")
            print(f"Empty Markdown file created at: {output_md_path}")
            return


        # Join all collected parts into a single string
        # Assuming the model output already includes necessary newlines between paragraphs
        full_content = "\n\n".join(all_content_parts) # Add extra newline for safety, might adjust later if needed

        # Write the combined content to the output Markdown file
        with open(output_md_path, 'w', encoding='utf-8') as f_out:
            f_out.write(full_content)

        print(f"Successfully extracted content and created Markdown file: {output_md_path}")

    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from {json_file_path}. Please check the file format.")
    except KeyError as e:
        print(f"Error: Missing expected key in JSON structure: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# --- How to use ---

# 1. Save the JSON data provided into a file (e.g., 'my_conversation.json')
#    Make sure the file is saved with UTF-8 encoding.

# 2. The script will now ask you to enter the JSON file name when you run it.

# 3. Run the script and enter the JSON file name when prompted.

if __name__ == "__main__": # Ensures this part only runs when the script is executed directly
    input_file = input("Please enter the path to your input JSON file: ") # Get input from user

    # Generate output file name based on input file name
    base_name, _ = os.path.splitext(input_file) # Split path and extension, ignore extension
    output_file = base_name + ".md" # Append '.md' to the base name

    print(f"Input file: {input_file}")
    print(f"Output file will be: {output_file}")

    extract_model_content_to_md(input_file, output_file)