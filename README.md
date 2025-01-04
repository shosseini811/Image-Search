# Internet Image Finder

A Python tool that finds similar images across the internet using Microsoft's Bing Visual Search API and face recognition technology. It can optionally verify faces to ensure the found images contain the same person as your reference image.

## Features

- Visual search using Bing Visual Search API
- Face verification using face_recognition library
- Concurrent image downloads with progress tracking
- Comprehensive logging system
- Configurable matching parameters
- Organized output directory structure

## Prerequisites

- Python 3.8+
- Microsoft Azure account with Bing Search API access
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Image-Search.git
cd Image-Search
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables:
```bash
cp .env.example .env
```

4. Edit `.env` file with your configuration:
```
BING_SEARCH_API_KEY=your_api_key_here
BING_SEARCH_ENDPOINT=your_endpoint_here
FACE_MATCH_THRESHOLD=0.1
OUTPUT_DIR=./found_images
```

## Usage

Basic usage with face verification (default):
```python
from image_finder import ImageFinder

finder = ImageFinder()
matches = finder.find_similar_images("reference_image.jpg")
print(f"Found {len(matches)} matching images. Check {finder.output_dir} directory.")
```

Search without face verification:
```python
matches = finder.find_similar_images("reference_image.jpg", verify_faces=False)
```

## Configuration

Environment variables in `.env`:

- `BING_SEARCH_API_KEY` (required): Your Bing Search API key
- `BING_SEARCH_ENDPOINT` (required): Bing Visual Search API endpoint
- `FACE_MATCH_THRESHOLD` (optional): Face matching confidence threshold (default: 0.1)
- `OUTPUT_DIR` (optional): Directory for downloaded images (default: ./found_images)

## Logging

The application uses loguru for logging:
- Log file: `image_finder.log`
- Rotation: 10 MB
- Retention: 1 week
- Log level: INFO

## Error Handling

The tool includes comprehensive error handling for:
- Missing API credentials
- Image loading failures
- Face detection issues
- Network and API errors
- Download failures

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.