[app]
title = Dino Quest
package.name = dinoquest
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,wav,ogg
version = 1.8
requirements = python3,kivy

orientation = landscape
fullscreen = 1
android.archs = arm64-v8a
android.api = 34
android.minapi = 21
android.accept_sdk_license = True
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 0
