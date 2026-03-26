[app]
title = Dino Quest
package.name = dinoquest
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,wav,ogg
version = 3.0
requirements = python3,kivy==2.3.0,pillow

orientation = landscape
fullscreen = 1
android.archs = arm64-v8a
android.api = 34
android.minapi = 21
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 0
