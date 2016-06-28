@echo off
echo.Welcome to UML Parser,

if "%~1"=="" (
	goto :eof
)

if "%~2"=="" (
	goto :eof
)

if not "%~3"=="" (
    goto :eof
) 
echo Class Diagram Image will generate on path %1 with name as %2
python %Uml_Parser%Uml_Parser.py %1 %2	