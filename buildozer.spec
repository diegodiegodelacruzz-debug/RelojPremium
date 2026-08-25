[app]

# Nombre de la aplicación
title = Reloj Premium

# Identificador
package.name = relojpremium
package.domain = com.diegocruz

# Código fuente
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas

# Versión
version = 1.0.0

# Dependencias
requirements = python3,kivy,pyjnius,plyer

# Permisos
android.permissions = VIBRATE

# Orientación
orientation = portrait

# Pantalla completa
fullscreen = 1

# Android
android.api = 35
android.minapi = 24

# Solo ARM64 para simplificar la compilación
android.archs = arm64-v8a

# Backup y almacenamiento
android.allow_backup = True
android.private_storage = True

# Aceptar licencias del SDK automáticamente
android.accept_sdk_license = True


[buildozer]

log_level = 2
warn_on_root = 1
