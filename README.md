# German IPA Dictionary for macOS

A German dictionary (~ 364903 entries) with IPA pronunciations for the native macOS Dictionary app. 

This project converts a CSV file of German words and their IPA pronunciations into the Apple Dictionary format.

## Installation

### Pre-built Apple Dictionary
For most users, installing the pre-built dictionary is the recommended method.

1.  **Download:** Go to the [Releases page](https://github.com/vpnry/de-ipa-appledictionary/releases) and download the `DE_IPA.dictionary.zip` file.
2.  **Unzip:** Unzip the downloaded file, which will create a `DE_IPA.dictionary` file.
3.  **Install:** Move `DE_IPA.dictionary` to your `~/Library/Dictionaries/` folder.
    *You can open Finder, press `Cmd+Shift+G`, and paste `~/Library/Dictionaries/` to navigate there directly.*
4.  **Activate:**
    - Open the **Dictionary.app**.
    - Go to **Dictionary > Settings...** (or **Preferences...**).
    - Scroll down and check the box next to **"DE_IPA"** to enable it.

You can now look up German words and see their IPA pronunciation directly in the Dictionary app.

### Yomitan Dictionary

For users who want to use the dictionary with [Yomitan](https://github.com/yomidevs/yomitan), you can download the `yomitan_de_ipa.zip` file from the [Releases page](https://github.com/vpnry/de-ipa-appledictionary/releases) and use it to import it in the Yomitan settings.

---

## Building from Source

For developers who want to build or customize the dictionary from the source.

### Prerequisites

1.  **Python 3:** Required to execute the conversion script.
2.  **Apple Dictionary Development Kit:**
    - Download it from [Apple Developer Downloads](https://developer.apple.com/download/more/) (requires an Apple ID).
    - Search for "Dictionary Development Kit" and download it.
    - The build scripts assume it is located in `/Applications/Utilities/Dictionary Development Kit/`.

### Data Source

The pronunciation data is from the [German IPA Pronunciation Dictionary](https://www.kaggle.com/datasets/cdminix/german-ipa-pronunciation-dictionary) on Kaggle.

-   **License:** CC0: Public Domain

### Build Steps

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/vpnry/de-ipa-appledictionary.git
    cd de-ipa-appledictionary
    ```

2.  **Prepare the data:**
    Unzip the `de_word_ipa.csv.zip` file to extract the CSV data.
    ```bash
    unzip de_word_ipa.csv.zip
    ```

3.  **Run the conversion script:**
    This script generates a `GermanIPADictionary` directory containing the necessary project files (XML, CSS, Makefile).
    ```bash
    python3 csv-to-apple-dict.py de_word_ipa.csv "DE_IPA"
    ```

4.  **Build the dictionary:**
    Navigate into the generated directory and run `make`.
    ```bash
    cd GermanIPADictionary
    make
    ```
    This creates the `DE_IPA.dictionary` file inside the `objects/` sub-directory.

5.  **Install the dictionary:**
    You can either install the dictionary using a `make` command or by copying it manually.

    -   **Option A (Recommended):** Use the `make install` command.
        ```bash
        make install
        ```

    -   **Option B:** Copy the dictionary manually.
        ```bash
        cp -r ./objects/DE_IPA.dictionary ~/Library/Dictionaries/
        ```

6.  **Activate the dictionary:**
    Restart the **Dictionary.app**, open its settings, and enable **"DE_IPA"**.

### Script Details

The `csv-to-apple-dict.py` script performs the following actions:
-   Parses the input CSV file using `csv.DictReader`.
-   Sanitizes text to ensure it is valid XML, which is essential for Apple's build tools.
-   Generates a styled `MyDictionary.css` that displays the IPA pronunciation in a gray box.
-   Creates a `Makefile` configured to automate the build and installation process.

#### Generated XML Structure Preview

Here is an example of the XML entry generated for the word "Hallo":
```xml
<d:entry id="Hallo_0" d:title="Hallo">
  <d:index d:value="Hallo"/>
  <div class="entry">
    <h1>Hallo</h1>
    <span class="ipa">[haˈloː]</span>
  </div>
</d:entry>
```


### For Yomitan

```bash
npm install yomichan-dict-builder

node yomitan_export_ipa_dict.js
```


## License

The data used in this dictionary is under the **CC0: Public Domain** license.

The Python script and associated project files are generated with Google `gemini`
