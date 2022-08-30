from TubeDownload import DownloadYouTube

if __name__ == "__main__":
    YT_link = input("Please enter the YouTube Link: ")
    video = DownloadYouTube(YT_link)
    if video.valid:
        print()
        print("Which one do you need? \n 1. Video\n 2. Audio\n")

        option = int(input("Please enter valid option: "))

        if option == 1:
            print("\nWhich format do you wish to download?\n")
            all_formats = video.all_available_formats()
            print(all_formats)
            user_format = input("\nPlease select one from above list: ")
            if user_format in all_formats:
                print("Downloading video..")
                video.download_video(user_format)
            else:
                print("Downloading video..")
                video.download_video()
                print("\n\n")
            print(
                "Video is downloaded successfully. Please check your working directory for the file.\n"
            )
        elif option == 2:
            print("Downloading audio...")
            video.download_audio_only()
            print("\n\n")
            print(
                "Audio is downloaded successfully. Please check your working directory for the file.\n"
            )
        print(
            "Thank you for using our services. Please do visit us again.. \N{grinning face}"
        )

    else:
        print(
            "\nWe couldn't find data with the given YouTube URL. Please try back again.. \N{upside-down face}"
        )
