# -*- mode: python -*-

block_cipher = None


a = Analysis(['WordofTheDay.py'],
             pathex=['E:\\我的文件\\文件\\python教學\\wordoftheday'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='WordofTheDay',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False )
