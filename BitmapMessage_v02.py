from PIL import Image # Python Imaging Library for converting the image to greyscale and resizing it.
from tkinter import filedialog, Tk # Standard GUI package to open dialogs to select images and output txt files.
import sys # Provides access to system specific parameters and functions. Used for exiting the program.

def create_ascii_art(bitmap, message):
    """
    Generate ASCII art from the bitmap using a provide message.
    
    Parameters:
    - bitmap:   A string representation of the image, where ' ' represents a pixel that
                passes the threshold (darker), and '*' represents a lighter pixel. 
                (My system is in darkmode. Invert '*' and ' ' for lightmode.)
    - message:  The message to display in the ASCII art format.
    
    Returns:
    A string that visually represents the original image using ASCII characters,
    composed of the message's characters.
    """
    # Use list comprehension to process each line in the bitmap.
    # For each '*' (lighter pixel), a character from the message is used.
    # For ' ' (darker pixel), a space is added instead.
    # i is used to step through the message. % is used to loop the message.
    ascii_art = [
        ''.join(message[i % len(message)] if bit == '*' else ' ' # Repeat message across the line with message[i % len(message)] if the char is '*' else leave as ' '.
                for i, bit in enumerate(line)) # Iterate over each character in the line.
        for line in bitmap.splitlines() # This iterates over each line of the bitmap.
        ]
    return '\n'.join(ascii_art) # Join every line together with newline characters


def get_input(prompt, cast_to=None):
    """
    Prompts the user for input, with an option to cast the input to a specified type.
    It loops until a non-empty input is received if casting is not required,
    or a valid input is provided that can be cast to the required type.
    
    Parameters:
    - prompt:       The message displayed to the user.
    - cast_to:      The type to which the user's input should be cast.
    
    Returns:
    The user's input, optionally cast to the specified type.
    """
    while True: # Loop until valid input is received or the user exits.
        user_input = input(prompt) # Gets the users input using the unique prompt.            
        if not user_input:
            print("Input cannot be empty. Please provide a valid input.")
            continue
        
        if cast_to:
            try:
                return cast_to(user_input) # Attempt to cast the user input to the specified type.
            except ValueError: # Catch ValueError if casting fails (e.g., convering 'cat' to int).
                print(f"Invalid input. Please enter a value of type {cast_to.__name__}.")
                continue # Prompt the user for input again.
        else:
            return user_input # Return the input as is if no casting is required.


def convert_image_to_bitmap(image_path, threshold, width_limit=1000):
    """
    Converts an image to a bitmap representation based on the threshold.
    
    Parameters:
    - image_path:   Path to the image file.
    - threshold:    The threshold to differentiate between dark and light pixels.
    - width_limit:  The maximum width of the ASCII art, to prevent excessively wide outputs.
    
    Returns:
    A string representing the bitmap, with '*' for light pixels and ' ' for dark pixels.
    (My system is in darkmode. Invert '*' and ' ' for lightmode.)
    """
    try:
        with Image.open(image_path) as img: # Opens a dialog to select an image.
            # Resize image if its width exceeds the width limit.
            if img.width > width_limit:
                aspect_ratio = img.height / img.width
                # Get a new height to account for the adjusted width while maintaining the aspect ratio.
                new_height = int(aspect_ratio * width_limit * 0.55) # 0.55 is a correction factor to compensate for the height of non-square fonts. Adjust as needed.
                img = img.resize((width_limit, new_height), Image.Resampling.LANCZOS) # Resize the image with LANCZOS resampling.
                
            img = img.convert("L") # Convert the image to greyscale.
            
            # Generate the bitmap string with '*' for dark pixels and ' ' for light pixels.
            bitmap = "" # Initialize as an empty string.
            for y in range(img.height): # Loop through the y pixels.
                for x in range(img.width): # Loop through the x pixels.
                    if img.getpixel((x,y)) < threshold: # Check if x, y pixel is less than threshold.
                        bitmap += " " # Dark pixel.
                    else:
                        bitmap += "*" # Light pixel.
                bitmap += "\n" # New line at the end of each row.
            
            # Split the string by line breaks, remove trailing white spaces, rebuild again with newline characters, then return.
            return '\n'.join(
                line.rstrip() # Remove trailing spaces from each line for cleaner ASCII art.
                for line in bitmap.splitlines() # Split by line breaks.
            )
    except FileNotFoundError: # Exit the program if no file is found.
        print("File not found. Please ensure the path is correct.")
        sys.exit()
    except Exception as e: # Exit the program if an error occurs.
        print(f"An error occurred: {e}")
        sys.exit()
        

def select_file(title, prompt, filetypes): 
    """Opens a dialog to select a file, returns the selected path."""
    # Tk().withdraw() # We don't want a full GUI so keep the root window from appearing
    print(prompt)
    selected_file = filedialog.askopenfilename(title=title, filetypes=filetypes)
    if selected_file == "":
        print("No image selected. Exiting.")
        sys.exit()
    else:
        return selected_file


def save_file(content, title, filetypes):
    """Saves content to a file chosen by the user through a dialog."""
    # Tk().withdraw() # We don't want a full GUI so keep the root window from appearing
    output_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=filetypes, title=title)
    if output_path:
        with open(output_path, "w") as f:
            f.write(content)    
        print(f"File saved to {output_path}") # Notify user of output path.
    else: # Exit if no output directory selected.
        print("No file selected. Exiting.")
        sys.exit()
        

def main():
    print('Image to Message, by smallcabbage333 smallcabbage33@gmail.com') # Intro.
    image_path = select_file("Select an Image", "Selecting an image...", [("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")]) # Get the image.
    threshold = get_input("Input a threshold for black and white pixels: ", int) # Get the thresehold for processing black and white.
    message = get_input("Enter the message to display with the bitmap: ", str) # Get the message for filling out the ASCII art.
    bitmap = convert_image_to_bitmap(image_path, threshold) # Convert the image to a string of '*' (white) and ' ' (black) using the threshold.
    ascii_art = create_ascii_art(bitmap, message) # Fill the string with the message on only the '*' (white) characters
    save_file(ascii_art, "Save ASCII Art As", [("Text files", "*.txt")]) # Output the ASCII art to a txt file.
    

if __name__ == '__main__':
    main() # Start the main loop.