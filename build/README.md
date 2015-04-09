Requirements
------------

To compile into an .exe, install [PyInstaller](https://github.com/pyinstaller/pyinstaller/wiki).

Then to create the installer, install [Inno Setup](http://www.jrsoftware.org/isinfo.php).

Before compiling
----------------

* ``1_compile_qt.bat`` assumes that the path to ``pyrcc4`` and ``pyuic4`` (e.g. ``path_to_python\Lib\site-packages\PyQt4``) is in Windows ``%PATH%`` system variable;
* ``2_compile_exe.bat`` assumes that the path to ``pyinstaller`` (e.g. ``path_to_python\Scripts``) is in Windows ``%PATH%`` system variable.

How to compile
--------------

1. Execute ``1_compile_qt.bat`` (only if you edited any of the ``qt/*.ui`` files);
2. Execute ``2_compile_exe.bat``;
3. Open ``3_compile_installer.iss`` using Inno Setup Compiler and click ``Compile``.