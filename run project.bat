@echo off

start powershell -NoExit -Command "$Host.UI.RawUI.WindowTitle = 'emilys_luxury'; & '.\venv\Scripts\activate';  code .;  python manage.py runserver 9000"
