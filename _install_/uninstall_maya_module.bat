
:: bTools is determined by the current folder name
for %%I in (.) do set bTools=%%~nxI

:: Check if modules folder exists
if not exist %UserProfile%\Documents\maya\modules mkdir %UserProfile%\Documents\maya\modules

:: Delete .mod file if it already exists
del %UserProfile%\Documents\maya\modules\%bTools%.mod

:: end print 
echo .mod file removed from %UserProfile%\Documents\maya\modules\%bTools%.mod

