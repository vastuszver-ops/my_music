[app]
title = My Music Player
package.name = mymusicplayer
package.domain = org.mymusic
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,txt
version = 1.0
requirements = python3,kivy,pyjnius,requests,yt-dlp,ffmpeg

[buildozer]
log_level = 2
warn_on_root = 1
android.api = 34
android.minapi = 24
android.archs = arm64-v8a
