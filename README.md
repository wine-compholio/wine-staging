What is Wine Staging?
---------------------

**Warning: Do not report bugs at bugs.winehq.org when using this version!
Please take a look [here](http://bugs.wine-staging.com) for more information
about how to report bugs.**

**Wine Staging** (formerly wine-compholio) is a special wine version containing
bug fixes and features, which are not yet available in regular wine versions.
The idea of Wine Staging is to provide new features faster to end users and to
give developers the possibility to discuss and improve their patches before
they are sent upstream. We also intend to create a community of wine developers
to share experience and to make it easier for beginners to start hacking on
wine. More information about Wine Staging can also be found on our website
[wine-staging.com](http://wine-staging.com).

Although we are reviewing and testing all patches before adding them, you may
encounter additional bugs, which are not present in vanilla wine. Make sure to
report such issues in our bug tracker instead of winehq.org so that we can try
to solve them in future versions. Thanks!

How to install and use Wine Staging
-----------------------------------

Ready-to-use packages for Wine Staging are available for a variety
of different Linux distributions directly for download. Just follow the
instructions available on the
[Wiki](https://github.com/wine-compholio/wine-staging/wiki/Installation).

When using Wine Staging there are a few differences compared to regular
Wine. The main difference is that it is not sufficient to type `wine` to
run it, but instead you will have to type `/opt/wine-staging/bin/wine`.
Besides that there are also some other differences, for example additional
configuration options to tweak performance, which are not available in regular
Wine. All those differences are also documented on the
[Wiki](https://github.com/wine-compholio/wine-staging/wiki/Usage).


Included bug fixes and improvements
-----------------------------------

**Bug fixes and features included in the next upcoming release [8]:**

* Add stub for atl80.AtlIPersistPropertyBag_Save ([Wine Bug #33888](https://bugs.winehq.org/show_bug.cgi?id=33888))
* Add stub for winsta.WinStationEnumerateW ([Wine Bug #38102](https://bugs.winehq.org/show_bug.cgi?id=38102))
* Dirtify vertex shader on transformed update to fix graphical corruption ([Wine Bug #38539](https://bugs.winehq.org/show_bug.cgi?id=38539))
* Improve ReadDataAvailable handling in FilePipeLocalInformation class
* Return default palette entries from GetSystemPaletteEntries for non-palette-based devices
* Support for ObjectTypeInformation class support in NtQueryObject
* Use POSIX implementation to enumerate directory content on FreeBSD ([Wine Bug #35397](https://bugs.winehq.org/show_bug.cgi?id=35397))
* Wait before reusing recently freed memory


**Bug fixes and features in Wine Staging 1.7.42 [221]:**

*Note: The following list only contains features and bug fixes which are not
yet available in vanilla Wine. They are removed from the list as soon as they
are included upstream. The list also includes features and fixes from previous
releases, take a look at the
[changelog](https://github.com/wine-compholio/wine-staging/blob/master/debian/changelog)
for more details.*

* Add a ProfileList\<UserSID> registry subkey ([Wine Bug #15670](https://bugs.winehq.org/show_bug.cgi?id=15670))
* ~~Add default ACLs for user shell folders~~
* Add implementation for CreateThreadpool ([Wine Bug #35192](https://bugs.winehq.org/show_bug.cgi?id=35192))
* Add implementation for mfplat.MFTRegister ([Wine Bug #37811](https://bugs.winehq.org/show_bug.cgi?id=37811))
* Add nvapi stubs required for GPU PhysX support
* Add performance library registry keys needed by MS SQL Server Management Studio Express 2008 R2 ([Wine Bug #33661](https://bugs.winehq.org/show_bug.cgi?id=33661))
* Add semi-stub for GetFileVersionInfoExA/W ([Wine Bug #38098](https://bugs.winehq.org/show_bug.cgi?id=38098))
* Add semi-stub for GetFileVersionInfoSizeExA/W ([Wine Bug #38090](https://bugs.winehq.org/show_bug.cgi?id=38090))
* Add stub fltmgr.sys (filter manager driver) ([Wine Bug #23583](https://bugs.winehq.org/show_bug.cgi?id=23583))
* Add stub for D3DXComputeNormalMap
* Add stub for D3DXComputeTangentFrameEx ([Wine Bug #31984](https://bugs.winehq.org/show_bug.cgi?id=31984))
* Add stub for D3DXFrameFind ([Wine Bug #38334](https://bugs.winehq.org/show_bug.cgi?id=38334))
* Add stub for D3DXIntersect
* Add stub for NtSetLdtEntries/ZwSetLdtEntries ([Wine Bug #26268](https://bugs.winehq.org/show_bug.cgi?id=26268))
* Add stub for advapi32.ImpersonateAnonymousToken
* Add stub for d3d11.D3D11CreateDeviceAndSwapChain ([Wine Bug #33153](https://bugs.winehq.org/show_bug.cgi?id=33153))
* Add stub for gdiplus.GdipCreateEffect ([Wine Bug #32163](https://bugs.winehq.org/show_bug.cgi?id=32163))
* Add stub for ntoskrnl.ExAcquireResourceExclusiveLite
* Add stub for ntoskrnl.ExDeleteResourceLite
* Add stub for ntoskrnl.ExReleaseResourceForThread
* Add stub for ntoskrnl.KeWaitForMultipleObjects
* Add stub for ntoskrnl.Mm{Map,Unmap}LockedPages
* Add stub for ntoskrnl.PsRemoveLoadImageNotifyRoutine
* Add stub for setupapi.SetupDiSelectBestCompatDrv ([Wine Bug #32088](https://bugs.winehq.org/show_bug.cgi?id=32088))
* Add stub for wininet.ParseX509EncodedCertificateForListBoxEntry ([Wine Bug #29842](https://bugs.winehq.org/show_bug.cgi?id=29842))
* Add stubs for D3DXCreateAnimationController interface
* Add support for CopyFileEx progress callback ([Wine Bug #22692](https://bugs.winehq.org/show_bug.cgi?id=22692))
* Add support for GetPropValue to PulseAudio backend
* Add support for process specific debug channels
* Add support for wbemprox Win32_SystemEnclosure table ([Wine Bug #34517](https://bugs.winehq.org/show_bug.cgi?id=34517))
* Adobe Reader needs ITextSelection_fnGetDuplicate implementation
* Allow selection of audio device for PulseAudio backend
* Allow special characters in pipe names ([Wine Bug #28995](https://bugs.winehq.org/show_bug.cgi?id=28995))
* Allow to cancel a file operation via progress callback ([Wine Bug #22690](https://bugs.winehq.org/show_bug.cgi?id=22690))
* Allow to edit winecfg library override by double clicking
* Allow to open files/directories without any access rights in order to query attributes
* Allow to override number of quality levels for D3DMULTISAMPLE_NONMASKABLE. ([Wine Bug #12652](https://bugs.winehq.org/show_bug.cgi?id=12652))
* Anno 1602 installer depends on Windows 98 behavior of SHFileOperationW ([Wine Bug #37916](https://bugs.winehq.org/show_bug.cgi?id=37916))
* Audio stuttering and performance drops in multiple applications ([Wine Bug #30639](https://bugs.winehq.org/show_bug.cgi?id=30639))
* Avoid crashing when broken app tries to release surface although refcount is zero ([Wine Bug #18477](https://bugs.winehq.org/show_bug.cgi?id=18477))
* Avoid race-conditions in NtReadFile() operations with write watches.
* Avoid race-conditions of async WSARecv() operations with write watches.
* Avoid race-conditions with write watches in WS2_async_accept.
* Avseq crashes when multisampling is enabled ([Wine Bug #31998](https://bugs.winehq.org/show_bug.cgi?id=31998))
* Basic handling of write watches triggered while we're on the signal stack.
* Basic support for CUDA
* Black & White needs DXTn software decoding support ([Wine Bug #14939](https://bugs.winehq.org/show_bug.cgi?id=14939))
* CPU-Z fails to start because GetLogicalProcessorInformationEx returns FALSE
* Calculate msvcrt exponential math operations with higher precision ([Wine Bug #37149](https://bugs.winehq.org/show_bug.cgi?id=37149))
* Create HKLM\Software\Microsoft\Cryptography\MachineGuid registry key ([Wine Bug #38508](https://bugs.winehq.org/show_bug.cgi?id=38508))
* CreateProcess does not prioritize the working directory over the system search path ([Wine Bug #23934](https://bugs.winehq.org/show_bug.cgi?id=23934))
* D3DCompileShader should filter specific warning messages ([Wine Bug #33770](https://bugs.winehq.org/show_bug.cgi?id=33770))
* Do not append duplicate NULL characters when importing keys with regedit ([Wine Bug #37575](https://bugs.winehq.org/show_bug.cgi?id=37575))
* Do not fail when a used context is passed to wglShareLists ([Wine Bug #11436](https://bugs.winehq.org/show_bug.cgi?id=11436))
* Emulate \Device\Null using /dev/null ([Wine Bug #38107](https://bugs.winehq.org/show_bug.cgi?id=38107))
* Emulate access to KI_USER_SHARED_DATA kernel page on x86_64 ([Wine Bug #33849](https://bugs.winehq.org/show_bug.cgi?id=33849))
* Enforce that surfaces are flushed after ReleaseDC
* Ensure NtProtectVirtualMemory and NtCreateSection are on separate pages ([Wine Bug #33162](https://bugs.winehq.org/show_bug.cgi?id=33162))
* Ensure X11 input events are handled even without explicit message loop ([Wine Bug #8854](https://bugs.winehq.org/show_bug.cgi?id=8854))
* Exception during start of fr-043 caused by missing DXTn support ([Wine Bug #37391](https://bugs.winehq.org/show_bug.cgi?id=37391))
* Expose PKEY_AudioEndpoint_PhysicalSpeakers device property in PulseAudio driver
* FEAR 1 installer expects basic_string_wchar_dtor to return NULL ([Wine Bug #37358](https://bugs.winehq.org/show_bug.cgi?id=37358))
* Fallback to global key state for threads without a queue ([Wine Bug #27238](https://bugs.winehq.org/show_bug.cgi?id=27238))
* Fix NULL dereference in ICSeqCompressFrameStart ([Wine Bug #27595](https://bugs.winehq.org/show_bug.cgi?id=27595))
* Fix access violation when calling GetStringTypeW with NULL src. ([Wine Bug #37759](https://bugs.winehq.org/show_bug.cgi?id=37759))
* Fix black screen on startup introduced by pixelformat changes. ([Wine Bug #35950](https://bugs.winehq.org/show_bug.cgi?id=35950))
* Fix caps lock state issues with multiple processes ([Wine Bug #35907](https://bugs.winehq.org/show_bug.cgi?id=35907))
* Fix comparison of punctuation characters in lstrcmp ([Wine Bug #10767](https://bugs.winehq.org/show_bug.cgi?id=10767))
* Fix condition mask handling in RtlVerifyVersionInfo ([Wine Bug #36143](https://bugs.winehq.org/show_bug.cgi?id=36143))
* Fix crash in Space Rangers2 caused by missing DXTn support ([Wine Bug #24983](https://bugs.winehq.org/show_bug.cgi?id=24983))
* Fix crash in clip_cursor_notify caused by uninitialized TLS ([Wine Bug #36915](https://bugs.winehq.org/show_bug.cgi?id=36915))
* Fix crash of Trine Demo on start ([Wine Bug #19231](https://bugs.winehq.org/show_bug.cgi?id=19231))
* Fix crash of winedevice when relocation entry crosses page boundary ([Wine Bug #28254](https://bugs.winehq.org/show_bug.cgi?id=28254))
* Fix cursor clip regression / broken raw input in multiple games ([Wine Bug #33479](https://bugs.winehq.org/show_bug.cgi?id=33479))
* Fix device paths in HKLM\SYSTEM\MountedDevices ([Wine Bug #38235](https://bugs.winehq.org/show_bug.cgi?id=38235))
* Fix flickering introduced by pixelformat changes. ([Wine Bug #35718](https://bugs.winehq.org/show_bug.cgi?id=35718))
* Fix for ConnectNamedPort return value in overlapped mode ([Wine Bug #16550](https://bugs.winehq.org/show_bug.cgi?id=16550))
* Fix for programs leaking wndproc slots ([Wine Bug #32451](https://bugs.winehq.org/show_bug.cgi?id=32451))
* Fix graphical corruption in FarCry 3 with NVIDIA drivers ([Wine Bug #35062](https://bugs.winehq.org/show_bug.cgi?id=35062))
* Fix gray screen on startup introduced by pixelformat changes. ([Wine Bug #35975](https://bugs.winehq.org/show_bug.cgi?id=35975))
* Fix handling of ANSI NTLM credentials ([Wine Bug #37063](https://bugs.winehq.org/show_bug.cgi?id=37063))
* Fix handling of empty section and key name for profile files. ([Wine Bug #8036](https://bugs.winehq.org/show_bug.cgi?id=8036))
* Fix handling of invert_y in DrawTextExW ([Wine Bug #22109](https://bugs.winehq.org/show_bug.cgi?id=22109))
* Fix handling of opening read-only files for FILE_DELETE_ON_CLOSE ([Wine Bug #38417](https://bugs.winehq.org/show_bug.cgi?id=38417))
* Fix handling of window attributes for WS_EX_LAYERED | WS_EX_COMPOSITED ([Wine Bug #37876](https://bugs.winehq.org/show_bug.cgi?id=37876))
* Fix issues with dragging layers between images in Adobe Photoshop 7.0 ([Wine Bug #12007](https://bugs.winehq.org/show_bug.cgi?id=12007))
* Fix missing video introduced by pixelformat changes. ([Wine Bug #36900](https://bugs.winehq.org/show_bug.cgi?id=36900))
* Fix multithreading issues with fullscreen clipping ([Wine Bug #38087](https://bugs.winehq.org/show_bug.cgi?id=38087))
* Fix possible segfault in pulse_rd_loop of PulseAudio backend
* Fix race-condition when threads are killed during shutdown
* Fix regression caused by blacklisting supported OpenGL extensions ([Wine Bug #38480](https://bugs.winehq.org/show_bug.cgi?id=38480))
* Fix return value of ScrollWindowEx for invisible windows ([Wine Bug #37706](https://bugs.winehq.org/show_bug.cgi?id=37706))
* Fix texture corruption in CSI: Fatal Conspiracy ([Wine Bug #33768](https://bugs.winehq.org/show_bug.cgi?id=33768))
* Fix unintentional leaks with ntdll internals
* Fix wined3d performance drop introduced by pixelformat changes. ([Wine Bug #35655](https://bugs.winehq.org/show_bug.cgi?id=35655))
* Fix wrong colors in Wolfenstein (2009) ([Wine Bug #34692](https://bugs.winehq.org/show_bug.cgi?id=34692))
* Fix wrong defition of ntoskrnl.IoReleaseCancelSpinLock function.
* Fix wrong version of ID3DXEffect interface for d3dx9_24
* Fix wrong version of ID3DXEffect interface for d3dx9_25 ([Wine Bug #25138](https://bugs.winehq.org/show_bug.cgi?id=25138))
* Games For Windows Live 1.x expects a valid linker version in the PE header ([Wine Bug #28768](https://bugs.winehq.org/show_bug.cgi?id=28768))
* GetMessage should remove already seen messages with higher priority ([Wine Bug #28884](https://bugs.winehq.org/show_bug.cgi?id=28884))
* GetMonitorInfo returns the same name for all monitors ([Wine Bug #37709](https://bugs.winehq.org/show_bug.cgi?id=37709))
* GetSecurityInfo returns NULL DACL for process object ([Wine Bug #15980](https://bugs.winehq.org/show_bug.cgi?id=15980))
* Graphical issues in Inquisitor ([Wine Bug #32490](https://bugs.winehq.org/show_bug.cgi?id=32490))
* IOCTL_DVD_READ_STRUCTURE expects the wrong size of output buffer for some requests ([Wine Bug #37767](https://bugs.winehq.org/show_bug.cgi?id=37767))
* Ignore garbage after decoding gif lines ([Wine Bug #32227](https://bugs.winehq.org/show_bug.cgi?id=32227))
* Ignore unsupported flags for CoInternetSetFeatureEnabled ([Wine Bug #35197](https://bugs.winehq.org/show_bug.cgi?id=35197))
* Implement D3DXGetShaderOutputSemantics
* Implement DDENUMSURFACES_CANBECREATED in IDirectDraw7::EnumSurfaces ([Wine Bug #17233](https://bugs.winehq.org/show_bug.cgi?id=17233))
* Implement ID3DXEffect::FindNextValidTechnique ([Wine Bug #34101](https://bugs.winehq.org/show_bug.cgi?id=34101))
* Implement IDXGIOutput::GetDesc
* Implement SetFileInformationByHandle
* Implement a Microsoft Yahei replacement font ([Wine Bug #13829](https://bugs.winehq.org/show_bug.cgi?id=13829))
* Implement additional stubs for vcomp dlls ([Wine Bug #31640](https://bugs.winehq.org/show_bug.cgi?id=31640))
* Implement an Arial replacement font ([Wine Bug #32323](https://bugs.winehq.org/show_bug.cgi?id=32323))
* Implement combase.WindowsSubstring function
* Implement empty enumerator for IWiaDevMgr::EnumDeviceInfo ([Wine Bug #27775](https://bugs.winehq.org/show_bug.cgi?id=27775))
* Implement exclusive mode in PulseAudio backend ([Wine Bug #37042](https://bugs.winehq.org/show_bug.cgi?id=37042))
* Implement locking and synchronization of key states ([Wine Bug #31899](https://bugs.winehq.org/show_bug.cgi?id=31899))
* Implement mscoree._CorValidateImage for mono runtime
* Implement ntoskrnl driver testing framework.
* Implement ntoskrnl.KeInitializeMutex
* Implement proper handling of CLI .NET images in Wine library loader
* Implement stub for ntoskrnl.IoGetAttachedDeviceReference
* Implement stub for ntoskrnl.KeDelayExecutionThread.
* Implement stubs for ntoskrnl.Ex{Acquire,Release}FastMutexUnsafe
* Implement stubs for ntoskrnl.ObReferenceObjectByPointer and ntoskrnl.ObDereferenceObject
* Implement threadpool timers ([Wine Bug #37306](https://bugs.winehq.org/show_bug.cgi?id=37306))
* Implement threadpool wait objects
* Implement threadpool work items ([Wine Bug #32531](https://bugs.winehq.org/show_bug.cgi?id=32531))
* Improve stub for AEV_GetVolumeRange ([Wine Bug #35658](https://bugs.winehq.org/show_bug.cgi?id=35658))
* Improve stub for ID3DXEffectImpl_CloneEffect
* Improve stubs for AEV_{Get,Set}MasterVolumeLevel
* Improve stubs for AEV_{Get,Set}Mute
* Improvement for heap allocation performance
* Jedi Knight: Dark Forces II crashes with winmm set to native ([Wine Bug #37983](https://bugs.winehq.org/show_bug.cgi?id=37983))
* Lego Stunt Rally requires DXTn software de/encoding support ([Wine Bug #25486](https://bugs.winehq.org/show_bug.cgi?id=25486))
* ~~Lockfree algorithm for filedescriptor cache (improves file access speed)~~
* MSVCRT crashes when NULL is passed as string to atof or strtod ([Wine Bug #32550](https://bugs.winehq.org/show_bug.cgi?id=32550))
* MSYS2 expects correct handling of WRITECOPY memory protection ([Wine Bug #35561](https://bugs.winehq.org/show_bug.cgi?id=35561))
* Make it possible to change media center / tablet pc status ([Wine Bug #18732](https://bugs.winehq.org/show_bug.cgi?id=18732))
* MediaCoder needs CUDA for video encoding ([Wine Bug #37664](https://bugs.winehq.org/show_bug.cgi?id=37664))
* Multiple applications need EnumDisplayDevicesW implementation ([Wine Bug #34978](https://bugs.winehq.org/show_bug.cgi?id=34978))
* Multiple applications start wrong executable if whitespace present in name ([Wine Bug #19666](https://bugs.winehq.org/show_bug.cgi?id=19666))
* Need for Speed 3 installer requires devices in HKEY_DYN_DATA ([Wine Bug #7115](https://bugs.winehq.org/show_bug.cgi?id=7115))
* OpenClipboard with current owner shouldn't fail ([Wine Bug #2805](https://bugs.winehq.org/show_bug.cgi?id=2805))
* Other Pipelight-specific enhancements
* Port Royale doesn't display ocean correctly ([Wine Bug #17913](https://bugs.winehq.org/show_bug.cgi?id=17913))
* Prevent window managers from grouping all wine programs together ([Wine Bug #32699](https://bugs.winehq.org/show_bug.cgi?id=32699))
* Process APC calls before starting process
* Process Hacker 2.x needs ntoskrnl.ProbeForRead ([Wine Bug #38103](https://bugs.winehq.org/show_bug.cgi?id=38103))
* ~~Properly handle closing sockets during a select call~~ ([Wine Bug #38399](https://bugs.winehq.org/show_bug.cgi?id=38399))
* Python PIP needs better NtQueryInformationJobObject stub
* Reduced SetTimer minimum value from 10 ms to 5 ms (improves Silverlight framerates)
* Reset device state in SysKeyboard*Impl_Acquire ([Wine Bug #11607](https://bugs.winehq.org/show_bug.cgi?id=11607))
* Return an error when trying to open a terminated process ([Wine Bug #37087](https://bugs.winehq.org/show_bug.cgi?id=37087))
* Return correct IMediaSeeking stream positions in quartz ([Wine Bug #23174](https://bugs.winehq.org/show_bug.cgi?id=23174))
* Return correct device type for cd devices without medium
* Return correct values for GetThreadTimes function ([Wine Bug #20230](https://bugs.winehq.org/show_bug.cgi?id=20230))
* ~~Return failure in NtProtectVirtualMemory when last argument is omitted~~ ([Wine Bug #38495](https://bugs.winehq.org/show_bug.cgi?id=38495))
* SO_CONNECT_TIME returns the appropriate time
* Scrolling causes mouse and screen to lock in Call to Power II ([Wine Bug #34559](https://bugs.winehq.org/show_bug.cgi?id=34559))
* Send WM_PAINT event during dialog creation ([Wine Bug #35652](https://bugs.winehq.org/show_bug.cgi?id=35652))
* Set last error when GetRawInputDeviceList fails ([Wine Bug #37667](https://bugs.winehq.org/show_bug.cgi?id=37667))
* Show unmounted devices in winecfg and allow changing the unix path
* Software support for Environmental Audio Extensions (EAX)
* Super Mario 3: Mario Forever fails to load keyboard mapping from profile files. ([Wine Bug #18099](https://bugs.winehq.org/show_bug.cgi?id=18099))
* Support for 8bpp grayscale TIFF images with 8bpp alpha channel ([Wine Bug #38027](https://bugs.winehq.org/show_bug.cgi?id=38027))
* Support for AllocateAndGetTcpExTableFromStack ([Wine Bug #34372](https://bugs.winehq.org/show_bug.cgi?id=34372))
* Support for BindImageEx ([Wine Bug #3591](https://bugs.winehq.org/show_bug.cgi?id=3591))
* Support for CSMT (command stream) to increase graphic performance ([Wine Bug #11674](https://bugs.winehq.org/show_bug.cgi?id=11674))
* Support for CUDA GPU video decoding
* Support for D3DXComputeNormals ([Wine Bug #26379](https://bugs.winehq.org/show_bug.cgi?id=26379))
* Support for D3DXGetShaderInputSemantics ([Wine Bug #22682](https://bugs.winehq.org/show_bug.cgi?id=22682))
* Support for DDS file format in D3DXSaveTextureToFileInMemory ([Wine Bug #26898](https://bugs.winehq.org/show_bug.cgi?id=26898))
* Support for DOS hidden/system file attributes ([Wine Bug #9158](https://bugs.winehq.org/show_bug.cgi?id=9158))
* Support for FileFsFullSizeInformation information class
* Support for GdipCreateRegionRgnData ([Wine Bug #34843](https://bugs.winehq.org/show_bug.cgi?id=34843))
* Support for GetFinalPathNameByHandle ([Wine Bug #34851](https://bugs.winehq.org/show_bug.cgi?id=34851))
* Support for GetSystemTimes ([Wine Bug #19813](https://bugs.winehq.org/show_bug.cgi?id=19813))
* Support for GetVolumePathName
* Support for H264 DXVA2 GPU video decoding through vaapi
* Support for ID3DXFont::DrawTextA/W ([Wine Bug #24754](https://bugs.winehq.org/show_bug.cgi?id=24754))
* Support for ID3DXSkinInfoImpl_UpdateSkinnedMesh ([Wine Bug #32572](https://bugs.winehq.org/show_bug.cgi?id=32572))
* Support for ITextDocument_fnRange function ([Wine Bug #12458](https://bugs.winehq.org/show_bug.cgi?id=12458))
* Support for ITextRange, ITextFont and ITextPara ([Wine Bug #18303](https://bugs.winehq.org/show_bug.cgi?id=18303))
* Support for Junction Points ([Wine Bug #12401](https://bugs.winehq.org/show_bug.cgi?id=12401))
* Support for KF_FLAG_DEFAULT_PATH in SHGetKnownFolderPath ([Wine Bug #30385](https://bugs.winehq.org/show_bug.cgi?id=30385))
* Support for LoadIconMetric ([Wine Bug #35375](https://bugs.winehq.org/show_bug.cgi?id=35375))
* Support for MPEG2 DXVA2 GPU video decoding through vaapi
* Support for NVIDIA video encoder library (nvencodeapi)
* Support for NtQuerySection ([Wine Bug #37338](https://bugs.winehq.org/show_bug.cgi?id=37338))
* Support for NtSetInformationFile class FileDispositionInformation ([Wine Bug #30397](https://bugs.winehq.org/show_bug.cgi?id=30397))
* Support for PulseAudio backend for audio ([Wine Bug #10495](https://bugs.winehq.org/show_bug.cgi?id=10495))
* Support for RtlDecompressBuffer ([Wine Bug #37449](https://bugs.winehq.org/show_bug.cgi?id=37449))
* Support for SHCreateSessionKey ([Wine Bug #35630](https://bugs.winehq.org/show_bug.cgi?id=35630))
* Support for TransmitFile ([Wine Bug #5048](https://bugs.winehq.org/show_bug.cgi?id=5048))
* Support for WTSEnumerateProcessesW ([Wine Bug #29903](https://bugs.winehq.org/show_bug.cgi?id=29903))
* Support for extra large and jumbo icon lists in shell32 ([Wine Bug #24721](https://bugs.winehq.org/show_bug.cgi?id=24721))
* Support for inherited file ACLs ([Wine Bug #34406](https://bugs.winehq.org/show_bug.cgi?id=34406))
* Support for linux priority levels for faster performance
* Support for loader dll redirections
* Support for named pipe message mode (Linux only) ([Wine Bug #17195](https://bugs.winehq.org/show_bug.cgi?id=17195))
* Support for non-blocking SIO_ADDRESS_LIST_CHANGE requests ([Wine Bug #38062](https://bugs.winehq.org/show_bug.cgi?id=38062))
* Support for pasting HTML from Unix applications ([Wine Bug #7372](https://bugs.winehq.org/show_bug.cgi?id=7372))
* Support for process ACLs ([Wine Bug #22006](https://bugs.winehq.org/show_bug.cgi?id=22006))
* Support for setcap on wine-preloader ([Wine Bug #26256](https://bugs.winehq.org/show_bug.cgi?id=26256))
* Support for shell32 file operation progress dialog
* Support for stored file ACLs ([Wine Bug #33576](https://bugs.winehq.org/show_bug.cgi?id=33576))
* Try harder to get the host name address in getaddrinfo() ([Wine Bug #29609](https://bugs.winehq.org/show_bug.cgi?id=29609))
* Tumblebugs 2 requires DXTn software encoding support ([Wine Bug #29586](https://bugs.winehq.org/show_bug.cgi?id=29586))
* Update a XIM candidate position when cursor location changes ([Wine Bug #30938](https://bugs.winehq.org/show_bug.cgi?id=30938))
* Use actual program name if available to describe PulseAudio streams
* Use manual relay for RunDLL_CallEntry16 in shell32 ([Wine Bug #23033](https://bugs.winehq.org/show_bug.cgi?id=23033))
* Voobly expects correct handling of WRITECOPY memory protection ([Wine Bug #29384](https://bugs.winehq.org/show_bug.cgi?id=29384))
* Wine ignores IDF_CHECKFIRST flag in SetupPromptForDisk ([Wine Bug #20465](https://bugs.winehq.org/show_bug.cgi?id=20465))
* Workaround for shlwapi URLs with relative paths
* XEMBED support for embedding Wine windows inside Linux applications
* eRacer Demo doesn't correctly display text ([Wine Bug #29598](https://bugs.winehq.org/show_bug.cgi?id=29598))
* ntdll is missing WinSqm[Start|End]Session implementation ([Wine Bug #31971](https://bugs.winehq.org/show_bug.cgi?id=31971))
* wglDescribePixelFormat should return max index for NULL descriptor ([Wine Bug #6176](https://bugs.winehq.org/show_bug.cgi?id=6176))

