
[app]
title = Dino Quest
package.name = dinoquest
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy

orientation = landscape
osx.python_version = 3
osx.kivy_version = 1.9.1
fullscreen = 1
android.archs = arm64-v8a
android.allow_backup = True
android.api = 31
android.minapi = 21
android.sdk = 31
android.ndk = 25b
android.private_storage = True

[buildozer]
log_level = 2
warn_on_root = 1
