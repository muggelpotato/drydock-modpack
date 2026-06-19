@echo off
setlocal enabledelayedexpansion

set "SCRIPT_DIR=%~dp0"
set "PACK_DIR=%SCRIPT_DIR%pack"
set "BUILDS_DIR=%SCRIPT_DIR%builds"

if not exist "%BUILDS_DIR%" (
    mkdir "%BUILDS_DIR%"
)

python "%SCRIPT_DIR%scripts\enforce_client_side.py"

pushd "%PACK_DIR%"
packwiz update --all -y
packwiz refresh
packwiz modrinth export
move /y *.mrpack "%BUILDS_DIR%"
popd