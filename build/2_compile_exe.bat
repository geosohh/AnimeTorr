IF EXIST pyinstaller (
    RD /S /Q pyinstaller\build
    RD /S /Q pyinstaller\dist
) ELSE (
    MD pyinstaller
)

::debug only -  to check stdout/stderr, replace 'windowed' with 'console', run .exe from cmd
pyinstaller --name="AnimeTorr" ^
            --onedir ^
            --windowed ^
            --icon="icon.ico" ^
            --clean ^
            --noupx ^
            --specpath="pyinstaller" ^
            --workpath="pyinstaller/build" ^
            --distpath="pyinstaller/dist" ^
            --version-file="version_info.txt" ^
            "../animetorr/main.py"

RD /S /Q pyinstaller\build
COPY "..\animetorr\dbTemplate.db" "pyinstaller\dist\AnimeTorr\"
COPY "..\animetorr\cacert.pem" "pyinstaller\dist\AnimeTorr\"

::It still works if AnimeTorr.exe.manifest is deleted, but will show error messages...
::DEL /s pyinstaller\dist\AnimeTorr\*.manifest