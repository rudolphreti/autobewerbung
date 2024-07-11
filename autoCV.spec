# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['main.py'],
             pathex=['.'],
             binaries=[],
             datas=[
                 ('templates', 'templates'),
                 ('data.json', '.'),
                 ('CV_Zeugniss.pdf', '.'),
                 ('CV.pdf', '.'),
                 ('LAP-Zeugnis.pdf', '.'),
                 ('profilfoto.jpg', '.'),
                 ('create_application_files.py', '.'),
                 ('pdf_generator.py', '.')
             ],
             hiddenimports=[
                 'pandas',
                 'jinja2',
                 'werkzeug',
                 'click',
                 'itsdangerous',
                 'lxml',
                 'pyparsing',
                 'email_validator',
                 'babel'
             ],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='autoCV',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True)

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='autoCV')
