import json
import os

def flatten_quran_by_chapters(file_path):
    """
    Flattens the Quran JSON file by merging verses for each chapter into a single document.
    Saves the flattened data back as "flattened_quran.json" in the same location.

    Parameters:
        file_path (str): The path to the original Quran JSON file.
    """
    # Read the original JSON data
    with open(file_path, 'r', encoding='utf-8') as file:
        quran_data = json.load(file)

    # Initialize an empty list to hold the flattened data
    flattened_data = []

    # Loop through each chapter in the Quran data
    for chapter in quran_data:
        # Initialize an empty string for Arabic text and English translation
        arabic_text = ""
        english_translation = ""

        # Loop through each verse in the chapter
        for verse in chapter["verses"]:
            # Concatenate the Arabic text and English translation
            arabic_text += verse["text"] + "\n\n"  # Adding a double newline as a separator
            english_translation += verse["translation"] + "\n\n"  # Adding a double newline as a separator

        # Create a dictionary for the merged chapter and add it to the flattened_data list
        merged_chapter = {
            "chapter_id": chapter["id"],
            "chapter_name": chapter["name"],
            "chapter_transliteration": chapter["transliteration"],
            "chapter_translation": chapter["translation"],
            "chapter_type": chapter["type"],
            "total_verses": chapter["total_verses"],
            "arabic_text": arabic_text.strip(),  # Remove trailing newlines
            "english_translation": english_translation.strip()  # Remove trailing newlines
        }
        flattened_data.append(merged_chapter)

    # Save the flattened data back to a new JSON file in the same location
    save_path = os.path.join(os.path.dirname(file_path), "flattened_quran_by_chapters.json")
    with open(save_path, 'w', encoding='utf-8') as file:
        json.dump(flattened_data, file, ensure_ascii=False, indent=4)


def flatten_quran_by_verses(file_path):
    """
    Flattens the Quran JSON file by creating a record for each verse.
    Saves the flattened data back as "flattened_quran_verses.json" in the same location.

    Parameters:
        file_path (str): The path to the original Quran JSON file.
    """
    # Read the original JSON data
    with open(file_path, 'r', encoding='utf-8') as file:
        quran_data = json.load(file)

    # Initialize an empty list to hold the flattened data
    flattened_data = []

    # Loop through each chapter in the Quran data
    for chapter in quran_data:
        # Loop through each verse in the chapter
        for verse in chapter["verses"]:
            # Create a dictionary for each verse and populate it with chapter and verse information
            verse_record = {
                "chapter_id": chapter["id"],
                "chapter_name": chapter["name"],
                "chapter_transliteration": chapter["transliteration"],
                "chapter_translation": chapter["translation"],
                "chapter_type": chapter["type"],
                "verse_id": verse["id"],
                "arabic_text": verse["text"],
                "english_translation": verse["translation"]
            }
            flattened_data.append(verse_record)

    # Save the flattened data back to a new JSON file in the same location
    save_path = os.path.join(os.path.dirname(file_path), "flattened_quran_verses.json")
    with open(save_path, 'w', encoding='utf-8') as file:
        json.dump(flattened_data, file, ensure_ascii=False, indent=4)

# Run the functions
if __name__ == "__main__":
    flatten_quran_by_chapters('../data/quran_en.json')
    flatten_quran_by_verses('../data/quran_en.json')
