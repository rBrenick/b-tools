
:: bTools is determined by the current folder name
for %%I in (.) do set bTools=%%~nxI

:: Check if modules folder exists
if not exist %UserProfile%\Documents\maya\modules mkdir %UserProfile%\Documents\maya\modules

:: Delete .mod file if it already exists
if exist %UserProfile%\Documents\maya\modules\%bTools%.mod del %UserProfile%\Documents\maya\modules\%bTools%.mod

:: Create file with contents in users maya/modules folder
(echo|set /p=+ %bTools% 1.0 %CD%\src)>%UserProfile%\Documents\maya\modules\%bTools%.mod

:: end print
echo .mod file created at %UserProfile%\Documents\maya\modules\%bTools%.mod

