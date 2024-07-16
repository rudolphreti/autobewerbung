# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['C:\\Users\\Miko\\Desktop\\autoCV\\main.py'],
    pathex=['C:\\Users\\Miko\\Desktop\\autoCV'],
    binaries=[],
    datas=[
        ('C:\\Users\\Miko\\Desktop\\autoCV\\data.json', '.'),
        ('C:\\Users\\Miko\\Desktop\\autoCV\\templates\\*', 'templates'),
        ('C:\\Users\\Miko\\Desktop\\autoCV\\CV_Zeugnis.pdf', '.'),
        ('C:\\Users\\Miko\\Desktop\\autoCV\\LAP-Zeugnis.pdf', '.'),
        ('C:\\Users\\Miko\\Desktop\\autoCV\\profilfoto.jpg', '.'),
        ('C:\\Users\\Miko\\Desktop\\autoCV\\CV.pdf', '.'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)
