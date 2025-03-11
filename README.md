# migTool
Automated URL redirection mapping tool for website migrations. Uses multiple similarity algorithms to match 404 URLs with the best live counterparts.

## Features

- 404 Status Verification: Checks which URLs are truly 404 before processing.
- Data Cleaning: Removes duplicates and unnecessary URL parameters.
- Advanced Matching Algorithms:
  - Fuzzy Matching
  - Levenshtein Distance
  - Jaccard Similarity
  - Hamming Distance
  - Ratcliff/Obershelp
  - Tversky Index
  - Spacy NLP
  - TF-IDF Vectorization
  - Jaro-Winkler Similarity
  - BERTopic Clustering
- Scoring System: Aggregates results from multiple algorithms to determine the best redirect.
- Excel Output: Saves the final redirection mapping as an Excel file.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/URL-Redirect-Migrator.git
   cd URL-Redirect-Migrator
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate  # On Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Prepare two Excel files:
   - One containing 404 URLs that need redirection.
   - One containing Live URLs to which redirections should be mapped.

2. Run the script:
   ```bash
   python redirect_mapper.py
   ```

3. Follow the prompts to select the appropriate Excel files and sheets.

4. The script will generate an output Excel file containing the best redirection mapping.

## Output Example

The script generates an Excel file with two sheets:
- Mapping: Full algorithm analysis with scores.
- Redirects: Cleaned final redirection list.

## Dependencies

- Python 3.8+
- pandas, numpy, httpx, fuzzywuzzy, Levenshtein, scipy, spacy, joblib, scikit-learn, bertopic, jellyfish, difflib

## Contributing

Feel free to fork this project and submit pull requests.

## License

This project is licensed under the MIT License.

