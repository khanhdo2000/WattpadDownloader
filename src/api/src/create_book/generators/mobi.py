import subprocess
from io import BytesIO
from pathlib import Path
from tempfile import NamedTemporaryFile

from bs4 import BeautifulSoup

from ..logs import logger
from ..models import Story
from .epub import EPUBGenerator
from .types import AbstractGenerator


class MOBIGenerator(AbstractGenerator):
    """Generates MOBI files by converting from EPUB format.
    
    This generator first creates an EPUB file, then converts it to MOBI
    using calibre's ebook-convert command-line tool.
    """

    def __init__(
        self,
        metadata: Story,
        part_trees: list[BeautifulSoup],
        cover: bytes,
        images: list[list[bytes | None]],
    ):
        self.story = metadata
        self.parts = part_trees
        self.cover = cover
        self.images = images
        
        # Create the EPUB generator
        self.epub_generator = EPUBGenerator(metadata, part_trees, cover, images)
        
        # This will be our temporary MOBI file
        self.mobi_file: NamedTemporaryFile = NamedTemporaryFile(suffix=".mobi", delete=False)

    def compile(self) -> bool:
        """Compile the book by first creating EPUB, then converting to MOBI.
        
        Returns:
            bool: True if compilation successful.
        """
        # First compile the EPUB
        logger.info("Generating EPUB for MOBI conversion...")
        self.epub_generator.compile()
        
        # Get the EPUB bytes
        epub_buffer = self.epub_generator.dump()
        epub_buffer.seek(0)
        
        # Write EPUB to a temporary file
        with NamedTemporaryFile(suffix=".epub", delete=False) as epub_file:
            epub_file.write(epub_buffer.read())
            epub_file_path = epub_file.name
        
        try:
            # Convert EPUB to MOBI using calibre's ebook-convert
            logger.info("Converting EPUB to MOBI using calibre...")
            self._convert_epub_to_mobi(epub_file_path, self.mobi_file.name)
            return True
        except FileNotFoundError:
            logger.error("Calibre's ebook-convert not found. Make sure calibre is installed.")
            raise RuntimeError(
                "MOBI generation requires calibre to be installed. "
                "Please install calibre: https://calibre-ebook.com/download"
            )
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to convert EPUB to MOBI: {e}")
            raise RuntimeError(f"Failed to convert EPUB to MOBI: {e}")
        finally:
            # Clean up temporary EPUB file
            try:
                Path(epub_file_path).unlink()
            except Exception as e:
                logger.warning(f"Could not delete temporary EPUB file: {e}")

    def _convert_epub_to_mobi(self, epub_path: str, mobi_path: str):
        """Convert EPUB file to MOBI format using calibre's ebook-convert.
        
        Args:
            epub_path: Path to the source EPUB file
            mobi_path: Path where the MOBI file should be written
        """
        # Check if ebook-convert is available
        try:
            result = subprocess.run(
                ["ebook-convert", epub_path, mobi_path],
                capture_output=True,
                text=True,
                check=True,
            )
            logger.info(f"Successfully converted EPUB to MOBI: {result.stdout}")
        except FileNotFoundError:
            # Try alternative command (for some installations)
            try:
                result = subprocess.run(
                    ["calibre-convert", epub_path, mobi_path],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                logger.info(f"Successfully converted EPUB to MOBI: {result.stdout}")
            except FileNotFoundError:
                logger.error("Neither ebook-convert nor calibre-convert found")
                raise

    def dump(self) -> BytesIO:
        """Return the MOBI file as a BytesIO buffer.
        
        Returns:
            BytesIO: Buffer containing the MOBI file data
        """
        # Read the MOBI file content
        self.mobi_file.seek(0)
        mobi_content = self.mobi_file.read()
        
        # Create a BytesIO buffer
        buffer = BytesIO(mobi_content)
        
        # Clean up the temporary file
        self.mobi_file.close()
        try:
            Path(self.mobi_file.name).unlink()
        except Exception as e:
            logger.warning(f"Could not delete temporary MOBI file: {e}")
        
        buffer.seek(0)
        return buffer


