# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['NRE_webscrape.py'],
             pathex=['C:\\Users\\gwilliams\\Documents\\GitHub\\RME_Rail_Fares\\RME_Rail_Fares'],
             binaries=[],
             datas=[
			 ('C:\\Users\\gwilliams\\Documents\\GitHub\\RME_Rail_Fares\\1_READ_ME_Instructions\\Instructions for use.txt','1_READ_ME_Instructions'),
			 ('C:\\Users\\gwilliams\\Documents\\GitHub\\RME_Rail_Fares\\2_Route_and_times_metadata\\route_and_time_metadata.xlsx','2_Route_and_times_metadata'),
			 ('C:\\Users\\gwilliams\\Documents\\GitHub\\RME_Rail_Fares\\3_Data_goes_here\\Placeholder for data.txt','3_Data_goes_here'),
			 ('C:\\Users\\gwilliams\\Documents\\GitHub\\RME_Rail_Fares\\3_Data_goes_here\\appended_data\\appended_data_for_intial_run.csv','3_Data_goes_here\\appended_data')
			 
			 ],
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
          name='NRE_webscrape',
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
               name='NRE_webscrape')
