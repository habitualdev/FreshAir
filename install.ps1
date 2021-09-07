#Powershell install script for Fresh Air
#Ensure you run as administrator

Set-ExecutionPolicy Bypass -Scope Process -Force;
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072;
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

C:\ProgramData\chocolatey\bin\RefreshEnv.cmd

#Use choco to install python
choco install python
choco install git

refreshenv

#Install all required python packages
pip install flask
pip3 install --user --upgrade -e git+https://github.com/twintproject/twint.git@origin/master#egg=twint
