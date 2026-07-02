# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import (
    collect_submodules,
    collect_data_files,
    collect_dynamic_libs
)

hidden_imports = (
    collect_submodules("PySide6")
    + collect_submodules("google")
    + collect_submodules("google.genai")
    + collect_submodules("cryptography")
    + collect_submodules("certifi")
    + collect_submodules("requests")
    + collect_submodules("httpx")
    + collect_submodules("httpcore")
    + collect_submodules("anyio")
    + collect_submodules("sniffio")
    + collect_submodules("websockets")
)

datas = [
    ("assets", "assets"),
    ("engine", "engine"),
]

datas += collect_data_files("certifi")
datas += collect_data_files("google.genai")

binaries = []
binaries += collect_dynamic_libs("cryptography")

a = Analysis(
    ["main.py"],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='AI-Mate',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,   # ← GUIならFalse
    icon='assets/icon.ico'
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="AI-Mate",
)