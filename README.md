What is Wine Staging?
---------------------

**Wine Staging** is the testing area of winehq.org. It contains bug fixes and
features, which have not been integrated into the development branch yet. The
idea of Wine Staging is to provide experimental features faster to end users and
to give developers the possibility to discuss and improve their patches before
they are integrated into the main branch. More information about Wine Staging
can also be found on our website [wine-staging.com](http://wine-staging.com).

Although we are reviewing and testing all patches carefully before adding them,
you may encounter additional bugs, which are not present in the development
branch. Do not hesitate to report such issues at winehq.org, so they can be
fixed before the feature gets integrated.


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

**Bug fixes and features in Wine Staging 1.9.0 [269]:**

*Note: The following list only contains features and bug fixes which are not
yet available in vanilla Wine. They are removed from the list as soon as they
are included upstream. The list also includes features and fixes from previous
releases, take a look at the
[changelog](https://github.com/wine-compholio/wine-staging/blob/master/staging/changelog)
for more details.*

* Add IDragSourceHelper stub interface ([Wine Bug #24699](https://bugs.winehq.org/show_bug.cgi?id=24699))
* Add IHTMLLocation::hash property's getter implementation ([Wine Bug #32967](https://bugs.winehq.org/show_bug.cgi?id=32967))
* Add a ProfileList\<UserSID> registry subkey ([Wine Bug #15670](https://bugs.winehq.org/show_bug.cgi?id=15670))
* Add implementation for comctl32.PROPSHEET_InsertPage. ([Wine Bug #25625](https://bugs.winehq.org/show_bug.cgi?id=25625))
* Add implementation for mfplat.MFTEnum ([Wine Bug #39309](https://bugs.winehq.org/show_bug.cgi?id=39309))
* Add implementation for mfplat.MFTRegister ([Wine Bug #37811](https://bugs.winehq.org/show_bug.cgi?id=37811))
* Add implementation for msidb commandline tool
* Add implementation for shlwapi.AssocGetPerceivedType
* Add nvapi stubs required for GPU PhysX support
* Add performance library registry keys needed by MS SQL Server Management Studio Express 2008 R2 ([Wine Bug #33661](https://bugs.winehq.org/show_bug.cgi?id=33661))
* Add semi-stub for FileFsVolumeInformation information class ([Wine Bug #21466](https://bugs.winehq.org/show_bug.cgi?id=21466))
* Add shell32 placeholder icons to match offsets with Windows ([Wine Bug #30185](https://bugs.winehq.org/show_bug.cgi?id=30185))
* Add stub dlls required for MSVC 2015 runtime library (Windows 10)
* Add stub for D3DXComputeNormalMap
* Add stub for D3DXFrameFind ([Wine Bug #38334](https://bugs.winehq.org/show_bug.cgi?id=38334))
* Add stub for NtSetLdtEntries/ZwSetLdtEntries ([Wine Bug #26268](https://bugs.winehq.org/show_bug.cgi?id=26268))
* Add stub for SetCoalescableTimer ([Wine Bug #39509](https://bugs.winehq.org/show_bug.cgi?id=39509))
* Add stub for ntoskrnl.ExAcquireResourceExclusiveLite
* Add stub for ntoskrnl.ExDeleteResourceLite
* Add stub for ntoskrnl.ExReleaseResourceForThread
* Add stub for ntoskrnl.KeWaitForMultipleObjects ([Wine Bug #32186](https://bugs.winehq.org/show_bug.cgi?id=32186))
* Add stub for ntoskrnl.Mm{Map,Unmap}LockedPages
* Add stub for ntoskrnl.PsRemoveLoadImageNotifyRoutine
* Add stub for wininet.ParseX509EncodedCertificateForListBoxEntry ([Wine Bug #29842](https://bugs.winehq.org/show_bug.cgi?id=29842))
* Add stub for winscard.SCardListReadersA/W ([Wine Bug #26978](https://bugs.winehq.org/show_bug.cgi?id=26978))
* Add stub for winspool.SetPrinterW level 8 ([Wine Bug #24645](https://bugs.winehq.org/show_bug.cgi?id=24645))
* Add stub for winsta.WinStationEnumerateW ([Wine Bug #38102](https://bugs.winehq.org/show_bug.cgi?id=38102))
* Add stub kernel32.FreeUserPhysicalPages ([Wine Bug #39543](https://bugs.winehq.org/show_bug.cgi?id=39543))
* Add stubbed ISWbemSecurity interfaces in wbemdisp
* Add stubs for D3DXCreateAnimationController interface
* Add stubs for additional wininet options in InternetSetOption
* Add support for CopyFileEx progress callback ([Wine Bug #22692](https://bugs.winehq.org/show_bug.cgi?id=22692))
* Add support for GTK3 theming
* Add support for GetPropValue to PulseAudio backend
* Add support for hiding wine version information from applications ([Wine Bug #38656](https://bugs.winehq.org/show_bug.cgi?id=38656))
* Add support for process specific debug channels
* Add wined3d detection for GeForce GT 425M ([Wine Bug #35054](https://bugs.winehq.org/show_bug.cgi?id=35054))
* Adobe Reader needs ITextSelection_fnGetDuplicate implementation
* Allow non-nullterminated string as working directory in kernel32.create_startup_info
* Allow selection of audio device for PulseAudio backend
* Allow special characters in pipe names ([Wine Bug #28995](https://bugs.winehq.org/show_bug.cgi?id=28995))
* Allow to cancel a file operation via progress callback ([Wine Bug #22690](https://bugs.winehq.org/show_bug.cgi?id=22690))
* Allow to edit winecfg library override by double clicking
* Allow to open files/directories without any access rights in order to query attributes
* Allow to override number of quality levels for D3DMULTISAMPLE_NONMASKABLE. ([Wine Bug #12652](https://bugs.winehq.org/show_bug.cgi?id=12652))
* Allow to set debug registers separately in NtSetContextThread ([Wine Bug #39454](https://bugs.winehq.org/show_bug.cgi?id=39454))
* Allow to set pixel format for desktop window
* Allow to specify default display frequency in registry
* Also send WM_CAPTURECHANGE when capture has not changed ([Wine Bug #13683](https://bugs.winehq.org/show_bug.cgi?id=13683))
* Always use 64-bit registry view on WOW64 setups
* Anno 1602 installer depends on Windows 98 behavior of SHFileOperationW ([Wine Bug #37916](https://bugs.winehq.org/show_bug.cgi?id=37916))
* Assign a drive serial number during prefix creation/update ([Wine Bug #17823](https://bugs.winehq.org/show_bug.cgi?id=17823))
* Audio stuttering and performance drops in multiple applications ([Wine Bug #30639](https://bugs.winehq.org/show_bug.cgi?id=30639))
* Avoid corruption of caret when SetCaretPos() is called
* Avoid crashing when broken app tries to release surface although refcount is zero ([Wine Bug #18477](https://bugs.winehq.org/show_bug.cgi?id=18477))
* Avoid race-conditions in NtReadFile() operations with write watches.
* Avoid race-conditions of async WSARecv() operations with write watches.
* Avoid race-conditions with write watches in WS2_async_accept.
* Basic handling of write watches triggered while we're on the signal stack.
* Basic support for CUDA
* Black & White needs DXTn software decoding support ([Wine Bug #14939](https://bugs.winehq.org/show_bug.cgi?id=14939))
* CPU-Z fails to start because GetLogicalProcessorInformationEx returns FALSE
* Calculate msvcrt exponential math operations with higher precision ([Wine Bug #37149](https://bugs.winehq.org/show_bug.cgi?id=37149))
* Catch invalid memory accesses in imagehlp.CheckSumMappedFile
* Check IsWoW64Process before calling Wow64 functions in UNIXFS_get_unix_path
* Check architecture before trying to load libraries ([Wine Bug #38021](https://bugs.winehq.org/show_bug.cgi?id=38021))
* Check handle type for HSPFILEQ handles ([Wine Bug #12332](https://bugs.winehq.org/show_bug.cgi?id=12332))
* Codepage conversion should fail when destination length is < 0
* CompareString should abort on first non-matching character ([Wine Bug #37556](https://bugs.winehq.org/show_bug.cgi?id=37556))
* Create Microsoft\Windows\Themes directory during Wineprefix creation ([Wine Bug #34910](https://bugs.winehq.org/show_bug.cgi?id=34910))
* Create stub files for system32/drivers/etc/{services,hosts,networks,protocol} ([Wine Bug #12076](https://bugs.winehq.org/show_bug.cgi?id=12076))
* CreateProcess does not prioritize the working directory over the system search path ([Wine Bug #23934](https://bugs.winehq.org/show_bug.cgi?id=23934))
* D3DCompileShader should filter specific warning messages ([Wine Bug #33770](https://bugs.winehq.org/show_bug.cgi?id=33770))
* Do not allow interruption of system APC in server_select ([Wine Bug #14697](https://bugs.winehq.org/show_bug.cgi?id=14697))
* Do not allow to deallocate thread stack for current thread
* Do not fail when a used context is passed to wglShareLists ([Wine Bug #11436](https://bugs.winehq.org/show_bug.cgi?id=11436))
* Do not hold reference on parent process in wineserver ([Wine Bug #37087](https://bugs.winehq.org/show_bug.cgi?id=37087))
* Do not signal threads until they are really gone
* Do not use unixfs for devices without mountpoint
* Do not wait for hook thread startup in IDirectInput8::Initialize ([Wine Bug #21403](https://bugs.winehq.org/show_bug.cgi?id=21403))
* Ensure NtProtectVirtualMemory and NtCreateSection are on separate pages ([Wine Bug #33162](https://bugs.winehq.org/show_bug.cgi?id=33162))
* Ensure default route IP addresses are returned first in gethostbyname ([Wine Bug #22819](https://bugs.winehq.org/show_bug.cgi?id=22819))
* Exception during start of fr-043 caused by missing DXTn support ([Wine Bug #37391](https://bugs.winehq.org/show_bug.cgi?id=37391))
* Export additional OpenAL32 functions ([Wine Bug #38972](https://bugs.winehq.org/show_bug.cgi?id=38972))
* Expose PKEY_AudioEndpoint_PhysicalSpeakers device property in PulseAudio driver
* Fake success in IViewObject::Draw stub ([Wine Bug #30611](https://bugs.winehq.org/show_bug.cgi?id=30611))
* Fake success in kernel32.SetFileCompletionNotificationModes ([Wine Bug #38960](https://bugs.winehq.org/show_bug.cgi?id=38960))
* Fallback to default comspec when %COMSPEC% is not set
* Fallback to system ping command when CAP_NET_RAW is not available ([Wine Bug #8332](https://bugs.winehq.org/show_bug.cgi?id=8332))
* Fix broken textures in XIII Century: Death or Glory ([Wine Bug #25419](https://bugs.winehq.org/show_bug.cgi?id=25419))
* Fix calculation of listbox size when horizontal scrollbar is present ([Wine Bug #38142](https://bugs.winehq.org/show_bug.cgi?id=38142))
* Fix caps lock state issues with multiple processes ([Wine Bug #35907](https://bugs.winehq.org/show_bug.cgi?id=35907))
* Fix comparison of punctuation characters in lstrcmp ([Wine Bug #10767](https://bugs.winehq.org/show_bug.cgi?id=10767))
* Fix condition mask handling in RtlVerifyVersionInfo ([Wine Bug #36143](https://bugs.winehq.org/show_bug.cgi?id=36143))
* Fix crash in Space Rangers2 caused by missing DXTn support ([Wine Bug #24983](https://bugs.winehq.org/show_bug.cgi?id=24983))
* Fix crash of winedevice when relocation entry crosses page boundary ([Wine Bug #28254](https://bugs.winehq.org/show_bug.cgi?id=28254))
* Fix detection of case-insensitive systems in MSYS2
* Fix device paths in HKLM\SYSTEM\MountedDevices ([Wine Bug #38235](https://bugs.winehq.org/show_bug.cgi?id=38235))
* Fix error handling in DeferWindowPos when passing an invalid HWND ([Wine Bug #23187](https://bugs.winehq.org/show_bug.cgi?id=23187))
* Fix font loading in Capella ([Wine Bug #12377](https://bugs.winehq.org/show_bug.cgi?id=12377))
* Fix for ConnectNamedPort return value in overlapped mode ([Wine Bug #16550](https://bugs.winehq.org/show_bug.cgi?id=16550))
* Fix for programs leaking wndproc slots ([Wine Bug #32451](https://bugs.winehq.org/show_bug.cgi?id=32451))
* Fix graphical corruption in FarCry 3 with NVIDIA drivers ([Wine Bug #35062](https://bugs.winehq.org/show_bug.cgi?id=35062))
* Fix handling of ANSI NTLM credentials ([Wine Bug #37063](https://bugs.winehq.org/show_bug.cgi?id=37063))
* Fix handling of empty section and key name for profile files. ([Wine Bug #8036](https://bugs.winehq.org/show_bug.cgi?id=8036))
* Fix handling of invert_y in DrawTextExW ([Wine Bug #22109](https://bugs.winehq.org/show_bug.cgi?id=22109))
* Fix handling of window attributes for WS_EX_LAYERED | WS_EX_COMPOSITED ([Wine Bug #37876](https://bugs.winehq.org/show_bug.cgi?id=37876))
* Fix implementation of msvcrt.close when stdout == stderr
* Fix issue causing applications to report magic loopback address instead of real IP ([Wine Bug #37271](https://bugs.winehq.org/show_bug.cgi?id=37271))
* Fix issues with dragging layers between images in Adobe Photoshop 7.0 ([Wine Bug #12007](https://bugs.winehq.org/show_bug.cgi?id=12007))
* Fix multithreading issues with fullscreen clipping ([Wine Bug #38087](https://bugs.winehq.org/show_bug.cgi?id=38087))
* Fix possible leak of explorer.exe processes and implement proper desktop refcounting
* Fix possible segfault in pulse_rd_loop of PulseAudio backend
* Fix race-condition when threads are killed during shutdown
* Fix return value of ScrollWindowEx for invisible windows ([Wine Bug #37706](https://bugs.winehq.org/show_bug.cgi?id=37706))
* Fix scaling behaviour of images and mipmap levels in IDirect3DTexture2_Load (needed for example by Prezzie Hunt)
* Fix texture corruption in CSI: Fatal Conspiracy ([Wine Bug #33768](https://bugs.winehq.org/show_bug.cgi?id=33768))
* Fix the initialization of combined DACLs when the new DACL is empty ([Wine Bug #38423](https://bugs.winehq.org/show_bug.cgi?id=38423))
* Fix unintentional leaks with ntdll internals
* Fix wrong colors in Wolfenstein (2009) ([Wine Bug #34692](https://bugs.winehq.org/show_bug.cgi?id=34692))
* Fix wrong defition of ntoskrnl.IoReleaseCancelSpinLock function.
* Fix wrong version of ID3DXEffect interface for d3dx9_24
* Fix wrong version of ID3DXEffect interface for d3dx9_25 ([Wine Bug #25138](https://bugs.winehq.org/show_bug.cgi?id=25138))
* GetMessage should remove already seen messages with higher priority ([Wine Bug #28884](https://bugs.winehq.org/show_bug.cgi?id=28884))
* GetMonitorInfo returns the same name for all monitors ([Wine Bug #37709](https://bugs.winehq.org/show_bug.cgi?id=37709))
* GetSecurityInfo returns NULL DACL for process object ([Wine Bug #15980](https://bugs.winehq.org/show_bug.cgi?id=15980))
* Globally invalidate key state on changes in other threads ([Wine Bug #29871](https://bugs.winehq.org/show_bug.cgi?id=29871))
* Graphical issues in Inquisitor ([Wine Bug #32490](https://bugs.winehq.org/show_bug.cgi?id=32490))
* Ignore socket type for protocol IPPROTO_IPV6 in getaddrinfo
* Implement AMStream GetMultiMediaStream functions ([Wine Bug #37090](https://bugs.winehq.org/show_bug.cgi?id=37090))
* Implement D3DXGetShaderOutputSemantics
* Implement DDENUMSURFACES_CANBECREATED in IDirectDraw7::EnumSurfaces ([Wine Bug #17233](https://bugs.winehq.org/show_bug.cgi?id=17233))
* Implement FileNamesInformation class support for NtQueryDirectoryFile
* Implement FolderImpl_Items and stubbed FolderItems interface
* Implement ID3DXEffect::FindNextValidTechnique ([Wine Bug #34101](https://bugs.winehq.org/show_bug.cgi?id=34101))
* ~~Implement SystemHandleInformation info class~~
* Implement a Courier New replacement font ([Wine Bug #20456](https://bugs.winehq.org/show_bug.cgi?id=20456))
* Implement a Microsoft Yahei replacement font ([Wine Bug #13829](https://bugs.winehq.org/show_bug.cgi?id=13829))
* Implement a Times New Roman replacement font ([Wine Bug #32342](https://bugs.winehq.org/show_bug.cgi?id=32342))
* Implement additional stub functions in authz.dll
* Implement an Arial replacement font ([Wine Bug #32323](https://bugs.winehq.org/show_bug.cgi?id=32323))
* Implement default homepage button in inetcpl.cpl
* Implement dinput device property DIPROP_USERNAME ([Wine Bug #39667](https://bugs.winehq.org/show_bug.cgi?id=39667))
* Implement enumeration of sound devices and basic properties to dxdiagn ([Wine Bug #32613](https://bugs.winehq.org/show_bug.cgi?id=32613))
* Implement exclusive mode in PulseAudio backend ([Wine Bug #37042](https://bugs.winehq.org/show_bug.cgi?id=37042))
* Implement general tab for file property dialog
* Implement hal.KeQueryPerformanceCounter ([Wine Bug #39500](https://bugs.winehq.org/show_bug.cgi?id=39500))
* Implement locking and synchronization of key states ([Wine Bug #31899](https://bugs.winehq.org/show_bug.cgi?id=31899))
* Implement marshalling for TKIND_COCLASS ([Wine Bug #19016](https://bugs.winehq.org/show_bug.cgi?id=19016))
* Implement mscoree._CorValidateImage for mono runtime ([Wine Bug #38662](https://bugs.winehq.org/show_bug.cgi?id=38662))
* Implement ntoskrnl driver testing framework.
* Implement ntoskrnl.KeInitializeMutex
* Implement proper handling of CLI .NET images in Wine library loader ([Wine Bug #38661](https://bugs.winehq.org/show_bug.cgi?id=38661))
* Implement shell32 NewMenu class with new folder item ([Wine Bug #24812](https://bugs.winehq.org/show_bug.cgi?id=24812))
* Implement special handling for calling GetChildContainer with an empty string ([Wine Bug #38014](https://bugs.winehq.org/show_bug.cgi?id=38014))
* Implement stub for ProcessQuotaLimits info class
* Implement stub for hid.HidP_TranslateUsagesToI8042ScanCodes ([Wine Bug #39447](https://bugs.winehq.org/show_bug.cgi?id=39447))
* Implement stub for ntoskrnl.IoGetAttachedDeviceReference
* Implement stub for ntoskrnl.KeDelayExecutionThread.
* Implement stubless proxies on x86_64 ([Wine Bug #26768](https://bugs.winehq.org/show_bug.cgi?id=26768))
* Implement stubs for ntoskrnl.Ex{Acquire,Release}FastMutexUnsafe
* Implement stubs for ntoskrnl.ObReferenceObjectByPointer and ntoskrnl.ObDereferenceObject
* Implement support for "Purist Mode" (override for all dlls)
* Improve INetFwAuthorizedApplication::get_ProcessImageFileName stub
* Improve ReadDataAvailable handling in FilePipeLocalInformation class
* Improve detection of symbol charset for old truetype fonts ([Wine Bug #33117](https://bugs.winehq.org/show_bug.cgi?id=33117))
* Improve startup performance by delaying font initialization
* Improve stub for AEV_GetVolumeRange ([Wine Bug #35658](https://bugs.winehq.org/show_bug.cgi?id=35658))
* Improve stub for ID3DXEffectImpl_CloneEffect
* Improve stub for NtQueryEaFile
* Improve stubs for AEV_{Get,Set}MasterVolumeLevel
* Improve stubs for AEV_{Get,Set}Mute
* Improve stubs for dxgi MakeWindowAssociation and GetWindowAssociation
* Improvement for heap allocation performance
* Initial implementation of wusa.exe (MSU package installer) ([Wine Bug #26757](https://bugs.winehq.org/show_bug.cgi?id=26757))
* Initialize *lpcDevices in RasEnumDevicesA ([Wine Bug #30378](https://bugs.winehq.org/show_bug.cgi?id=30378))
* Initialize System\CurrentControlSet\Control\TimeZoneInformation registry keys
* Jedi Knight: Dark Forces II crashes with winmm set to native ([Wine Bug #37983](https://bugs.winehq.org/show_bug.cgi?id=37983))
* Lego Stunt Rally requires DXTn software de/encoding support ([Wine Bug #25486](https://bugs.winehq.org/show_bug.cgi?id=25486))
* MSYS2 expects correct handling of WRITECOPY memory protection ([Wine Bug #35561](https://bugs.winehq.org/show_bug.cgi?id=35561))
* Make ddraw1 and ddraw_surface1 vtable as writable ([Wine Bug #39534](https://bugs.winehq.org/show_bug.cgi?id=39534))
* Make it possible to change media center / tablet pc status ([Wine Bug #18732](https://bugs.winehq.org/show_bug.cgi?id=18732))
* Map EXDEV error code to STATUS_NOT_SAME_DEVICE
* MediaCoder needs CUDA for video encoding ([Wine Bug #37664](https://bugs.winehq.org/show_bug.cgi?id=37664))
* Multiple applications need EnumDisplayDevicesW implementation ([Wine Bug #34978](https://bugs.winehq.org/show_bug.cgi?id=34978))
* Need for Speed 3 installer requires devices in HKEY_DYN_DATA ([Wine Bug #7115](https://bugs.winehq.org/show_bug.cgi?id=7115))
* Only set SFGAO_HASSUBFOLDER when there are really subfolders ([Wine Bug #24851](https://bugs.winehq.org/show_bug.cgi?id=24851))
* Other Pipelight-specific enhancements
* Pass MOUSEHOOKSTRUCTEX struct to mouse hook callback ([Wine Bug #38314](https://bugs.winehq.org/show_bug.cgi?id=38314))
* Port Royale doesn't display ocean correctly ([Wine Bug #17913](https://bugs.winehq.org/show_bug.cgi?id=17913))
* Prevent window managers from grouping all wine programs together ([Wine Bug #32699](https://bugs.winehq.org/show_bug.cgi?id=32699))
* Process APC calls before starting process
* Properly close sockets when WSACleanup is called ([Wine Bug #18670](https://bugs.winehq.org/show_bug.cgi?id=18670))
* Properly handle multiple registry notifications per key
* Properly implement GetLargestConsoleWindowSize ([Wine Bug #10919](https://bugs.winehq.org/show_bug.cgi?id=10919))
* Properly implement imagehlp.ImageLoad and ImageUnload ([Wine Bug #23455](https://bugs.winehq.org/show_bug.cgi?id=23455))
* Properly initialize caps->dwZBufferBitDepths in ddraw7_GetCaps ([Wine Bug #27002](https://bugs.winehq.org/show_bug.cgi?id=27002))
* Properly render themed buttons when they are pressed ([Wine Bug #37584](https://bugs.winehq.org/show_bug.cgi?id=37584))
* Reduced SetTimer minimum value from 10 ms to 5 ms (improves Silverlight framerates)
* Refresh MDI menus when DefMDIChildProc(WM_SETTEXT) is called ([Wine Bug #21855](https://bugs.winehq.org/show_bug.cgi?id=21855))
* Report correct ObjectName for NamedPipe wineserver objects
* Return STATUS_INVALID_DEVICE_REQUEST when trying to call NtReadFile on directory
* Return WN_NOT_CONNECTED from WNetGetUniversalName REMOTE_NAME_INFO_LEVEL stub ([Wine Bug #39452](https://bugs.winehq.org/show_bug.cgi?id=39452))
* Return a valid mesh in D3DXCreateTeapot ([Wine Bug #36884](https://bugs.winehq.org/show_bug.cgi?id=36884))
* Return correct IMediaSeeking stream positions in quartz
* Return correct values for GetThreadTimes function ([Wine Bug #20230](https://bugs.winehq.org/show_bug.cgi?id=20230))
* Return dummy ID3DXSkinInfo interface when skinning info not present ([Wine Bug #33904](https://bugs.winehq.org/show_bug.cgi?id=33904))
* Return fake device type when systemroot is located on virtual disk ([Wine Bug #36546](https://bugs.winehq.org/show_bug.cgi?id=36546))
* Return proper status codes when NtReadFile/NtWriteFile is called on closed (but not disconnected) pipe
* SHFileOperation with FO_MOVE should create new directory on Vista+ ([Wine Bug #25207](https://bugs.winehq.org/show_bug.cgi?id=25207))
* SHMapHandle should not set error when NULL is passed as hShared
* SO_CONNECT_TIME returns the appropriate time
* Send WM_PAINT event during dialog creation ([Wine Bug #35652](https://bugs.winehq.org/show_bug.cgi?id=35652))
* Set EOF on file which has a memory mapping should fail
* Set NamedPipeState to FILE_PIPE_CLOSING_STATE on broken pipe in NtQueryInformationFile
* Share source of d3dx9_36 with d3dx9_33 to avoid Wine DLL forwards ([Wine Bug #21817](https://bugs.winehq.org/show_bug.cgi?id=21817))
* Show unmounted devices in winecfg and allow changing the unix path
* Silence repeated FIXME message in surface_cpu_blt
* Silence repeated LocaleNameToLCID/LCIDToLocaleName unsupported flags FIXMEs ([Wine Bug #30076](https://bugs.winehq.org/show_bug.cgi?id=30076))
* Skip unknown item when decoding a CMS certificate ([Wine Bug #34388](https://bugs.winehq.org/show_bug.cgi?id=34388))
* Software support for Environmental Audio Extensions (EAX)
* Start SERVICE_FILE_SYSTEM_DRIVER services with winedevice ([Wine Bug #35824](https://bugs.winehq.org/show_bug.cgi?id=35824))
* Super Mario 3: Mario Forever fails to load keyboard mapping from profile files. ([Wine Bug #18099](https://bugs.winehq.org/show_bug.cgi?id=18099))
* Support for AllocateAndGetTcpExTableFromStack ([Wine Bug #34372](https://bugs.winehq.org/show_bug.cgi?id=34372))
* Support for BindImageEx ([Wine Bug #3591](https://bugs.winehq.org/show_bug.cgi?id=3591))
* Support for CSMT (command stream) to increase graphic performance ([Wine Bug #11674](https://bugs.winehq.org/show_bug.cgi?id=11674))
* Support for CUDA GPU video decoding
* Support for D3DXGetShaderInputSemantics ([Wine Bug #22682](https://bugs.winehq.org/show_bug.cgi?id=22682))
* Support for DDS file format in D3DXSaveTextureToFileInMemory ([Wine Bug #26898](https://bugs.winehq.org/show_bug.cgi?id=26898))
* Support for DOS hidden/system file attributes ([Wine Bug #9158](https://bugs.winehq.org/show_bug.cgi?id=9158))
* Support for FileFsFullSizeInformation information class
* Support for GetFinalPathNameByHandle ([Wine Bug #34851](https://bugs.winehq.org/show_bug.cgi?id=34851))
* Support for H264 DXVA2 GPU video decoding through vaapi
* Support for ID3DXFont::DrawTextA/W ([Wine Bug #24754](https://bugs.winehq.org/show_bug.cgi?id=24754))
* Support for ID3DXSkinInfoImpl_UpdateSkinnedMesh ([Wine Bug #32572](https://bugs.winehq.org/show_bug.cgi?id=32572))
* Support for Junction Points ([Wine Bug #12401](https://bugs.winehq.org/show_bug.cgi?id=12401))
* Support for KF_FLAG_DEFAULT_PATH in SHGetKnownFolderPath ([Wine Bug #30385](https://bugs.winehq.org/show_bug.cgi?id=30385))
* Support for MPEG2 DXVA2 GPU video decoding through vaapi
* Support for NVIDIA video encoder library (nvencodeapi)
* Support for NtQuerySection ([Wine Bug #37338](https://bugs.winehq.org/show_bug.cgi?id=37338))
* Support for SHCreateSessionKey ([Wine Bug #35630](https://bugs.winehq.org/show_bug.cgi?id=35630))
* Support for WTSEnumerateProcessesW ([Wine Bug #29903](https://bugs.winehq.org/show_bug.cgi?id=29903))
* Support for extra large and jumbo icon lists in shell32 ([Wine Bug #24721](https://bugs.winehq.org/show_bug.cgi?id=24721))
* Support for inherited file ACLs
* Support for linux priority levels for faster performance
* Support for loader dll redirections
* Support for named pipe message mode (Linux only) ([Wine Bug #17195](https://bugs.winehq.org/show_bug.cgi?id=17195))
* Support for pasting HTML from Unix applications ([Wine Bug #7372](https://bugs.winehq.org/show_bug.cgi?id=7372))
* Support for process ACLs ([Wine Bug #22006](https://bugs.winehq.org/show_bug.cgi?id=22006))
* Support for setcap on wine-preloader ([Wine Bug #26256](https://bugs.winehq.org/show_bug.cgi?id=26256))
* Support for shell32 file operation progress dialog
* Support for stored file ACLs ([Wine Bug #33576](https://bugs.winehq.org/show_bug.cgi?id=33576))
* ~~SysAllocStringByteLen should align terminating null WCHAR~~
* Tumblebugs 2 requires DXTn software encoding support ([Wine Bug #29586](https://bugs.winehq.org/show_bug.cgi?id=29586))
* Update a XIM candidate position when cursor location changes ([Wine Bug #30938](https://bugs.winehq.org/show_bug.cgi?id=30938))
* Use GLX_MESA_query_renderer extension to get more exact GPU infos
* Use NVX_GPU_MEMORY_INFO extension for more exact video memory accounting on NVIDIA graphic cards
* Use POSIX implementation to enumerate directory content on FreeBSD ([Wine Bug #35397](https://bugs.winehq.org/show_bug.cgi?id=35397))
* Use actual program name if available to describe PulseAudio streams
* Use manual relay for RunDLL_CallEntry16 in shell32 ([Wine Bug #23033](https://bugs.winehq.org/show_bug.cgi?id=23033))
* Use video memory for rendering targets if possible ([Wine Bug #34906](https://bugs.winehq.org/show_bug.cgi?id=34906))
* Use wrapper functions for syscalls to appease Chromium sandbox (32-bit) ([Wine Bug #39403](https://bugs.winehq.org/show_bug.cgi?id=39403))
* Voobly expects correct handling of WRITECOPY memory protection ([Wine Bug #29384](https://bugs.winehq.org/show_bug.cgi?id=29384))
* Wine ignores IDF_CHECKFIRST flag in SetupPromptForDisk ([Wine Bug #20465](https://bugs.winehq.org/show_bug.cgi?id=20465))
* Workaround for shlwapi URLs with relative paths
* Workaround installation bug of IE7 caused by version bump
* XEMBED support for embedding Wine windows inside Linux applications
* eRacer Demo doesn't correctly display text ([Wine Bug #29598](https://bugs.winehq.org/show_bug.cgi?id=29598))
* ntdll is missing WinSqm[Start|End]Session implementation ([Wine Bug #31971](https://bugs.winehq.org/show_bug.cgi?id=31971))

