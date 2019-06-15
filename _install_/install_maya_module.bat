
:: b_tools is determined by the current folder name
for %%I in (.) do set b_tools=%%~nxI
SET CLEAN_b_tools=%b_tools:-=_%

:: Check if modules folder exists
if not exist %UserProfile%\Documents\maya\modules mkdir %UserProfile%\Documents\maya\modules

:: Delete .mod file if it already exists
if exist %UserProfile%\Documents\maya\modules\%b_tools%.mod del %UserProfile%\Documents\maya\modules\%b_tools%.mod

:: Create file with contents in users maya/modules folder
(echo|set /p=+ %b_tools% 1.0 %CD%\_install_ & echo; & echo icons: ..\%CLEAN_b_tools%\icons)>%UserProfile%\Documents\maya\modules\%b_tools%.mod

:: end print
echo .mod file created at %UserProfile%\Documents\maya\modules\%b_tools%.mod


