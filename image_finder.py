import os
import json
import requests
from PIL import Image
import face_recognition
from pathlib import Path
from dotenv import load_dotenv
from loguru import logger
from tqdm import tqdm
from typing import List, Dict, Optional
import concurrent.futures
from io import BytesIO

class ImageFinder:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('BING_SEARCH_API_KEY')
        self.endpoint = os.getenv('BING_SEARCH_ENDPOINT')
        self.face_match_threshold = float(os.getenv('FACE_MATCH_THRESHOLD', 0.1))
        self.output_dir = Path(os.getenv('OUTPUT_DIR', './found_images'))
        self.output_dir.mkdir(exist_ok=True)
        
        if not self.api_key:
            raise ValueError("BING_SEARCH_API_KEY not found in environment variables")
        
        logger.add(
            "image_finder.log",
            rotation="10 MB",
            retention="1 week",
            level="INFO"
        )

    def _load_reference_image(self, image_path: str) -> tuple:
        """Load and encode reference image for face comparison."""
        try:
            reference_image = face_recognition.load_image_file(image_path)
            face_encodings = face_recognition.face_encodings(reference_image)
            
            if not face_encodings:
                raise ValueError("No faces found in the reference image")
                
            return face_encodings[0]
        except Exception as e:
            logger.error(f"Error loading reference image: {str(e)}")
            raise

    def _search_similar_images(self, image_path: str) -> List[Dict]:
        """Perform visual search using Bing API."""
        try:
            headers = {
                'Ocp-Apim-Subscription-Key': self.api_key
            }
            
            with open(image_path, 'rb') as image_file:
                form_data = {
                    'image': ('image', image_file, 'application/octet-stream')
                }
                response = requests.post(
                    self.endpoint,
                    headers=headers,
                    files=form_data
                )
                response.raise_for_status()
                
            results = response.json()
            if 'tags' not in results:
                return []
                
            similar_images = []
            for tag in results['tags']:
                if 'actions' in tag:
                    for action in tag['actions']:
                        if action.get('actionType') == 'VisualSearch':
                            similar_images.extend(action.get('data', {}).get('value', []))
            
            return similar_images
        except Exception as e:
            logger.error(f"Error in visual search: {str(e)}")
            return []

    def _verify_face_match(self, reference_encoding, image_url: str) -> bool:
        """Verify if the face in found image matches reference face."""
        try:
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()
            
            image_data = BytesIO(response.content)
            found_image = face_recognition.load_image_file(image_data)
            found_encodings = face_recognition.face_encodings(found_image)
            
            if not found_encodings:
                return False
                
            # Compare with all faces found in the image
            distances = face_recognition.face_distance([reference_encoding], found_encodings[0])
            return any(distance <= self.face_match_threshold for distance in distances)
            
        except Exception as e:
            logger.warning(f"Error processing image {image_url}: {str(e)}")
            return False

    def _download_image(self, image_url: str, index: int) -> Optional[str]:
        """Download and save matched image."""
        try:
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()
            
            # Save image with index
            image_path = self.output_dir / f"found_image_{index}.jpg"
            with open(image_path, 'wb') as f:
                f.write(response.content)
            return str(image_path)
            
        except Exception as e:
            logger.warning(f"Error downloading image {image_url}: {str(e)}")
            return None

    def find_similar_images(self, reference_image_path: str, verify_faces: bool = True) -> List[str]:
        """
        Find similar images across the internet using the reference image.
        
        Args:
            reference_image_path (str): Path to the reference image
            verify_faces (bool): Whether to verify faces in found images
            
        Returns:
            List[str]: Paths to downloaded matching images
        """
        logger.info(f"Starting image search for: {reference_image_path}")
        
        # Load reference face if face verification is enabled
        reference_encoding = None
        if verify_faces:
            reference_encoding = self._load_reference_image(reference_image_path)
        
        # Perform visual search
        similar_images = self._search_similar_images(reference_image_path)
        logger.info(f"Found {len(similar_images)} potential matches")
        
        matched_images = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            
            for idx, image_data in enumerate(similar_images):
                image_url = image_data.get('contentUrl')
                if not image_url:
                    continue
                
                if verify_faces and reference_encoding is not None:
                    # Verify face match before downloading
                    if not self._verify_face_match(reference_encoding, image_url):
                        continue
                
                futures.append(executor.submit(self._download_image, image_url, idx))
            
            for future in tqdm(concurrent.futures.as_completed(futures), 
                             total=len(futures), 
                             desc="Downloading matches"):
                result = future.result()
                if result:
                    matched_images.append(result)
        
        logger.info(f"Successfully downloaded {len(matched_images)} matching images")
        return matched_images

if __name__ == "__main__":
    # Example usage
    finder = ImageFinder()
    matches = finder.find_similar_images("images.jpeg")
    print(f"Found {len(matches)} matching images. Check {finder.output_dir} directory.") 