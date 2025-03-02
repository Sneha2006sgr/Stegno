from PIL import Image

def binary_to_text(binary_string):
    """Convert a binary string to text."""
    # Break the binary string into 8-bit chunks
    binary_chunks = [binary_string[i:i+8] for i in range(0, len(binary_string), 8)]
    text = ""
    
    for chunk in binary_chunks:
        # Skip incomplete chunks
        if len(chunk) != 8:
            continue
            
        # Convert to decimal
        decimal_value = int(chunk, 2)
        
        # Only add printable ASCII and common whitespace
        if (32 <= decimal_value <= 126) or decimal_value in (9, 10, 13):
            text += chr(decimal_value)
        else:
            # Found a non-printable character - likely the end of the real message
            break
            
    return text

def find_message_end(text):
    """Find where the actual message ends before garbage characters begin."""
    # Look for common message terminators
    common_endings = ['.', '!', '?', ':', ';']
    
    # First, try to find where message naturally ends with punctuation
    for i in range(len(text)-1, 0, -1):
        if text[i] in common_endings:
            # Check if what follows looks like garbage
            following_text = text[i+1:]
            if not following_text or has_high_entropy(following_text):
                return text[:i+1]
    
    return text

def has_high_entropy(text):
    """Check if text has characteristics of random garbage."""
    if not text:
        return False
        
    # Count unusual character sequences
    unusual_pairs = 0
    for i in range(len(text)-1):
        c1, c2 = text[i], text[i+1]
        # Check for uncommon character transitions
        if not is_common_pair(c1, c2):
            unusual_pairs += 1
            
    # If more than 40% of character pairs are unusual, likely garbage
    return unusual_pairs / (len(text)-1) > 0.4

def is_common_pair(c1, c2):
    """Check if two characters commonly appear next to each other in normal text."""
    # Space followed by letter/number is common
    if c1 == ' ' and (c2.isalnum() or c2 in '.,!?'):
        return True
    # Letter followed by letter/space/punctuation is common
    if c1.isalpha() and (c2.isalpha() or c2 == ' ' or c2 in '.,!?:;'):
        return True
    # Number followed by number/space/punctuation is common
    if c1.isdigit() and (c2.isdigit() or c2 == ' ' or c2 in '.,'):
        return True
    # Punctuation followed by space is common
    if c1 in '.!?:;,' and c2 == ' ':
        return True
    return False

def extract_message(image_path):
    """Extract hidden message from an image using LSB steganography."""
    try:
        # Open and prepare the image
        img = Image.open(image_path)
        img = img.convert("RGB")
        width, height = img.size
        pixels = list(img.getdata())
        
        # Extract the length bytes (32 bits / 4 bytes)
        binary_length = ""
        byte_index = 0
        
        # Get the first 32 bits to determine message length
        for i in range(min(32, len(pixels)*3)):
            pixel_index = i // 3
            color_index = i % 3
            if pixel_index < len(pixels):
                pixel = pixels[pixel_index]
                binary_length += str(pixel[color_index] & 1)
                byte_index += 1
        
        # Convert to decimal
        try:
            message_length = int(binary_length, 2)
        except ValueError:
            return "Error: Couldn't determine message length. This image may not contain a hidden message."
            
        # Sanity check on message length
        if message_length <= 0 or message_length > (len(pixels)*3 - 32) // 8:
            return "Error: Invalid message length detected."
            
        # Extract the message bits
        binary_message = ""
        for i in range(message_length * 8):
            if byte_index >= len(pixels) * 3:
                break
                
            pixel_index = byte_index // 3
            color_index = byte_index % 3
            
            if pixel_index < len(pixels):
                pixel = pixels[pixel_index]
                binary_message += str(pixel[color_index] & 1)
                byte_index += 1
        
        # Convert to text
        message = binary_to_text(binary_message)
        
        # Clean up any remaining garbage
        clean_message = find_message_end(message)
        
        return clean_message
        
    except Exception as e:
        return f"Error processing image: {str(e)}"

def main():
    """Main program function."""
    try:
        # Get input file
        image_file = input("Enter the encoded image filename: ")
        
        # Process and display result
        result = extract_message(image_file)
        
        print("\n===== EXTRACTED MESSAGE =====")
        print(result)
        print("============================\n")
        
    except Exception as e:
        print(f"Program error: {str(e)}")

if __name__ == "__main__":
    main()