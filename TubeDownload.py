import shutil
import sys

from pytube import YouTube


def display_progress_bar(
    bytes_received: int, filesize: int, ch: str = "█", scale: float = 0.55
) -> None:
    """Display a simple, pretty progress bar.

    Example:
    ~~~~~~~~
    PSY - GANGNAM STYLE(강남스타일) MV.mp4
    ↳ |███████████████████████████████████████| 100.0%

    :param int bytes_received:
        The delta between the total file size (bytes) and bytes already
        written to disk.
    :param int filesize:
        File size of the media stream in bytes.
    :param str ch:
        Character to use for presenting progress segment.
    :param float scale:
        Scale multiplier to reduce progress bar size.

    """
    columns = shutil.get_terminal_size().columns
    max_width = int(columns * scale)

    filled = int(round(max_width * bytes_received / float(filesize)))
    remaining = max_width - filled
    progress_bar = ch * filled + " " * remaining
    percent = round(100.0 * bytes_received / float(filesize), 1)
    text = (
        f" ↳ |{progress_bar}| "
        f"{round(bytes_received / 1000 / 1000, 2)} MB of {round(filesize / 1000 / 1000, 2)} MB | {percent}%\r"
    )
    sys.stdout.write(text)
    sys.stdout.flush()


def on_progress(
    stream, chunk: bytes, bytes_remaining: int
) -> None:  # pylint: disable=W0613
    filesize = stream.filesize
    bytes_received = filesize - bytes_remaining
    display_progress_bar(bytes_received, filesize)


class DownloadYouTube:
    def __init__(self, link):
        self.target = None
        self.link = link
        try:
            self.yt = YouTube(self.link, on_progress_callback=on_progress)
            self.formats = (
                self.yt.streams.filter(progressive=True, file_extension="mp4")
                .order_by("resolution")
                .desc()
            )
            self.valid = True
        except Exception as error:
            print(error)
            self.valid = False

    def all_available_formats(self):
        """
        This will return all the available formats to user, so user can select which one to download.
        :return:
        """

        self.target = {}
        for video in self.formats:
            if video.resolution not in self.target:
                self.target[video.resolution] = video.itag
            else:
                self.target[video.resolution] = video.itag
        return list(self.target.keys())

    def download_video(self, required_format: str = "720p"):
        """
        This method does download the file based on the format that user has provided,
        by default it will try to download 720p.
        :param required_format:
        :return:
        """
        # self.formats.get_by_resolution(required_format).download()
        # self.formats.first().download()
        self.formats.get_by_itag(self.target.get(required_format, "360p")).download()

    def download_audio_only(self):
        """
        This method will download the Audio only file.
        :return:
        """
        self.yt.streams.filter(only_audio=True).desc().first().download()
