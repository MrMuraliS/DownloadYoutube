from pytube import YouTube


class DownloadYouTube:

    def __init__(self, link):
        self.link = input("Please provide the link: ")
        try:
            self.yt = YouTube(self.link)
            self.formats = self.yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
        except Exception as error:
            print(error)

    def all_available_formats(self):
        return [video.resolution for video in self.formats]

    def download_video(self, required_format: str = "720p"):
        self.formats.get_by_resolution(required_format).download()

    def download_audio_only(self):
        self.yt.streams.filter(only_audio=True).desc().first().download()

