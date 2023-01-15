# YTD
youtube downloader

I'm a fan of vtuber, but the vtuber I subscribe to always stream suddenly and then delete the stream
So I made this to keep the flow going while I was sleeping!
Oh btw, she is a Taiwan vtuber, here is the link
https://www.youtube.com/channel/UCeeUqiYJFwJSuFkfxHKwASQ

this work on win10 and need chrome!!

base on [yt-dlp](https://github.com/yt-dlp/yt-dlp)

need download [ffmpeg](https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip) to work

## package version

| name              | version  |
|-------------------|----------|
| pyqt              | 5.15.7   |
| beautifulsoup4    | 4.11.1   |
| ffmpeg            | 4.2.2    |
| python            | 3.7.13   |
| yt-dlp            | 2022.9.1 |
| selenium          | 3.141.0  |
| webdriver_manager | 3.8.3    |
| pyinstaller       | 5.3      |

## English


this is a python base win10/win11 app for monitor the youtube chennel you add

now you can:

1. monitor channel and auto download
2. member only download support(if you have chrome and is member)
3. merge video and audio
4. convert file to video:[ mkv / webm / mp4 / avi / flv / mov / ts ] audio:[ ogg / mp3 ]

## 中文


這是一個給win10/win11的YT頻道監控下載程式

現在有的功能:

1. 監控頻道並自動下載
2. 會員頻道下載支持(如果你有在chrome上登錄會員)
3. 可以將音軌與影片合併
4. 可以將檔案轉換為 影片:[ mkv / webm / mp4 / avi / flv / mov / ts ] 音軌:[ ogg / mp3 ]

# exe Download (已打包程式下載)
 https://drive.google.com/file/d/1r54anYFI3Bc4WlMyvbP1wwmXioSep3Aq/view?usp=share_link
# HOW TO PACK?(如何打包)
use cmd and execute the command(在環境下cmd使用以下指令)
```
pyinstaller --name=YTD --icon=icon.ico --upx-exclude=vcruntime140.dll --noconfirm --hidden-import=Cryptodome --hidden-import=mutagen --hidden-import=brotli --hidden-import=certifi --hidden-import=websockets --collect-submodules=websockets --exclude-module=youtube_dl --exclude-module=youtube_dlc --exclude-module=test --exclude-module=ytdlp_plugins --exclude-module=devscripts -w .\main.py

```
download [ffmpeg](https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip)
and unzip it in ./dist/YTD/
(下載[ffmpeg](https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip)
並且解壓縮在路徑 ./dist/YTD/ )

# PS

download will save 3 file , the description and the thumbnail(下載會同時載3種檔案,影片描述跟略縮圖):
1. audio only(音軌)+description(影片描述)+thumbnail(略縮圖)
2. video only(視訊))+description(影片描述)+thumbnail(略縮圖)
3. video+audio(影片))+description(影片描述)+thumbnail(略縮圖)

and if stream start download it 0% download is normal,because no end time so can't get %(如果下載直播保持0%是正常的,因為無法得知直播結束時間做計算)

after the stream download finish it need some time to merge,some computer can't merge so you can also use other editor to merge the audio only and video only
(在下載直播結束後影片需要時間做影音合併,有些電腦無法完成合併可以使用其他影音編輯器合併音軌與視訊)





