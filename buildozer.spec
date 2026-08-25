[app]
title = Reloj Premium
package.name = relojpremium
package.domain = com.diegocruz
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas
version = 1.0.0
requirements = python3,kivy,plyer
orientation = portrait
fullscreen = 1
android.api = 35
android.minapi = 23
android.archs = arm64-v8a,armeabi-v7a
android.allow_backup = True
android.private_storage = True

[buildozer]
log_level = 2
warn_on_root = 1
