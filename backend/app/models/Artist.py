from typing import List
class Album:
    albums: List[str]  # References to other albums, e.g., ["/Albums/album1", "/Albums/album2"]
    description: str
    image_url: str  # URL for the album's image
    name: str