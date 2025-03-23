# Text Cluster Comparison

A tool for analyzing and visualizing textual similarities between two texts. This application identifies and displays clusters (similar passages) between texts, making it useful for comparing different editions, translations, or versions of documents.

## Motivation

The initial idea for this project came from Kristin Mothes and Antje Ziemer, who needed to compare two editions of a Tibetan text in preparation for a research project. A script for detecting identical clusters in two texts was developed. When presented at a Tibetology conference in Oxford, the method garnered significant interest, encouraging its publication.

Texts from different languages and cultures often exist in various editions. This tool is designed to be applicable to texts in different languages and writing systems. The project is continuously being developed to integrate new features.

## Features

- **Text Preprocessing**: Tokenization and optional character replacement
- **Cluster Analysis**: Efficient identification of similar text sequences with adjustable minimum length
- **Comparison Generation**: Detailed analysis of differences and similarities

### Web Application (Dash)

The Dash application provides a user-friendly interface with the following features:

- **Text Input Page**: Enter two texts, titles, and configure preprocessing parameters
- **Analysis Page**:
  - Visualization of clusters (Bubble Plot or Line Plot)
  - Ability to remove unwanted clusters through selection
  - Generation of detailed comparison tables
  - Download results in various formats

## Installation

### Prerequisites

- Python 3.8 or higher

### Option 1: Using Installation Scripts

#### Windows

```
# Clone the repository
git clone https://github.com/username/text-cluster-comparison.git
cd text-cluster-comparison

# Run the installation script
install_on_win.bat

# Start the application
start_on_win.bat
```

#### Linux

```
# Clone the repository
git clone https://github.com/username/text-cluster-comparison.git
cd text-cluster-comparison

# Make scripts executable
chmod +x install_on_linux.sh
chmod +x start_on_linux.sh

# Run the installation script
./install_on_linux.sh

# Start the application
./start_on_linux.sh
```

### Option 2: Manual Installation

```
# Clone the repository
git clone https://github.com/username/text-cluster-comparison.git
cd text-cluster-comparison

# Create and activate virtual environment
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -e .

# Start the application
python scripts/run_app.py
```

### Option 3: Using Docker

#### Build Docker Image

```
# Clone the repository
git clone https://github.com/username/text-cluster-comparison.git
cd text-cluster-comparison

# Build Docker image
docker build -t text-cluster-comparison .

# Run Docker container
docker run -p 8050:8050 text-cluster-comparison
```

Access the application at http://127.0.0.1:8050 in your web browser.

## Usage

1. **Start the Application**: Run the application using one of the methods described in the installation section.
2. **Input Texts**: Navigate to the Input page and enter or paste the two texts you want to compare.
3. **Configure Parameters**: Set preprocessing parameters like tokenization and minimum cluster length.
4. **Analyze**: Click the analyze button to generate the cluster comparison.
5. **Visualize**: Explore the identified clusters through the visualization tools.
6. **Export**: Download the results for further analysis or reporting.

## Project Structure

```
text-cluster-comparison/
├── src/                      # Core modules
│   ├── clustering/           # Cluster identification algorithms
│   ├── preprocessing/        # Text preprocessing functions
│   ├── web/                  # Dash application
│   └── text_example/         # Example text data
├── scripts/                  # Startup scripts
├── tests/                    # Test cases
└── examples/                 # Example data and notebooks
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 Rafael Deichsel

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Contributing

Contributions to this project are welcome. Please feel free to submit issues or pull requests.

## Contact

[Insert Contact Information Here]