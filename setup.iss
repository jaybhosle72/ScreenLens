[Setup]
AppName=ScreenLens
AppVersion=1.0
AppPublisher=Jay Bhosle
DefaultDirName={userappdata}\ScreenLens
DefaultGroupName=ScreenLens
OutputDir=Releases
OutputBaseFilename=ScreenLens-Installer
Compression=lzma2
SolidCompression=yes
SetupIconFile=app.ico
UninstallDisplayIcon={app}\app.ico

[Files]
Source: "main.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "overlay.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "ocr_engine.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "capture.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "clipboard_utils.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "app.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "run_silent.vbs"; DestDir: "{app}"; Flags: ignoreversion
Source: "ui\*"; DestDir: "{app}\ui"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\ScreenLens"; Filename: "wscript.exe"; Parameters: """{app}\run_silent.vbs"" ""{app}\main.py"""; IconFilename: "{app}\app.ico"; WorkingDir: "{app}"
Name: "{userdesktop}\ScreenLens"; Filename: "wscript.exe"; Parameters: """{app}\run_silent.vbs"" ""{app}\main.py"""; IconFilename: "{app}\app.ico"; WorkingDir: "{app}"; Tasks: desktopicon
; --- Auto Start with Windows ---
Name: "{userstartup}\ScreenLens"; Filename: "wscript.exe"; Parameters: """{app}\run_silent.vbs"" ""{app}\main.py"""; IconFilename: "{app}\app.ico"; WorkingDir: "{app}"; Tasks: startupicon

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Additional icons:"
Name: "startupicon"; Description: "Automatically start ScreenLens when Windows starts"; GroupDescription: "Additional icons:"; Flags: unchecked

[Run]
Filename: "wscript.exe"; Parameters: """{app}\run_silent.vbs"" ""{app}\main.py"""; WorkingDir: "{app}"; Description: "Launch ScreenLens now"; Flags: nowait postinstall skipifsilent
