# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['Game.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        # Всі Python скрипти гри
        ('Lobby.py', '.'),
        ('Menu.py', '.'),
        ('book.py', '.'),
        ('osnowa.py', '.'),
        ('osnowa_endless.py', '.'),
        ('osnowa_hardcore.py', '.'),
        # Всі картинки
        ('logo.png', '.'),
        ('maus.png', '.'),
        ('nemech.png', '.'),
        ('pz.png', '.'),
        ('Tanks.png', '.'),
        ('Tanks_34.png', '.'),
        ('Mega.png', '.'),
        ('T-26.png', '.'),
    ],
    hiddenimports=['tkinter', 'tkinter.ttk'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='TanksVsGuys',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,        # без чорного вікна консолі
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
