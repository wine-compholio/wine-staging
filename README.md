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

**Bugfixes and features included in the next upcoming release [5]:**

* Fix issues when driver dispatch routine returns different status codes ([Wine Bug #30155](http://bugs.winehq.org/show_bug.cgi?id=30155))
* Send WM_PAINT event during dialog creation ([Wine Bug #35652](http://bugs.winehq.org/show_bug.cgi?id=35652))
* Support for FIND_FIRST_EX_CASE_SENSITIVE flag in FindFirstFileExW
* Unity3D Editor requires ProductId registry value ([Wine Bug #36964](http://bugs.winehq.org/show_bug.cgi?id=36964))
* Update a XIM candidate position when cursor location changes ([Wine Bug #30938](http://bugs.winehq.org/show_bug.cgi?id=30938))


**Bugs fixed in Wine-Compholio 1.7.27 [63]:**

* ATL IOCS data should not be stored in GWLP_USERDATA ([Wine Bug #21767](http://bugs.winehq.org/show_bug.cgi?id=21767))
* Add Dynamic DST exceptions for Israel Standard Time ([Wine Bug #36374](http://bugs.winehq.org/show_bug.cgi?id=36374))
* Add default ACLs for user shell folders
* Allow special characters in pipe names ([Wine Bug #28995](http://bugs.winehq.org/show_bug.cgi?id=28995))
* Audio stuttering and performance drops in multiple applications ([Wine Bug #30639](http://bugs.winehq.org/show_bug.cgi?id=30639))
* Don't fill KdHelp structure for usermode applications ([Wine Bug #37272](http://bugs.winehq.org/show_bug.cgi?id=37272))
* Ensure NtProtectVirtualMemory and NtCreateSection are on separate pages ([Wine Bug #33162](http://bugs.winehq.org/show_bug.cgi?id=33162))
* Fix black screen on startup introduced by pixelformat changes. ([Wine Bug #35950](http://bugs.winehq.org/show_bug.cgi?id=35950))
* Fix comparison of punctuation characters in lstrcmp ([Wine Bug #10767](http://bugs.winehq.org/show_bug.cgi?id=10767))
* Fix flickering introduced by pixelformat changes. ([Wine Bug #35718](http://bugs.winehq.org/show_bug.cgi?id=35718))
* Fix for ConnectNamedPort return value in overlapped mode ([Wine Bug #16550](http://bugs.winehq.org/show_bug.cgi?id=16550))
* Fix for programs leaking wndproc slots ([Wine Bug #32451](http://bugs.winehq.org/show_bug.cgi?id=32451))
* Fix gray screen on startup introduced by pixelformat changes. ([Wine Bug #35975](http://bugs.winehq.org/show_bug.cgi?id=35975))
* Fix issue with invisible dragimages in ImageList ([Wine Bug #36761](http://bugs.winehq.org/show_bug.cgi?id=36761))
* Fix missing video introduced by pixelformat changes. ([Wine Bug #36900](http://bugs.winehq.org/show_bug.cgi?id=36900))
* Fix unintentional leaks with ntdll internals
* Fix wined3d performance drop introduced by pixelformat changes. ([Wine Bug #35655](http://bugs.winehq.org/show_bug.cgi?id=35655))
* Games For Windows Live 1.x expects a valid linker version in the PE header ([Wine Bug #28768](http://bugs.winehq.org/show_bug.cgi?id=28768))
* GetSecurityInfo returns NULL DACL for process object ([Wine Bug #15980](http://bugs.winehq.org/show_bug.cgi?id=15980))
* Implement a Microsoft Yahei replacement font ([Wine Bug #13829](http://bugs.winehq.org/show_bug.cgi?id=13829))
* Implement an Arial replacement font ([Wine Bug #32323](http://bugs.winehq.org/show_bug.cgi?id=32323))
* Improvement for heap allocation performance
* Lego Stunt Rally requires DXTn software de/encoding support ([Wine Bug #25486](http://bugs.winehq.org/show_bug.cgi?id=25486))
* Lockfree algorithm for filedescriptor cache (improves file access speed)
* Make it possible to change media center / tablet pc status ([Wine Bug #18732](http://bugs.winehq.org/show_bug.cgi?id=18732))
* Need for Speed 3 installer requires devices in HKEY_DYN_DATA ([Wine Bug #7115](http://bugs.winehq.org/show_bug.cgi?id=7115))
* Other Pipelight-specific enhancements
* Prevent window managers from grouping all wine programs together ([Wine Bug #32699](http://bugs.winehq.org/show_bug.cgi?id=32699))
* Reduced SetTimer minimum value from 10 ms to 5 ms (improves Silverlight framerates)
* Return an error when trying to open a terminated process ([Wine Bug #37087](http://bugs.winehq.org/show_bug.cgi?id=37087))
* Return correct IMediaSeeking stream positions in quartz ([Wine Bug #23174](http://bugs.winehq.org/show_bug.cgi?id=23174))
* SO_CONNECT_TIME returns the appropriate time
* Set ldr.EntryPoint for main executable ([Wine Bug #33034](http://bugs.winehq.org/show_bug.cgi?id=33034))
* Support for AllocateAndGetTcpExTableFromStack ([Wine Bug #34372](http://bugs.winehq.org/show_bug.cgi?id=34372))
* Support for DOS hidden/system file attributes ([Wine Bug #9158](http://bugs.winehq.org/show_bug.cgi?id=9158))
* Support for Dynamic DST (daylight saving time) information in registry
* Support for FIND_FIRST_EX_LARGE_FETCH flag in FindFirstFileExW ([Wine Bug #35121](http://bugs.winehq.org/show_bug.cgi?id=35121))
* Support for GetFinalPathNameByHandle ([Wine Bug #36073](http://bugs.winehq.org/show_bug.cgi?id=36073))
* Support for GetSystemTimes ([Wine Bug #19813](http://bugs.winehq.org/show_bug.cgi?id=19813))
* Support for GetVolumePathName
* Support for ITextDocument_fnRange function ([Wine Bug #12458](http://bugs.winehq.org/show_bug.cgi?id=12458))
* Support for ITextRange, ITextFont and ITextPara ([Wine Bug #18303](http://bugs.winehq.org/show_bug.cgi?id=18303))
* Support for Junction Points ([Wine Bug #12401](http://bugs.winehq.org/show_bug.cgi?id=12401))
* Support for KF_FLAG_DEFAULT_PATH in SHGetKnownFolderPath ([Wine Bug #30385](http://bugs.winehq.org/show_bug.cgi?id=30385))
* Support for LoadIconMetric ([Wine Bug #35375](http://bugs.winehq.org/show_bug.cgi?id=35375))
* Support for NtSetInformationFile class FileDispositionInformation ([Wine Bug #30397](http://bugs.winehq.org/show_bug.cgi?id=30397))
* Support for PulseAudio backend for audio ([Wine Bug #10495](http://bugs.winehq.org/show_bug.cgi?id=10495))
* Support for SHCreateSessionKey ([Wine Bug #35630](http://bugs.winehq.org/show_bug.cgi?id=35630))
* Support for TOOLTIPS_GetTipText edge cases ([Wine Bug #30648](http://bugs.winehq.org/show_bug.cgi?id=30648))
* Support for TransmitFile ([Wine Bug #5048](http://bugs.winehq.org/show_bug.cgi?id=5048))
* Support for WTSEnumerateProcessesW ([Wine Bug #29903](http://bugs.winehq.org/show_bug.cgi?id=29903))
* Support for [Get|Set]SystemFileCacheSize ([Wine Bug #35886](http://bugs.winehq.org/show_bug.cgi?id=35886))
* Support for extra large and jumbo icon lists in shell32 ([Wine Bug #24721](http://bugs.winehq.org/show_bug.cgi?id=24721))
* Support for inherited file ACLs ([Wine Bug #34406](http://bugs.winehq.org/show_bug.cgi?id=34406))
* Support for interface change notifications ([Wine Bug #32328](http://bugs.winehq.org/show_bug.cgi?id=32328))
* Support for process ACLs ([Wine Bug #22006](http://bugs.winehq.org/show_bug.cgi?id=22006))
* Support for setcap on wine-preloader ([Wine Bug #26256](http://bugs.winehq.org/show_bug.cgi?id=26256))
* Support for stored file ACLs ([Wine Bug #31858](http://bugs.winehq.org/show_bug.cgi?id=31858))
* Support for ws2_32.inet_pton ([Wine Bug #36713](http://bugs.winehq.org/show_bug.cgi?id=36713))
* Use manual relay for RunDLL_CallEntry16 in shell32 ([Wine Bug #23033](http://bugs.winehq.org/show_bug.cgi?id=23033))
* Workaround for shlwapi URLs with relative paths
* XEMBED support for embedding Wine windows inside Linux applications
* nVidia driver for high-end laptop cards does not list all supported resolutions

