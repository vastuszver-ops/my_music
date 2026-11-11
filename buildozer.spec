[app]
title = My Music Player
package.name = mymusicplayer
package.domain = org.mymusic
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,txt
version = 1.0
requirements = python3,kivy,pyjnius
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
android.api = 33
android.minapi = 24
android.archs = arm64-v8a
