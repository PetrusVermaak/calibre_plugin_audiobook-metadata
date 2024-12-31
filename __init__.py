from datetime import date
import io
import subprocess
import os

from calibre.customize import MetadataReaderPlugin
from calibre.ebooks.metadata.book.base import Metadata
from calibre.utils.logging import default_log as log
from PIL import Image
from calibre_plugins.audiobook_metadata.tinytag import TinyTag


class AudioBookPlugin(MetadataReaderPlugin):
    file_types = {"m4b", "m4a"}
    author = "Artur Kupiec"
    contributor = "Petrus Vermaak"

    name = "Read Audiobooks metadata"
    description = "Read metadata from m4b,m4a files, perhaps more in future..."
    version = (0, 1, 1)
    minimum_calibre_version = (7, 0, 0)
    can_be_disabled = False

    def get_duration_ffprobe(self, filepath):
        try:
            cmd = ['ffprobe', '-v', 'quiet', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', filepath]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.stdout.strip():
                return float(result.stdout)
        except Exception as e:
            log.debug(f"FFprobe error: {e}")
        return None

    def get_metadata(self, stream, type) -> Metadata:
        tag = TinyTag.get(filename=stream.name, file_obj=stream, image=True, duration=True)
        log.debug(f"Processing file: {stream.name}")

        title = get_title_form_tag(tag)
        authors = [tag.albumartist, tag.artist, tag.composer]
        meta = Metadata(title, authors)

        if tag.year is not None:
            meta.pubdate = date(int(tag.year), 1, 1)

        image_bytes = tag.get_image()
        if image_bytes is not None:
            image = Image.open(io.BytesIO(image_bytes))
            if image.format is not None:
                format_type = image.format.lower()
                meta.cover_data = (format_type, image_bytes)

        if tag.extra is not None and "copyright" in tag.extra:
            meta.rights = tag.extra["copyright"]

        if tag.genre is not None:
            meta.tags = tuple(tag.genre.split(", "))

        meta.comments = tag.comment
        meta.performer = tag.composer

        # Try to get duration
        duration_seconds = None
        if hasattr(tag, 'duration') and tag.duration is not None:
            duration_seconds = tag.duration
            log.debug(f"Got duration from TinyTag: {duration_seconds}")
        else:
            duration_seconds = self.get_duration_ffprobe(stream.name)
            log.debug(f"Got duration from FFprobe: {duration_seconds}")

        if duration_seconds is not None:
            total_seconds = int(duration_seconds)
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            duration_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            log.debug(f"Formatted duration: {duration_str}")

            try:
                meta.set_user_metadata('#duration', {
                    '#value#': duration_str,
                    '#extra#': None,
                    'datatype': 'text',
                    'is_multiple': None,
                    'name': 'Duration'
                })
                log.debug("Successfully set duration metadata")
            except Exception as e:
                log.debug(f"Error setting duration metadata: {e}")
                # Fallback to comments
                prefix = "Duration: "
                if meta.comments:
                    if prefix not in meta.comments:
                        meta.comments = f"{meta.comments}\n{prefix}{duration_str}"
                else:
                    meta.comments = f"{prefix}{duration_str}"

        return meta


def join_strings_ignore_none(strings, delimiter=' & '):
    return delimiter.join([s for s in strings if s is not None])


def get_title_form_tag(tag):
    title = tag.album or tag.title
    if title is None:
        return None
    title = title.strip()
    if title.endswith(" (Unabridged)"):
        return title[:-12]  # remove exactly " (Unabridged)"
    return title
