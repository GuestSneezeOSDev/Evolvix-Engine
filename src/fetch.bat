@echo off
echo Evolvix Fetch is fetching files
git clone https://github.com/Vortex-Engine/vortex-engine
cd vortex-engine\sp\game\mod-hl2
echo Installing files
xcopy /E /I materials %USERPROFILE%\evolvix\sp
xcopy /E /I models %USERPROFILE%\evolvix\sp
cd ..\..\..\..
rmdir /S /Q vortex-engine
echo Complete
