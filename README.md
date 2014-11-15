What is Wine Staging?
=====================

**Warning: Do not report bugs at bugs.winehq.org when using this version!
Please take a look at our
[Wiki](https://github.com/wine-compholio/wine-staging/wiki/Reporting-bugs)
for more information about how to report bugs.**

**Wine Staging** (formerly wine-compholio) is a special wine version containing
bug fixes and features that are not yet available in regular wine versions. The
idea behind Wine Staging is to provide new features faster to end users and to
give developers the possibility to discuss and improve their patches before
they are sent upstream. We also intend to create a community of wine developers
to share experience and to make it easier for beginners to start hacking on
wine.

Although we are reviewing all patches before adding them, you may encounter
additional bugs, which are not present in regular wine. Make sure to report
such issues in our bug tracker instead of winehq.org so that we can try to
solve them in future versions. Thanks!

How to install and use Wine Staging
===================================

Ready-to-use packages for Wine Staging are available for a variety
of different Linux distributions directly for download. Just follow the
instructions available on the
[Wiki](https://github.com/wine-compholio/wine-staging/wiki/Installation).

When using Wine Staging there are a few differences compared to regular
Wine. The main difference is that it is not sufficient to type `wine` to
run it, but instead you will have to type `/opt/wine-compholio/bin/wine`.
Besides that there are also some other differences, for example additional
configuration options to tweak performance, which are not available in regular
Wine. All those differences are also documented on the
[Wiki](https://github.com/wine-compholio/wine-staging/wiki/Usage).


Included bug fixes and improvements
===================================

**Bugfixes and features included in the next upcoming release [18]:**

* Add stub for NtSetLdtEntries/ZwSetLdtEntries ([Wine Bug #26268](https://bugs.winehq.org/show_bug.cgi?id=26268))
* Allow selection of audio device for PulseAudio backend
* Avoid crashing when broken app tries to release surface although refcount is zero ([Wine Bug #18477](https://bugs.winehq.org/show_bug.cgi?id=18477))
* Avoid sending window messages in FindWindowExW ([Wine Bug #27282](https://bugs.winehq.org/show_bug.cgi?id=27282))
* CoWaitForMultipleHandles shouldn't process window events when APC calls are queued ([Wine Bug #32568](https://bugs.winehq.org/show_bug.cgi?id=32568))
* Emulate access to KI_USER_SHARED_DATA kernel page on x86_64 ([Wine Bug #33849](https://bugs.winehq.org/show_bug.cgi?id=33849))
* Exception during start of fr-043 caused by missing DXTn support ([Wine Bug #37391](https://bugs.winehq.org/show_bug.cgi?id=37391))
* FairplayKD.sys needs KeSetSystemAffinityThread ([Wine Bug #36822](https://bugs.winehq.org/show_bug.cgi?id=36822))
* Fix crash of Trine Demo on start ([Wine Bug #19231](https://bugs.winehq.org/show_bug.cgi?id=19231))
* Fix crash of winedevice when relocation entry crosses page boundary ([Wine Bug #28254](https://bugs.winehq.org/show_bug.cgi?id=28254))
* Fix handling of invert_y in DrawTextExW ([Wine Bug #22109](https://bugs.winehq.org/show_bug.cgi?id=22109))
* Fix texture corruption in CSI: Fatal Conspiracy ([Wine Bug #33768](https://bugs.winehq.org/show_bug.cgi?id=33768))
* Initialize irp.Tail.Overlay.OriginalFileObject with stub file object ([Wine Bug #37537](https://bugs.winehq.org/show_bug.cgi?id=37537))
* MSVCRT crashes when NULL is passed as string to atof or strtod ([Wine Bug #32550](https://bugs.winehq.org/show_bug.cgi?id=32550))
* Return correct values for GetThreadTimes function ([Wine Bug #20230](https://bugs.winehq.org/show_bug.cgi?id=20230))
* Return more context attributes in schan_InitializeSecurityContextW ([Wine Bug #37527](https://bugs.winehq.org/show_bug.cgi?id=37527))
* vSphere needs IoCsqInitialize ([Wine Bug #36777](https://bugs.winehq.org/show_bug.cgi?id=36777))
* wglDescribePixelFormat should return max index for NULL descriptor ([Wine Bug #6176](https://bugs.winehq.org/show_bug.cgi?id=6176))


**Bugs fixed in Wine Staging 1.7.30 [90]:**

* ATL IOCS data should not be stored in GWLP_USERDATA ([Wine Bug #21767](https://bugs.winehq.org/show_bug.cgi?id=21767))
* Add Dynamic DST exceptions for Israel Standard Time ([Wine Bug #36374](https://bugs.winehq.org/show_bug.cgi?id=36374))
* Add default ACLs for user shell folders
* ~~Add partially support for sessionStorage~~
* Adobe Reader needs ITextSelection_fnGetDuplicate implementation
* Allow special characters in pipe names ([Wine Bug #28995](https://bugs.winehq.org/show_bug.cgi?id=28995))
* Anno 1602 installer depends on Windows 98 behavior of SHFileOperationW
* Audio stuttering and performance drops in multiple applications ([Wine Bug #30639](https://bugs.winehq.org/show_bug.cgi?id=30639))
* ~~Cinema 4D needs NotifyIpInterfaceChange~~ ([Wine Bug #34573](https://bugs.winehq.org/show_bug.cgi?id=34573))
* Correctly treat '.' when checking for empty directories ([Wine Bug #26272](https://bugs.winehq.org/show_bug.cgi?id=26272))
* D3DCompileShader should filter specific warning messages ([Wine Bug #33770](https://bugs.winehq.org/show_bug.cgi?id=33770))
* Do not fail when a used context is passed to wglShareLists ([Wine Bug #11436](https://bugs.winehq.org/show_bug.cgi?id=11436))
* Don't fill KdHelp structure for usermode applications ([Wine Bug #37272](https://bugs.winehq.org/show_bug.cgi?id=37272))
* Emulate write to CR4 register ([Wine Bug #30220](https://bugs.winehq.org/show_bug.cgi?id=30220))
* Ensure NtProtectVirtualMemory and NtCreateSection are on separate pages ([Wine Bug #33162](https://bugs.winehq.org/show_bug.cgi?id=33162))
* FEAR 1 installer expects basic_string_wchar_dtor to return NULL ([Wine Bug #37358](https://bugs.winehq.org/show_bug.cgi?id=37358))
* Fix black screen on startup introduced by pixelformat changes. ([Wine Bug #35950](https://bugs.winehq.org/show_bug.cgi?id=35950))
* Fix comparison of punctuation characters in lstrcmp ([Wine Bug #10767](https://bugs.winehq.org/show_bug.cgi?id=10767))
* Fix flickering introduced by pixelformat changes. ([Wine Bug #35718](https://bugs.winehq.org/show_bug.cgi?id=35718))
* Fix for ConnectNamedPort return value in overlapped mode ([Wine Bug #16550](https://bugs.winehq.org/show_bug.cgi?id=16550))
* Fix for programs leaking wndproc slots ([Wine Bug #32451](https://bugs.winehq.org/show_bug.cgi?id=32451))
* Fix gray screen on startup introduced by pixelformat changes. ([Wine Bug #35975](https://bugs.winehq.org/show_bug.cgi?id=35975))
* Fix issues when driver dispatch routine returns different status codes ([Wine Bug #30155](https://bugs.winehq.org/show_bug.cgi?id=30155))
* Fix missing video introduced by pixelformat changes. ([Wine Bug #36900](https://bugs.winehq.org/show_bug.cgi?id=36900))
* Fix unintentional leaks with ntdll internals
* Fix wined3d performance drop introduced by pixelformat changes. ([Wine Bug #35655](https://bugs.winehq.org/show_bug.cgi?id=35655))
* Games For Windows Live 1.x expects a valid linker version in the PE header ([Wine Bug #28768](https://bugs.winehq.org/show_bug.cgi?id=28768))
* GetSecurityInfo returns NULL DACL for process object ([Wine Bug #15980](https://bugs.winehq.org/show_bug.cgi?id=15980))
* Implement a Microsoft Yahei replacement font ([Wine Bug #13829](https://bugs.winehq.org/show_bug.cgi?id=13829))
* Implement an Arial replacement font ([Wine Bug #32323](https://bugs.winehq.org/show_bug.cgi?id=32323))
* Improvement for heap allocation performance
* Lego Stunt Rally requires DXTn software de/encoding support ([Wine Bug #25486](https://bugs.winehq.org/show_bug.cgi?id=25486))
* Limit cross thread access to ImmSet* functions ([Wine Bug #35361](https://bugs.winehq.org/show_bug.cgi?id=35361))
* Lockfree algorithm for filedescriptor cache (improves file access speed)
* Make it possible to change media center / tablet pc status ([Wine Bug #18732](https://bugs.winehq.org/show_bug.cgi?id=18732))
* Multiple applications need EnumDisplayDevicesW implementation ([Wine Bug #34978](https://bugs.winehq.org/show_bug.cgi?id=34978))
* Need for Speed 3 installer requires devices in HKEY_DYN_DATA ([Wine Bug #7115](https://bugs.winehq.org/show_bug.cgi?id=7115))
* Other Pipelight-specific enhancements
* Prevent window managers from grouping all wine programs together ([Wine Bug #32699](https://bugs.winehq.org/show_bug.cgi?id=32699))
* Reduced SetTimer minimum value from 10 ms to 5 ms (improves Silverlight framerates)
* Return an error when trying to open a terminated process ([Wine Bug #37087](https://bugs.winehq.org/show_bug.cgi?id=37087))
* Return correct IMediaSeeking stream positions in quartz ([Wine Bug #23174](https://bugs.winehq.org/show_bug.cgi?id=23174))
* SO_CONNECT_TIME returns the appropriate time
* Send WM_PAINT event during dialog creation ([Wine Bug #35652](https://bugs.winehq.org/show_bug.cgi?id=35652))
* Support for AllocateAndGetTcpExTableFromStack ([Wine Bug #34372](https://bugs.winehq.org/show_bug.cgi?id=34372))
* Support for BindImageEx ([Wine Bug #3591](https://bugs.winehq.org/show_bug.cgi?id=3591))
* ~~Support for D3DXCreatePolygon~~ ([Wine Bug #13632](https://bugs.winehq.org/show_bug.cgi?id=13632))
* Support for D3DXGetShaderInputSemantics ([Wine Bug #22682](https://bugs.winehq.org/show_bug.cgi?id=22682))
* Support for DOS hidden/system file attributes ([Wine Bug #9158](https://bugs.winehq.org/show_bug.cgi?id=9158))
* Support for Dynamic DST (daylight saving time) information in registry
* ~~Support for FindFirstFileExW level FindExInfoBasic~~ ([Wine Bug #37354](https://bugs.winehq.org/show_bug.cgi?id=37354))
* Support for GdipCreateRegionRgnData ([Wine Bug #34843](https://bugs.winehq.org/show_bug.cgi?id=34843))
* Support for GetFinalPathNameByHandle ([Wine Bug #36073](https://bugs.winehq.org/show_bug.cgi?id=36073))
* Support for GetSystemTimes ([Wine Bug #19813](https://bugs.winehq.org/show_bug.cgi?id=19813))
* Support for GetVolumePathName
* Support for ID3DXSkinInfoImpl_UpdateSkinnedMesh ([Wine Bug #32572](https://bugs.winehq.org/show_bug.cgi?id=32572))
* Support for ITextDocument_fnRange function ([Wine Bug #12458](https://bugs.winehq.org/show_bug.cgi?id=12458))
* Support for ITextRange, ITextFont and ITextPara ([Wine Bug #18303](https://bugs.winehq.org/show_bug.cgi?id=18303))
* Support for Junction Points ([Wine Bug #12401](https://bugs.winehq.org/show_bug.cgi?id=12401))
* Support for KF_FLAG_DEFAULT_PATH in SHGetKnownFolderPath ([Wine Bug #30385](https://bugs.winehq.org/show_bug.cgi?id=30385))
* Support for LoadIconMetric ([Wine Bug #35375](https://bugs.winehq.org/show_bug.cgi?id=35375))
* Support for NtQuerySection ([Wine Bug #37338](https://bugs.winehq.org/show_bug.cgi?id=37338))
* Support for NtSetInformationFile class FileDispositionInformation ([Wine Bug #30397](https://bugs.winehq.org/show_bug.cgi?id=30397))
* Support for PulseAudio backend for audio ([Wine Bug #10495](https://bugs.winehq.org/show_bug.cgi?id=10495))
* Support for RtlDecompressBuffer ([Wine Bug #37449](https://bugs.winehq.org/show_bug.cgi?id=37449))
* Support for SHCreateSessionKey ([Wine Bug #35630](https://bugs.winehq.org/show_bug.cgi?id=35630))
* ~~Support for TLB dependencies lookup in resources~~ ([Wine Bug #34184](https://bugs.winehq.org/show_bug.cgi?id=34184))
* Support for TOOLTIPS_GetTipText edge cases ([Wine Bug #30648](https://bugs.winehq.org/show_bug.cgi?id=30648))
* Support for TransmitFile ([Wine Bug #5048](https://bugs.winehq.org/show_bug.cgi?id=5048))
* Support for UTF7 encoding/decoding ([Wine Bug #27388](https://bugs.winehq.org/show_bug.cgi?id=27388))
* Support for WTSEnumerateProcessesW ([Wine Bug #29903](https://bugs.winehq.org/show_bug.cgi?id=29903))
* Support for extra large and jumbo icon lists in shell32 ([Wine Bug #24721](https://bugs.winehq.org/show_bug.cgi?id=24721))
* Support for inherited file ACLs ([Wine Bug #34406](https://bugs.winehq.org/show_bug.cgi?id=34406))
* Support for interface change notifications ([Wine Bug #32328](https://bugs.winehq.org/show_bug.cgi?id=32328))
* Support for pasting HTML from Unix applications ([Wine Bug #7372](https://bugs.winehq.org/show_bug.cgi?id=7372))
* Support for process ACLs ([Wine Bug #22006](https://bugs.winehq.org/show_bug.cgi?id=22006))
* Support for setcap on wine-preloader ([Wine Bug #26256](https://bugs.winehq.org/show_bug.cgi?id=26256))
* Support for stored file ACLs ([Wine Bug #31858](https://bugs.winehq.org/show_bug.cgi?id=31858))
* Support for wine64 on FreeBSD/PC-BSD ([Wine Bug #34330](https://bugs.winehq.org/show_bug.cgi?id=34330))
* ~~Support for ws2_32.inet_pton~~ ([Wine Bug #36713](https://bugs.winehq.org/show_bug.cgi?id=36713))
* Tumblebugs 2 requires DXTn software encoding support ([Wine Bug #29586](https://bugs.winehq.org/show_bug.cgi?id=29586))
* Unity3D Editor requires ProductId registry value ([Wine Bug #36964](https://bugs.winehq.org/show_bug.cgi?id=36964))
* ~~Update ProductVersion property when applying MSI transforms~~ ([Wine Bug #37493](https://bugs.winehq.org/show_bug.cgi?id=37493))
* Update a XIM candidate position when cursor location changes ([Wine Bug #30938](https://bugs.winehq.org/show_bug.cgi?id=30938))
* Use manual relay for RunDLL_CallEntry16 in shell32 ([Wine Bug #23033](https://bugs.winehq.org/show_bug.cgi?id=23033))
* Voobly expects correct handling of WRITECOPY memory protection ([Wine Bug #29384](https://bugs.winehq.org/show_bug.cgi?id=29384))
* Wine ignores IDF_CHECKFIRST flag in SetupPromptForDisk ([Wine Bug #20465](https://bugs.winehq.org/show_bug.cgi?id=20465))
* Workaround for shlwapi URLs with relative paths
* XEMBED support for embedding Wine windows inside Linux applications
* nVidia driver for high-end laptop cards does not list all supported resolutions

