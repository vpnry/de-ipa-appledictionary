#!/usr/bin/env python3
"""
CSV to Apple Dictionary Converter
Specifically for de_word_ipa.csv with columns: words,ipa,common
"""

import csv
import re
import html
import os
from pathlib import Path

class CSVToAppleDictConverter:
    def __init__(self, input_file, output_dir="GermanIPADictionary", dict_name="German IPA"):
        self.input_file = input_file
        self.output_dir = Path(output_dir)
        self.dict_name = dict_name
        
    def parse_csv_file(self):
        """Parse the CSV file and extract entries"""
        entries = []
        
        try:
            with open(self.input_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    word = row.get('words', '').strip()
                    ipa = row.get('ipa', '').strip()
                    
                    if word and ipa:
                        entries.append((word, ipa))
        except Exception as e:
            print(f"Error parsing CSV: {e}")
            return []
        
        print(f"Parsed {len(entries)} entries")
        return entries
    
    def sanitize_xml_text(self, text):
        """Remove invalid XML characters"""
        def is_valid_xml_char(char):
            codepoint = ord(char)
            return (
                codepoint == 0x9 or
                codepoint == 0xA or
                codepoint == 0xD or
                (0x20 <= codepoint <= 0xD7FF) or
                (0xE000 <= codepoint <= 0xFFFD) or
                (0x10000 <= codepoint <= 0x10FFFF)
            )
        
        return ''.join(char for char in text if is_valid_xml_char(char))
    
    def create_dictionary_xml(self, entries):
        """Generate the Apple Dictionary XML content"""
        xml_content = ['<?xml version="1.0" encoding="UTF-8"?>']
        xml_content.append('<d:dictionary xmlns="http://www.w3.org/1999/xhtml" xmlns:d="http://www.apple.com/DTDs/DictionaryService-1.0.rng">')
        
        for idx, (word, ipa) in enumerate(entries):
            # Sanitize and escape HTML special characters
            word_clean = self.sanitize_xml_text(word)
            ipa_clean = self.sanitize_xml_text(ipa)
            
            word_escaped = html.escape(word_clean)
            ipa_escaped = html.escape(ipa_clean)
            
            # Create unique entry ID
            # Use index to avoid collisions with same words (if any)
            base_id = re.sub(r'[^a-zA-Z0-9]', '_', word_clean)
            entry_id = f"{base_id}_{idx}"
            
            xml_content.append(f'  <d:entry id="{entry_id}" d:title="{word_escaped}">')
            xml_content.append(f'    <d:index d:value="{word_escaped}"/>')
            xml_content.append(f'    <div class="entry">')
            xml_content.append(f'      <h1>{word_escaped}</h1>')
            xml_content.append(f'      <span class="ipa">| {ipa_escaped} |</span>')
            xml_content.append(f'    </div>')
            xml_content.append('  </d:entry>')
        
        xml_content.append('</d:dictionary>')
        
        return '\n'.join(xml_content)
    
    def create_makefile(self):
        """Generate Makefile for building the dictionary"""
        makefile_content = f"""#
# Makefile
#

# You need to edit these values if the Dictionary Development Kit is elsewhere.
DICT_BUILD_TOOL_DIR	=	"/Applications/Utilities/Dictionary Development Kit"

DICT_NAME		=	"{self.dict_name}"
DICT_SRC_PATH		=	Contents/Resources/MyDictionary.xml
CSS_PATH		=	Contents/Resources/MyDictionary.css
PLIST_PATH		=	Contents/MyInfo.plist

DICT_BUILD_TOOL_BIN	=	"$(DICT_BUILD_TOOL_DIR)/bin"
DICT_DEV_KIT_OBJ_DIR	=	./objects
export	DICT_DEV_KIT_OBJ_DIR

DESTINATION_FOLDER	=	~/Library/Dictionaries
RM			=	/bin/rm

all:
	"$(DICT_BUILD_TOOL_BIN)/build_dict.sh" $(DICT_NAME) $(DICT_SRC_PATH) $(CSS_PATH) $(PLIST_PATH)
	echo "Done."

install:
	echo "Installing into $(DESTINATION_FOLDER)".
	mkdir -p $(DESTINATION_FOLDER)
	ditto --noextattr --norsrc $(DICT_DEV_KIT_OBJ_DIR)/$(DICT_NAME).dictionary  $(DESTINATION_FOLDER)/$(DICT_NAME).dictionary
	touch $(DESTINATION_FOLDER)
	echo "Done."

clean:
	$(RM) -rf $(DICT_DEV_KIT_OBJ_DIR)
"""
        return makefile_content
    
    def create_info_plist(self):
        """Generate MyInfo.plist for the dictionary"""
        bundle_id = "com.apple.dictionary." + re.sub(r'[^a-zA-Z0-9]', '', self.dict_name).lower()
        plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>CFBundleDevelopmentRegion</key>
	<string>German</string>
	<key>CFBundleIdentifier</key>
	<string>{bundle_id}</string>
	<key>CFBundleName</key>
	<string>{self.dict_name}</string>
	<key>CFBundleShortVersionString</key>
	<string>1.0</string>
	<key>DCSDictionaryCopyright</key>
	<string>Created with CSVToAppleDictConverter</string>
	<key>DCSDictionaryManufacturerName</key>
	<string>User</string>
</dict>
</plist>
"""
        return plist_content
    
    def create_css(self):
        """Generate CSS styling for the dictionary"""
        css_content = """
body {
    font-family: -apple-system, sans-serif;
    margin: 10px;
}

.entry {
    margin-bottom: 20px;
}

h1 {
    font-size: 1.5em;
    margin-bottom: 5px;
    color: #333;
}

.ipa {
    font-family: "Lucida Sans Unicode", "Arial Unicode MS", sans-serif;
    font-size: 1.2em;
    color: #666;
    padding: 2px 5px;
    border-radius: 3px;
    display: inline-block;
}
"""
        return css_content
    
    def convert(self):
        """Main conversion process"""
        print(f"Converting {self.input_file}...")
        
        contents_dir = self.output_dir / "Contents"
        resources_dir = contents_dir / "Resources"
        resources_dir.mkdir(parents=True, exist_ok=True)
        
        entries = self.parse_csv_file()
        if not entries:
            return False
            
        print("Writing MyDictionary.xml...")
        xml_content = self.create_dictionary_xml(entries)
        with open(resources_dir / "MyDictionary.xml", 'w', encoding='utf-8') as f:
            f.write(xml_content)
            
        print("Writing Makefile...")
        with open(self.output_dir / "Makefile", 'w', encoding='utf-8') as f:
            f.write(self.create_makefile())
            
        print("Writing MyInfo.plist...")
        with open(contents_dir / "MyInfo.plist", 'w', encoding='utf-8') as f:
            f.write(self.create_info_plist())
            
        print("Writing MyDictionary.css...")
        with open(resources_dir / "MyDictionary.css", 'w', encoding='utf-8') as f:
            f.write(self.create_css())
            
        print(f"\nConversion finished! Files are in {self.output_dir}")
        print("To build: cd " + str(self.output_dir) + " && make && make install")
        return True

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python csv-to-apple-dict.py <input.csv> [dict_name]")
        sys.exit(1)
        
    input_csv = sys.argv[1]
    name = sys.argv[2] if len(sys.argv) > 2 else "German IPA"
    
    converter = CSVToAppleDictConverter(input_csv, dict_name=name)
    converter.convert()
