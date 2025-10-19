from io import BytesIO

from bs4 import BeautifulSoup
from ebooklib import epub
from re import sub

from ..logs import logger
from ..models import Story
from .types import AbstractGenerator


class EPUBGenerator(AbstractGenerator):
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

        self.book: epub.EpubBook = epub.EpubBook()

    def _get_valid_language_code(self) -> str:
        """Get a valid ISO language code with fallback handling."""
        # Language name to ISO 639-1 code mapping
        language_map = {
            "English": "en",
            "Spanish": "es", 
            "French": "fr",
            "German": "de",
            "Italian": "it",
            "Portuguese": "pt",
            "Russian": "ru",
            "Chinese": "zh",
            "Japanese": "ja",
            "Korean": "ko",
            "Arabic": "ar",
            "Hindi": "hi",
            "Dutch": "nl",
            "Swedish": "sv",
            "Norwegian": "no",
            "Danish": "da",
            "Finnish": "fi",
            "Polish": "pl",
            "Czech": "cs",
            "Hungarian": "hu",
            "Romanian": "ro",
            "Bulgarian": "bg",
            "Croatian": "hr",
            "Serbian": "sr",
            "Slovak": "sk",
            "Slovenian": "sl",
            "Estonian": "et",
            "Latvian": "lv",
            "Lithuanian": "lt",
            "Greek": "el",
            "Turkish": "tr",
            "Hebrew": "he",
            "Thai": "th",
            "Vietnamese": "vi",
            "Indonesian": "id",
            "Malay": "ms",
            "Tagalog": "tl",
            "Filipino": "fil",
            "Ukrainian": "uk",
            "Belarusian": "be",
            "Macedonian": "mk",
            "Albanian": "sq",
            "Maltese": "mt",
            "Icelandic": "is",
            "Irish": "ga",
            "Welsh": "cy",
            "Basque": "eu",
            "Catalan": "ca",
            "Galician": "gl"
        }
        
        # Get language from story metadata
        language = self.story.get("language", {}).get("name", "")
        logger.info(f"Language from API: {repr(language)}")
        
        # Handle empty, None, or invalid language
        if not language or language.strip() == "":
            logger.warning("Language field is empty or missing, defaulting to 'en'")
            return "en"
        
        # Clean the language string
        language = language.strip()
        
        # Check if it's already a valid ISO code (2-3 characters)
        if len(language) in [2, 3] and language.isalpha():
            logger.info(f"Using language code as-is: {language}")
            return language.lower()
        
        # Try to map language name to ISO code
        mapped_language = language_map.get(language, language)
        if mapped_language != language:
            logger.info(f"Mapped '{language}' to '{mapped_language}'")
            return mapped_language
        
        # If we can't map it, log warning and default to English
        logger.warning(f"Unknown language '{language}', defaulting to 'en'")
        return "en"

    def add_metadata(self):
        """Add metadata to epub."""
        self.book.add_author(self.story["user"]["username"])

        self.book.add_metadata("DC", "title", self.story["title"])
        self.book.add_metadata("DC", "description", self.story["description"])
        self.book.add_metadata("DC", "date", self.story["createDate"])
        self.book.add_metadata("DC", "modified", self.story["modifyDate"])
        
        # Handle language with validation and fallback
        language = self._get_valid_language_code()
        self.book.add_metadata("DC", "language", language)

        self.book.add_metadata(
            None, "meta", "", {"name": "tags", "content": ", ".join(self.story["tags"])}
        )
        self.book.add_metadata(
            None,
            "meta",
            "",
            {"name": "mature", "content": str(int(self.story["mature"]))},
        )
        self.book.add_metadata(
            None,
            "meta",
            "",
            {"name": "completed", "content": str(int(self.story["completed"]))},
        )

    def add_cover(self):
        """Add cover to epub."""
        self.book.set_cover("cover.jpg", self.cover)
        cover_chapter = epub.EpubHtml(
            file_name="titlepage.xhtml",  # Standard for cover page
        )
        cover_chapter.set_content('<img src="cover.jpg">')
        self.book.add_item(cover_chapter)

    def add_chapters(self):
        """Add chapters to epub, replacing references to image urls to static image paths if images are provided during initialization."""
        chapters = []

        for idx, (part, tree) in enumerate(zip(self.story["parts"], self.parts)):
            chapter = epub.EpubHtml(
                title=sub(r'[\x00-\x1F\x7F]', '', part["title"]), file_name=f"{idx}_{part['id']}.xhtml" # Removes control characters from chapter title
            )

            if self.images:
                for img_idx, (img_data, img_tag) in enumerate(
                    zip(self.images[idx], tree.find_all("img"))
                ):
                    path = f"static/{idx}_{part['id']}/{img_idx}.jpeg"
                    img = epub.EpubImage(
                        media_type="image/jpeg", content=img_data, file_name=path
                    )
                    self.book.add_item(img)

                    img_tag["src"] = path

            chapter.set_content(tree.prettify())
            self.book.add_item(chapter)
            chapters.append(chapter)

        # ! Review, are these needed? #11
        self.book.toc = chapters

        # Thanks https://github.com/aerkalov/ebooklib/blob/master/samples/09_create_image/create.py
        self.book.add_item(epub.EpubNcx())
        self.book.add_item(epub.EpubNav())

        # create spine
        self.book.spine = ["nav"] + chapters

    def compile(self):
        self.add_metadata()
        self.add_cover()
        self.add_chapters()
        return True

    def dump(self) -> BytesIO:
        # Thanks https://stackoverflow.com/a/75398222
        buffer = BytesIO()
        epub.write_epub(buffer, self.book)

        buffer.seek(0)

        return buffer
