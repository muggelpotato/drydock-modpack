@echo off
setlocal enabledelayedexpansion

set "SCRIPT_DIR=%~dp0"
set "PACK_DIR=%SCRIPT_DIR%pack"
set "BUILDS_DIR=%SCRIPT_DIR%builds"

if not exist "%BUILDS_DIR%" (
    mkdir "%BUILDS_DIR%"
)

pushd "%PACK_DIR%"
packwiz refresh
packwiz modrinth export
move /y *.mrpack "%BUILDS_DIR%"
popd