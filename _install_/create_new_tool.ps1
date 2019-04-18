
# This script takes the current tool directory
# clones it to another folder with the same parent directory
# renames all the instances of the current ToolName with the prompted new name
# searches through files and replaces in there as well

$TOOL_PACKAGES_FOLDER = (Get-Item -Path "..\").FullName
$CURRENT_bTools = "bTools"
$CURRENT_TOOL_FOLDER = (Get-Item -Path ".").FullName
$NEW_bTools = Read-Host -Prompt 'New Tool Name'
$NEW_TOOL_FOLDER = $TOOL_PACKAGES_FOLDER + "\" + $NEW_bTools

echo ""

if (([string]::IsNullOrEmpty($NEW_bTools)))
{
    echo "No tool name was given. Exiting...`n "
    exit
}

# Clone to new folder
Copy-Item -Path $CURRENT_TOOL_FOLDER -Recurse -Destination $NEW_TOOL_FOLDER -Container


# Remove .git folder
$GIT_FOLDER = $NEW_TOOL_FOLDER + "\.git"
if(Test-Path -Path $GIT_FOLDER ){
    Get-ChildItem -Path $GIT_FOLDER -Recurse | Remove-Item -force -recurse
    Remove-Item $GIT_FOLDER -Force
}


# Rename files in folder
Get-ChildItem $NEW_TOOL_FOLDER -recurse | 
Foreach-Object {
    if ($_.Name -like '*' + $CURRENT_bTools + '*') {
        Rename-Item -Path $_.PSPath -NewName $_.Name.replace($CURRENT_bTools, $NEW_bTools)
    }
    
}

# Find instances of bTools in files and replace them with the new tool name
Get-ChildItem $NEW_TOOL_FOLDER -recurse -File | 
Foreach-Object {
    
    $_.FullName
    
    ((Get-Content -path $_.FullName -Raw) -replace $CURRENT_bTools, $NEW_bTools) | Set-Content -Path $_.FullName
    ((Get-Content -path $_.FullName -Raw) -replace "bTools", $NEW_bTools) | Set-Content -Path $_.FullName
    
}

echo ""
echo "New Tool: '$NEW_bTools' has been created at '$NEW_TOOL_FOLDER'"


# pause before exit
# cmd /c pause | out-null

