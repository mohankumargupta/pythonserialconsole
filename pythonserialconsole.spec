# -*- mode: python -*-
from kivy.deps import sdl2,glew

block_cipher = None


a = Analysis(['pythonserialconsole.py'],
             pathex=['C:\\Users\\mohan\\Developer\\pythonserialconsole'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz, Tree('C:\\Users\\mohan\\Developer\\pythonserialconsole'),
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
          name='pythonserialconsole',
          debug=False,
          strip=False,
          upx=True,
          console=False )