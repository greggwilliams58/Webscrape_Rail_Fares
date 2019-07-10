# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['RME_webscrape.py'],
             pathex=['C:\\Users\\gwilliams\\Documents\\GitHub\\RME_Rail_Fares\\RME_Rail_Fares'],
             binaries=[],
             datas=[('C:\\Users\\gwilliams\Documents\GitHub\RME_Rail_Fares\RME_Rail_Fares/*.xlsx','Route_and_times_metadata')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='RME_webscrape',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='RME_webscrape')
