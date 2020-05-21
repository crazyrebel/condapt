@echo off
setlocal enabledelayedexpansion
rem echo %~dp0
rem set miniconda=Miniconda3-py38_4.8.2-Windows-x86_64.exe
set miniconda=Miniconda3-latest-Windows-x86_64.exe
set anaconda=Anaconda3-2020.02-Windows-x86_64.exe
set minicondaMirror=https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/%miniconda%
set anacondaMirror=https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/%anaconda%
set conda=%miniconda%
set condaMirror=%minicondaMirror%
set condaType=1
set input=y
set selectedConda=0
set installDir=D:\ProgramData\Miniconda3

goto :DownloadConda

:SelectConda
if "!selectedConda!"=="0" (
    set /p condaType="Select conda miniconda([1]), anaconda(2):"
    if not "!condaType!"=="1" (
        if not "!condaType!"=="2" (
            echo enter 1 or 2
            goto :SelectConda
        )
    )
    set selectedConda=1
    set conda=%miniconda%
    if "!condaType!"=="2" (
        set conda=%anaconda%
        set condaMirror=%anacondaMirror%
        set installDir=D:\ProgramData\Anaconda3
    )
)
goto :eof

:DownloadConda
set /p input="Download conda?([y]/n):"
if %input%==y (
    call :SelectConda
    if "!condaType!"=="1" (
        echo Download miniconda
    ) else if "!condaType!"=="2" (
        echo Download anaconda
    )

    bitsadmin /transfer "download conda" /download /priority foreground !condaMirror! %~dp0!conda!
)

:InstallConda
set input=y
set /p input="Install conda?([y]/n):"
if %input%==y (
    call :SelectConda
    if "!condaType!"=="1" (
        echo Install miniconda
    ) else if "!condaType!"=="2" (
        echo Install anaconda
    )
    call %~dp0!conda!
)

:InstallEnv
call :SelectConda
set defaultInstallDir=%installDir%
set /p installDir="Input conda install dir (Default dir is %defaultInstallDir%):"
call %installDir%\Scripts\activate.bat %installDir%
call %installDir%\python.exe %~dp0/install.py

pause