What is Wine-Compholio?
=======================

**Warning: Do not report bugs at bugs.winehq.org when using this version!
Please take a look at our
[Wiki](https://github.com/compholio/wine-compholio/wiki/Reporting-bugs)
for more information about how to report bugs.**

The **Wine "Compholio" Edition** is a special build of the popular Wine
software that includes both patches written by our team and selected patches
by third party developers that we consider good enough for inclusion. This can
be seen as a testing version in preparation for patches to be submitted to
upstream Wine - don't be surprised if you encounter additional bugs, which are
not present in regular wine, and always report such issues to us (via github!),
so we can improve our fixes even further. Thanks!


How to install and use Wine-Compholio
=====================================

Ready-to-use packages for Wine-Compholio are available for a variety
of different Linux distributions directly for download. Just follow the
instructions available on the
[Wiki](https://github.com/compholio/wine-compholio/wiki/Installation).

When using Wine-Compholio there are a few differences compared to regular
Wine. The main difference is that it is not sufficient to type `wine` to
run it, but instead you will have to type `/opt/wine-compholio/bin/wine`.
Besides that there are also some other differences, for example additional
configuration options to tweak performance, which are not available in regular
Wine. All those differences are also documented on the
[Wiki](https://github.com/compholio/wine-compholio/wiki/Usage).


Included bugfixes and improvements
==================================

**Bugs fixed in Wine-Compholio 1.7.26 [58]:**

* ATL IOCS data should not be stored in GWLP_USERDATA ([Wine Bug #21767](http://bugs.winehq.org/show_bug.cgi?id=21767 "Multiple applications storing AxHostWindow instance pointer in GWLP_USERDATA crash on startup (Wine uses GWLP_USERDATA to store IOCS)(JLC's Internet TV, Anime Studio Pro 10.x)"))
* Add Dynamic DST exceptions for Israel Standard Time ([Wine Bug #36374](http://bugs.winehq.org/show_bug.cgi?id=36374 "Israel timezone handled incorrectly"))
* Add default ACLs for user shell folders
* Allow special characters in pipe names ([Wine Bug #28995](http://bugs.winehq.org/show_bug.cgi?id=28995 "Unable to use named pipes with \">\" character in the name"))
* Audio stuttering and performance drops in multiple applications ([Wine Bug #30639](http://bugs.winehq.org/show_bug.cgi?id=30639 "Audio stuttering and performance drops in Star Wolves 3"))
* Ensure NtProtectVirtualMemory and NtCreateSection are on separate pages ([Wine Bug #33162](http://bugs.winehq.org/show_bug.cgi?id=33162 "Acrobat Reader 11 crashes on start (native API application virtualization, NtProtectVirtualMemory removes execute page protection on its own code)"))
* Fix comparison of punctuation characters in lstrcmp ([Wine Bug #10767](http://bugs.winehq.org/show_bug.cgi?id=10767 "lstrcmp and others do not compare punctuation characters correctly"))
* Fix for ConnectNamedPort return value in overlapped mode ([Wine Bug #16550](http://bugs.winehq.org/show_bug.cgi?id=16550 "ConnectNamedPort should never return OK in overlapped mode (affects chromium ui_tests.exe)"))
* Fix for programs leaking wndproc slots ([Wine Bug #32451](http://bugs.winehq.org/show_bug.cgi?id=32451 "Multiple GOG.com installer bundles show a broken/unresponsive dialog window during installation (installer process running out of wndproc slots)"))
* Fix issue with invisible dragimages in ImageList ([Wine Bug #36761](http://bugs.winehq.org/show_bug.cgi?id=36761 "Imagelist invisible dragimage"))
* Fix unintentional leaks with ntdll internals
* Fix unitialized cch value when calling GetMenuItemInfo with a null pointer ([Wine Bug #34642](http://bugs.winehq.org/show_bug.cgi?id=34642 "Adobe Premiere Pro 2.0 exits silently on startup ('GetMenuItemInfo' must zero out 'cch' if mask doesn't specify 'MIIM_TYPE')"))
* Games For Windows Live 1.x expects a valid linker version in the PE header ([Wine Bug #28768](http://bugs.winehq.org/show_bug.cgi?id=28768 "Multiple GFWL (Games For Windows Live) 1.x games crash on startup (Kane & Lynch: Dead Men)"))
* GetSecurityInfo returns NULL DACL for process object ([Wine Bug #15980](http://bugs.winehq.org/show_bug.cgi?id=15980 "Rhapsody 2 crashes on startup (GetSecurityInfo returns NULL DACL for process object)"))
* Implement a Microsoft Yahei replacement font ([Wine Bug #13829](http://bugs.winehq.org/show_bug.cgi?id=13829 "Wine does not have CJK fonts"))
* Implement an Arial replacement font ([Wine Bug #32323](http://bugs.winehq.org/show_bug.cgi?id=32323 "Netflix (Silverlight 4.x) and several .NET Framework 3.x/4.0 WPF apps require either Arial or Verdana to be installed"))
* Improvement for heap allocation performance
* Lockfree algorithm for filedescriptor cache (improves file access speed)
* Make it possible to change media center / tablet pc status ([Wine Bug #18732](http://bugs.winehq.org/show_bug.cgi?id=18732 "Microsoft Experience Pack for Tablet PC 1 refuses to install"))
* Need for Speed 3 installer requires devices in HKEY_DYN_DATA ([Wine Bug #7115](http://bugs.winehq.org/show_bug.cgi?id=7115 "Need for Speed III installer fails in Win9X mode, reporting \"Could not get 'HardWareKey' value\" (active PnP device keys in 'HKEY_DYN_DATA\\\\Config Manager\\\\Enum' missing)"))
* Other Pipelight-specific enhancements
* Prevent window managers from grouping all wine programs together ([Wine Bug #32699](http://bugs.winehq.org/show_bug.cgi?id=32699 "Add StartupWMClass to .desktop files."))
* Reduced SetTimer minimum value from 10 ms to 5 ms (improves Silverlight framerates)
* Return an error when trying to open a terminated process ([Wine Bug #37087](http://bugs.winehq.org/show_bug.cgi?id=37087 "Gothic 2 english demo fails with 'Conflict: a hook process was found. Please deactivate all Antivirus and Anti-Trojan programs and debuggers.'"))
* Return correct IMediaSeeking stream positions in quartz ([Wine Bug #23174](http://bugs.winehq.org/show_bug.cgi?id=23174 "Fallout 3: Diologue and Video/sound issues"))
* SO_CONNECT_TIME returns the appropriate time
* Set ldr.EntryPoint for main executable ([Wine Bug #33034](http://bugs.winehq.org/show_bug.cgi?id=33034 "Many GFWL (Games For Windows Live) 1.x/2.x/3.x games crash or exit silently on startup (DiRT 2/3, GTA IV Steam)"))
* Support for AllocateAndGetTcpExTableFromStack ([Wine Bug #34372](http://bugs.winehq.org/show_bug.cgi?id=34372 "Add missing function AllocateAndGetTcpExTableFromStack() to iphlpapi.dll"))
* Support for BCryptGetFipsAlgorithmMode ([Wine Bug #32194](http://bugs.winehq.org/show_bug.cgi?id=32194 "Multiple games and applications need bcrypt.dll.BCryptGetFipsAlgorithmMode (Chess Position Trainer, Terraria, .NET System.Security.Cryptography)"))
* Support for DOS hidden/system file attributes ([Wine Bug #9158](http://bugs.winehq.org/show_bug.cgi?id=9158 "Multiple Microsoft development tools online/web installers fail to skip \"$shtdwn$.req\" with FILE_ATTRIBUTE_HIDDEN (Visual Studio Express Editions, .NET Framework 3.0)"))
* Support for Dynamic DST (daylight saving time) information in registry
* Support for GetFinalPathNameByHandle ([Wine Bug #36073](http://bugs.winehq.org/show_bug.cgi?id=36073 "OneDrive crashes on unimplemented function KERNEL32.dll.GetFinalPathNameByHandleW"))
* Support for GetSystemTimes ([Wine Bug #19813](http://bugs.winehq.org/show_bug.cgi?id=19813 "Voddler needs GetSystemTimes to run"))
* Support for GetVolumePathName
* Support for ITextDocument_fnRange function ([Wine Bug #12458](http://bugs.winehq.org/show_bug.cgi?id=12458 "Multiple apps fail due to RichEdit ITextDocument_fnRange stub (MySQL Workbench, BlitzMaxDemo137)"))
* Support for ITextRange, ITextFont and ITextPara ([Wine Bug #18303](http://bugs.winehq.org/show_bug.cgi?id=18303 "Adobe Acrobat Pro 7: Crashes when selecting the \"edit\" menu while having a file open."))
* Support for Junction Points ([Wine Bug #12401](http://bugs.winehq.org/show_bug.cgi?id=12401 "Support junction points, i.e. DeviceIoCtl(FSCTL_SET_REPARSE_POINT/FSCTL_GET_REPARSE_POINT)"))
* Support for KF_FLAG_DEFAULT_PATH in SHGetKnownFolderPath ([Wine Bug #30385](http://bugs.winehq.org/show_bug.cgi?id=30385 "Windows Live Essentials 2011 web installer fails to download packages in background (shell32.SHGetKnownFolderPath missing support for KF_FLAG_DEFAULT_PATH)"))
* Support for LoadIconMetric ([Wine Bug #35375](http://bugs.winehq.org/show_bug.cgi?id=35375 "Multiple applications need Vista+ API COMCTL32.dll.380 a.k.a. 'LoadIconMetric' (Solidworks 2013 systray monitor, Microsoft One/SkyDrive)"))
* Support for NtSetInformationFile class FileDispositionInformation ([Wine Bug #30397](http://bugs.winehq.org/show_bug.cgi?id=30397 "Multiple applications need support for NtSetInformationFile class FileDispositionInformation (Cygwin installer, Stylizer 5.x Visual CSS editor, Spoon Studio 2011 (ex Xenocode) application sandboxing scheme)"))
* Support for PulseAudio backend for audio ([Wine Bug #10495](http://bugs.winehq.org/show_bug.cgi?id=10495 "Wine should support PulseAudio"))
* Support for SHCreateSessionKey ([Wine Bug #35630](http://bugs.winehq.org/show_bug.cgi?id=35630 "SHCreateSessionKey is unimplemented"))
* Support for TOOLTIPS_GetTipText edge cases ([Wine Bug #30648](http://bugs.winehq.org/show_bug.cgi?id=30648 "SEGA Genesis / Mega Drive Classic Collection (Steam) crashes on startup"))
* Support for TransmitFile ([Wine Bug #5048](http://bugs.winehq.org/show_bug.cgi?id=5048 "Multiple applications and games need support for ws2_32 SIO_GET_EXTENSION_FUNCTION_POINTER TransmitFile (WSAID_TRANSMITFILE)"))
* Support for WTSEnumerateProcessesW ([Wine Bug #29903](http://bugs.winehq.org/show_bug.cgi?id=29903 "Some Microsoft debuggers fail to enumerate processes due to wtsapi32.WTSEnumerateProcessesW() being a stub (Microsoft Visual Studio 2005, DbgCLR from .NET 2.0 SDK)"))
* Support for [Get|Set]SystemFileCacheSize ([Wine Bug #35886](http://bugs.winehq.org/show_bug.cgi?id=35886 "Lotus Notes 9 'cacheset.exe' utility needs KERNEL32.dll.SetSystemFileCacheSize"))
* Support for extra large and jumbo icon lists in shell32 ([Wine Bug #24721](http://bugs.winehq.org/show_bug.cgi?id=24721 "Explorer++ crashes when choosing to view large icons or extra large icons"))
* Support for inherited file ACLs ([Wine Bug #34406](http://bugs.winehq.org/show_bug.cgi?id=34406 "Finale Notepad 2012 doesn't copy/create user files on program start"))
* Support for interface change notifications ([Wine Bug #32328](http://bugs.winehq.org/show_bug.cgi?id=32328 "Many .NET and Silverlight applications require SIO_ADDRESS_LIST_CHANGE for interface change notifications"))
* Support for process ACLs ([Wine Bug #22006](http://bugs.winehq.org/show_bug.cgi?id=22006 "OpenProcess does not enforce ACL"))
* Support for setcap on wine-preloader ([Wine Bug #26256](http://bugs.winehq.org/show_bug.cgi?id=26256 "wine64-preloader can't handle setcap cap_net_raw+epi"))
* Support for stored file ACLs ([Wine Bug #31858](http://bugs.winehq.org/show_bug.cgi?id=31858 "Netflix on Firefox fails with Internet Connection Problem when loading bar is at 99%"))
* Support for ws2_32.inet_pton ([Wine Bug #36713](http://bugs.winehq.org/show_bug.cgi?id=36713 "Watch_Dogs requires ws2_32.inet_pton"))
* ~~Use assembly wrapper to run TLS callbacks~~ ([Wine Bug #21917](http://bugs.winehq.org/show_bug.cgi?id=21917 "SC2 'LazyLaunch' v2.0 fails with 'Exception frame is not in stack limits => unable to dispatch exception.' (TLS callbacks can taint EBP, needs assembly wrapper)"))
* Use manual relay for RunDLL_CallEntry16 in shell32 ([Wine Bug #23033](http://bugs.winehq.org/show_bug.cgi?id=23033 "Tages Protection v5.x: games report \"DLL not found shell.dll16.dll\" (Runaway 2: The Dream Of The Turtle, ...)"))
* Workaround for shlwapi URLs with relative paths
* XEMBED support for embedding Wine windows inside Linux applications
* nVidia driver for high-end laptop cards does not list all supported resolutions

