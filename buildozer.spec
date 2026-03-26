[app]
title = Dino Quest
package.name = dinoquest
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,wav,ogg
version = 1.2
requirements = python3,kivy==2.3.0,pillow,android,certifi

orientation = landscape
fullscreen = 1
android.archs = arm64-v8a
android.api = 34
android.minapi = 24
android.sdk = 34
android.ndk = 25c
android.accept_sdk_license = True
android.allow_backup = True
android.private_storage = True

[buildozer]
log_level = 2
warn_on_root = 0
