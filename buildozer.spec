[app]
title = My Music Player
package.name = mymusicplayer
package.domain = org.mymusic
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,txt
version = 1.0
requirements = python3==3.13.9,hostpython3==3.13.9,kivy==2.3.1,pyjnius==1.9.0,setuptools,openssl,sqlite3,requests,yt-dlp,certifi,charset-normalizer,idna,urllib3
android.accept_sdk_license=True

[buildozer]
log_level = 2
warn_on_root = 1
android.api = 34
android.minapi = 24
android.archs = arm64-v8a
