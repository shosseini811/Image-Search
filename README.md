# Internet Image Finder

A production-ready tool that helps you find similar images of yourself (or any reference image) across the internet using Microsoft's Bing Visual Search API and face recognition technology.

## Features

- Reverse image search using Bing Visual Search API
- Optional face verification to ensure matches contain the same person
- Concurrent downloads for better performance
- Comprehensive logging
- Progress tracking for long-running operations
- Configurable matching parameters
- Organized output directory for found images

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

3. Copy the environment template and configure your settings:
```bash
cp .env.example .env
```

4. Edit `.env` file and add your Bing Search API key:
```
BING_SEARCH_API_KEY=your_api_key_here
```

## Usage

1. Basic usage:
```python
from image_finder import ImageFinder

finder = ImageFinder()
matches = finder.find_similar_images("path_to_your_image.jpg")
print(f"Found {len(matches)} matching images")
```

2. Disable face verification for general image search:
```python
matches = finder.find_similar_images("path_to_your_image.jpg", verify_faces=False)
```

## Configuration

The following environment variables can be configured in `.env`:

- `BING_SEARCH_API_KEY`: Your Bing Search API key (required)
- `BING_SEARCH_ENDPOINT`: API endpoint (defaults to v7.0)
- `FACE_MATCH_THRESHOLD`: Confidence threshold for face matching (0.0 to 1.0, default: 0.6)
- `OUTPUT_DIR`: Directory for downloaded images (default: ./found_images)

## Logging

Logs are stored in `image_finder.log` with the following features:
- Rotation: 10MB file size
- Retention: 1 week
- Detailed error tracking and operation status

## Legal Considerations

- Ensure compliance with local privacy laws when searching for faces
- Respect copyright and usage rights of found images
- Review Microsoft Bing API terms of service

## Error Handling

The tool includes comprehensive error handling for:
- API failures
- Network issues
- Invalid images
- Face detection problems
- Download errors

## Performance

- Concurrent downloads with ThreadPoolExecutor
- Configurable number of worker threads
- Progress tracking for long operations
- Efficient memory usage with streaming downloads

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.