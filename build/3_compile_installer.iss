; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define config "config_installer.ini"

#define MyAppName "AnimeTorr"
#define MyAppVersion "3.3.1.2"
#define MyAppOutputDir "..\dist"
#define pyinstallerDist "pyinstaller\dist\AnimeTorr"
#define MyAppPublisher "Sohhla"
#define MyAppExeName "AnimeTorr.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{B44F17ED-E453-4240-9197-4C88066C41E2}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={pf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputDir={#MyAppOutputDir}
OutputBaseFilename={#MyAppName} {#MyAppVersion}
Compression=lzma
SolidCompression=yes
CloseApplications=yes
UninstallDisplayIcon={app}\{#MyAppExeName}

[Tasks]
Name: desktopicon; Description: {cm:CreateDesktopIcon}; GroupDescription: {cm:AdditionalIcons}; Flags: unchecked
Name: quicklaunchicon; Description: {cm:CreateQuickLaunchIcon}; GroupDescription: {cm:AdditionalIcons}; Flags: unchecked; OnlyBelowVersion: 0,6.1
Name: iniciaricon; Description: Auto-start on Windows startup; GroupDescription: {cm:AdditionalIcons}

[Files]
Source: {#pyinstallerDist}\*; DestDir: {app}; Flags: ignoreversion
Source: {#pyinstallerDist}\qt4_plugins\imageformats\qgif4.dll; DestDir: {app}\qt4_plugins\imageformats; Flags: ignoreversion
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: {group}\{#MyAppName}; Filename: {app}\{#MyAppExeName}
Name: {group}\{cm:UninstallProgram,{#MyAppName}}; Filename: {uninstallexe}
Name: {commondesktop}\{#MyAppName}; Filename: {app}\{#MyAppExeName}; Tasks: desktopicon
Name: {userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}; Filename: {app}\{#MyAppExeName}; Tasks: quicklaunchicon
Name: {userstartup}\{#MyAppName} (start minimized); Filename: {app}\{#MyAppExeName}; WorkingDir: {app}; Parameters: -nogui; IconFilename: {app}\{#MyAppExeName}; IconIndex: 0; Tasks: iniciaricon

[Run]
Filename: {app}\{#MyAppExeName}; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, "&", "&&")}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: files; Name: {commonstartup}\{#MyAppName}
