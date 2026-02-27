como crear un github actions para crear un ejecutable de windows a partir de un programa python con pyinstaller
sign applications for windows free for open source apps

https://signpath.org/terms

## Requisitos

py -m pip install --upgrade pip

py -m pip install --upgrade PyInstaller pyinstaller-hooks-contrib

py -m pip install pillow

pip freeze > requirements.txt

para desinstalar todos los módulos
pip freeze > requirements.txt
pip uninstall -r requirements.txt

## Para crear el ejecutable
pyinstaller  --onefile --windowed --icon="src/circulo-negro.ico" --add-data="src/circulo-rojo.ico:img/circulo-rojo.ico" --add-data="src/circulo-negro.ico:img/circulo-rojo.ico"  --collect-all tkinter --collect-all PIL src/capturas.py

