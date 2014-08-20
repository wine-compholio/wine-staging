What is Wine-Compholio?
=======================

The **Wine "Compholio" Edition** is a special patched version of Wine that
includes both patches written by our team directly and specific patches by
third party developers that we consider good enough for inclusion.  This can
be seen as a testing version in preparation for patches to be submitted
to upstream Wine - don't be surprised if you encounter additional bugs,
which are not present in regular wine, and always report such issues to us
(via github), so we can improve our fixes even further. Thanks!


Included bugfixes and improvements
----------------------------------

**Bugfixes and features included in the next upcoming release [11]:**

* Adobe Reader requires NtProtectVirtualMemory and NtCreateSection to be on separate pages ([Wine Bug #33162](http://bugs.winehq.org/show_bug.cgi?id=33162 "Acrobat Reader 11 crashes on start (native API application virtualization, NtProtectVirtualMemory removes execute page protection on its own code)"))
* Fix ITERATE_MoveFiles when no source- and destname is specified ([Wine Bug #10085](http://bugs.winehq.org/show_bug.cgi?id=10085 "Adobe Bridge CS2 complains that it can't start due to licensing restrictions (affects photoshop)"))
* Fix issue with invisible dragimages in ImageList ([Wine Bug #36761](http://bugs.winehq.org/show_bug.cgi?id=36761 "Imagelist invisible dragimage"))
* Gothic 2 demo expects an error when opening a terminating process ([Wine Bug #37087](http://bugs.winehq.org/show_bug.cgi?id=37087 "Gothic 2 english demo fails with 'Conflict: a hook process was found. Please deactivate all Antivirus and Anti-Trojan programs and debuggers.'"))
* Multiple applications need BCryptGetFipsAlgorithmMode ([Wine Bug #32194](http://bugs.winehq.org/show_bug.cgi?id=32194 "Multiple games and applications need bcrypt.dll.BCryptGetFipsAlgorithmMode (Chess Position Trainer, Terraria, .NET System.Security.Cryptography)"))
* Other Pipelight-specific enhancements
* Prevent window managers from grouping all wine programs together ([Wine Bug #32699](http://bugs.winehq.org/show_bug.cgi?id=32699 "Add StartupWMClass to .desktop files."))
* Support for DwmInvalidateIconicBitmaps ([Wine Bug #32977](http://bugs.winehq.org/show_bug.cgi?id=32977 "Solidworks 2012 needs unimplemented function dwmapi.dll.DwmInvalidateIconicBitmaps (Win7 mode)"))
* Support for Dynamic DST (daylight saving time) information in registry
* Support for GetFinalPathNameByHandle ([Wine Bug #36073](http://bugs.winehq.org/show_bug.cgi?id=36073 "OneDrive crashes on unimplemented function KERNEL32.dll.GetFinalPathNameByHandleW"))
* nVidia driver for high-end laptop cards does not list all supported resolutions


**Bugs fixed in Wine-Compholio 1.7.24 [45]:**

* ATL IOCS data should not be stored in GWLP_USERDATA ([Wine Bug #21767](http://bugs.winehq.org/show_bug.cgi?id=21767 "JLC's Internet TV crashes on startup"))
* Add Dynamic DST exceptions for Israel Standard Time ([Wine Bug #36374](http://bugs.winehq.org/show_bug.cgi?id=36374 "Israel timezone handled incorrectly"))
* Add default ACLs for user shell folders
* ~~Add support for Dynamic DST (daylight saving time) information in registry~~
* Allow special characters in pipe names ([Wine Bug #28995](http://bugs.winehq.org/show_bug.cgi?id=28995 "Unable to use named pipes with \">\" character in the name"))
* Audio stuttering and performance drops in multiple applications ([Wine Bug #30639](http://bugs.winehq.org/show_bug.cgi?id=30639 "Audio stuttering and performance drops in Star Wolves 3"))
* Fix comparison of punctuation characters in lstrcmp ([Wine Bug #10767](http://bugs.winehq.org/show_bug.cgi?id=10767 "lstrcmp and others do not compare punctuation characters correctly"))
* Fix for ConnectNamedPort return value in overlapped mode ([Wine Bug #16550](http://bugs.winehq.org/show_bug.cgi?id=16550 "ConnectNamedPort should never return OK in overlapped mode (affects chromium ui_tests.exe)"))
* Fix for programs leaking wndproc slots ([Wine Bug #32451](http://bugs.winehq.org/show_bug.cgi?id=32451 "Multiple GOG.com installer bundles show a broken/unresponsive dialog window during installation (installer process running out of wndproc slots)"))
* GetSecurityInfo returns NULL DACL for process object ([Wine Bug #15980](http://bugs.winehq.org/show_bug.cgi?id=15980 "Rhapsody 2 crashes on startup (GetSecurityInfo returns NULL DACL for process object)"))
* Implement a Microsoft Yahei replacement font ([Wine Bug #13829](http://bugs.winehq.org/show_bug.cgi?id=13829 "Wine does not have CJK fonts"))
* Implement an Arial replacement font ([Wine Bug #32323](http://bugs.winehq.org/show_bug.cgi?id=32323 "Netflix (Silverlight 4.x) and several .NET Framework 3.x/4.0 WPF apps require either Arial or Verdana to be installed"))
* Lockfree algorithm for filedescriptor cache (improves file access speed)
* Make it possible to change media center / tablet pc status ([Wine Bug #18732](http://bugs.winehq.org/show_bug.cgi?id=18732 "Microsoft Experience Pack for Tablet PC 1 refuses to install"))
* Need for Speed 3 installer requires devices in HKEY_DYN_DATA ([Wine Bug #7115](http://bugs.winehq.org/show_bug.cgi?id=7115 "Need for Speed III installer fails in Win9X mode, reporting \"Could not get 'HardWareKey' value\" (active PnP device keys in 'HKEY_DYN_DATA\\\\Config Manager\\\\Enum' missing)"))
* ~~Old games cannot locate software-only renderer~~ ([Wine Bug #32581](http://bugs.winehq.org/show_bug.cgi?id=32581 "Invalid dwFlags of reference rasterizer's HAL D3DDEVICEDESC"))
* ~~Other Pipelight specific enhancements~~
* Reduced SetTimer minimum value from 10 ms to 5 ms (improves Silverlight framerates)
* Return correct IMediaSeeking stream positions in quartz ([Wine Bug #23174](http://bugs.winehq.org/show_bug.cgi?id=23174 "Fallout 3: Diologue and Video/sound issues"))
* SO_CONNECT_TIME returns the appropriate time
* Set ldr.EntryPoint for main executable ([Wine Bug #33034](http://bugs.winehq.org/show_bug.cgi?id=33034 "Many GFWL (Games For Windows Live) 1.x/2.x/3.x games crash or exit silently on startup (DiRT 2/3, GTA IV Steam)"))
* Support for AllocateAndGetTcpExTableFromStack ([Wine Bug #34372](http://bugs.winehq.org/show_bug.cgi?id=34372 "Add missing function AllocateAndGetTcpExTableFromStack() to iphlpapi.dll"))
* Support for GetSystemTimes ([Wine Bug #19813](http://bugs.winehq.org/show_bug.cgi?id=19813 "Voddler needs GetSystemTimes to run"))
* Support for GetVolumePathName
* Support for ITextDocument_fnRange function ([Wine Bug #12458](http://bugs.winehq.org/show_bug.cgi?id=12458 "Multiple apps fail due to RichEdit ITextDocument_fnRange stub (MySQL Workbench, BlitzMaxDemo137)"))
* Support for ITextRange, ITextFont and ITextPara ([Wine Bug #18303](http://bugs.winehq.org/show_bug.cgi?id=18303 "Adobe Acrobat Pro 7: Crashes when selecting the \"edit\" menu while having a file open."))
* Support for Junction Points ([Wine Bug #12401](http://bugs.winehq.org/show_bug.cgi?id=12401 "Support junction points, i.e. DeviceIoCtl(FSCTL_SET_REPARSE_POINT/FSCTL_GET_REPARSE_POINT)"))
* Support for LoadIconMetric ([Wine Bug #35375](http://bugs.winehq.org/show_bug.cgi?id=35375 "Multiple applications need Vista+ API COMCTL32.dll.380 a.k.a. 'LoadIconMetric' (Solidworks 2013 systray monitor, Microsoft One/SkyDrive)"))
* Support for NtSetInformationFile class FileDispositionInformation ([Wine Bug #30397](http://bugs.winehq.org/show_bug.cgi?id=30397 "Multiple applications need support for NtSetInformationFile class FileDispositionInformation (Cygwin installer, Stylizer 5.x Visual CSS editor, Spoon Studio 2011 (ex Xenocode) application sandboxing scheme)"))
* Support for PulseAudio backend for audio ([Wine Bug #10495](http://bugs.winehq.org/show_bug.cgi?id=10495 "Wine should support PulseAudio"))
* Support for SHCreateSessionKey ([Wine Bug #35630](http://bugs.winehq.org/show_bug.cgi?id=35630 "SHCreateSessionKey is unimplemented"))
* Support for SetNamedPipeHandleState ([Wine Bug #17273](http://bugs.winehq.org/show_bug.cgi?id=17273 "Many apps and games need SetNamedPipeHandleState implementation (support for named pipe message mode)(FireFox+Flash, Win8/NET 4.x SDK/vcrun2012, WiX installers)"))
* Support for TOOLTIPS_GetTipText edge cases ([Wine Bug #30648](http://bugs.winehq.org/show_bug.cgi?id=30648 "SEGA Genesis / Mega Drive Classic Collection (Steam) crashes on startup"))
* Support for TransmitFile ([Wine Bug #5048](http://bugs.winehq.org/show_bug.cgi?id=5048 "Multiple applications and games need support for ws2_32 SIO_GET_EXTENSION_FUNCTION_POINTER TransmitFile (WSAID_TRANSMITFILE)"))
* Support for WTSEnumerateProcessesW ([Wine Bug #29903](http://bugs.winehq.org/show_bug.cgi?id=29903 "Some Microsoft debuggers fail to enumerate processes due to wtsapi32.WTSEnumerateProcessesW() being a stub (Microsoft Visual Studio 2005, DbgCLR from .NET 2.0 SDK)"))
* Support for [Get|Set]SystemFileCacheSize ([Wine Bug #35886](http://bugs.winehq.org/show_bug.cgi?id=35886 "Lotus Notes 9 'cacheset.exe' utility needs KERNEL32.dll.SetSystemFileCacheSize"))
* Support for extra large and jumbo icon lists in shell32 ([Wine Bug #24721](http://bugs.winehq.org/show_bug.cgi?id=24721 "Explorer++ crashes when choosing to view large icons or extra large icons"))
* Support for inherited file ACLs ([Wine Bug #34406](http://bugs.winehq.org/show_bug.cgi?id=34406 "Finale Notepad 2012 doesn't copy/create user files on program start"))
* Support for interface change notifications ([Wine Bug #32328](http://bugs.winehq.org/show_bug.cgi?id=32328 "Many .NET and Silverlight applications require SIO_ADDRESS_LIST_CHANGE for interface change notifications"))
* Support for process ACLs ([Wine Bug #22006](http://bugs.winehq.org/show_bug.cgi?id=22006 "OpenProcess does not enforce ACL"))
* Support for stored file ACLs ([Wine Bug #31858](http://bugs.winehq.org/show_bug.cgi?id=31858 "Netflix on Firefox fails with Internet Connection Problem when loading bar is at 99%"))
* Support for ws2_32.inet_pton ([Wine Bug #36713](http://bugs.winehq.org/show_bug.cgi?id=36713 "Watch_Dogs requires ws2_32.inet_pton"))
* Use manual relay for RunDLL_CallEntry16 in shell32 ([Wine Bug #23033](http://bugs.winehq.org/show_bug.cgi?id=23033 "Tages Protection v5.x: games report \"DLL not found shell.dll16.dll\" (Runaway 2: The Dream Of The Turtle, ...)"))
* Workaround for shlwapi URLs with relative paths
* XEMBED support for embedding Wine windows inside Linux applications


How to install Wine-Compholio
=============================

Ready-to-use packages for Wine-Compholio are available for a variety
of different Linux distributions directly for download. Just follow the
instructions below to install it (and all required dependencies). After the
installation, please take a look at the next section for instructions how
to use it in order to run your desired application.

**Important:** If you already have installed 'pipelight' on your system, there
is a good chance that you already have Wine-Compholio. Take a look at the
next section on how to find out if this is the case.

If your distribution is not listed below, feel free to add a feature request -
if the demand is high enough we might consider packaging it for additional
distributions.


![alt text](http://repos.fds-team.de/misc/images/ubuntu.png) Ubuntu / Linux Mint
--------------------------------------------------------------------------------

Please run the following commands from a terminal, one line after each other.
```bash
sudo add-apt-repository ppa:pipelight/stable
sudo apt-get update
sudo apt-get install --install-recommends wine-compholio
```

![alt text](http://repos.fds-team.de/misc/images/arch.png) Arch Linux
---------------------------------------------------------------------

As a first step you have to import the key for our repository, and set the
trust level to trusted:
```bash
sudo pacman-key -r E49CC0415DC2D5CA
sudo pacman-key --lsign-key E49CC0415DC2D5CA
```

Afterwards you have to add the following lines to `/etc/pacman.conf`:
```
[compholio]
Server = http://cdn.fds-team.de/stable/arch/$arch
```

Now you can install Wine-Compholio directly using `pacman`:
```bash
sudo pacman -Syu wine-compholio
```

![alt text](http://repos.fds-team.de/misc/images/debian.png) Debian Jessie/Sid
------------------------------------------------------------------------------

*(Instructions for Debian Wheezy can be found below)*

In order to install i386 packages on a 64-bit system, you have to run the
following command as a first step:
```bash
sudo dpkg --add-architecture i386
```

Afterwards import the key for our repository:
```bash
wget http://repos.fds-team.de/Release.key
sudo apt-key add Release.key
```

And add our repository at the end of your `/etc/apt/sources.list` file:
```
# For Debian Jessie add the following line:
deb http://cdn.fds-team.de/stable/debian/ jessie main

# For Debian Sid this one:
deb http://cdn.fds-team.de/stable/debian/ sid main
```

Afterwards update the package cache and install it:
```bash
sudo apt-get update
sudo apt-get install wine-compholio
```


![alt text](http://repos.fds-team.de/misc/images/debian.png) Debian Wheezy
--------------------------------------------------------------------------

In order to install i386 packages on a 64-bit system, you have to run the
following command as a first step:
```bash
sudo dpkg --add-architecture i386
```

Afterwards import the key for our repository:
```bash
wget http://download.opensuse.org/repositories/home:/DarkPlayer:/Pipelight/Debian_7.0/Release.key
sudo apt-key add Release.key
```

And add our repository at the end of your `/etc/apt/sources.list` file:
```
# For Debian Wheezy add the following line:
deb http://download.opensuse.org/repositories/home:/DarkPlayer:/Pipelight/Debian_7.0/ ./
```

Afterwards update the package cache and install it:
```bash
sudo apt-get update
sudo apt-get install wine-compholio
```


![alt text](http://repos.fds-team.de/misc/images/opensuse.png) OpenSUSE
-----------------------------------------------------------------------

All the following steps have to be executed as root user. As a first step
you have to add the repository - this step depends on the openSUSE version
you're using.

| openSUSE version    | Path component          |
| ------------------- | ----------------------- |
| openSUSE 12.2       | `/openSUSE_12.2/`       |
| openSUSE 12.3       | `/openSUSE_12.3/`       |
| openSUSE 13.1       | `/openSUSE_13.1/`       |
| openSUSE Factory    | `/openSUSE_Factory/`    |
| openSUSE Tumbleweed | `/openSUSE_Tumbleweed/` |

The following commandline is an example for openSUSE 13.1, for a different
version just replace the path component according to the table above:
```bash
zypper ar --refresh http://download.opensuse.org/repositories/home:/DarkPlayer:/Pipelight/openSUSE_13.1/home:DarkPlayer:Pipelight.repo
```

Afterwards just run the following commands to install it:
```bash
zypper ref
zypper install wine-compholio
```


![alt text](http://repos.fds-team.de/misc/images/fedora.png) Fedora
-------------------------------------------------------------------

**Warning:** In contrary to other distributions, its not possible to have both
a regular wine version and Wine-Compholio installed at the same time - using
the instructions below will replace your regular version. Moreover it will
be installed to `/usr/bin/wine` in contrary to `/opt/wine-compholio/bin/wine`.

As a first step you have to add the repository - this step depends on the
Fedora version you're using.

| Fedora version  | Patch component |
| --------------- | --------------- |
| Fedora 18       | `/Fedora_18/`   |
| Fedora 19       | `/Fedora_19/`   |
| Fedora 20       | `/Fedora_20/`   |

The following commandline is an example for Fedora 19, for a different version
just replace the path component according to the table above:
```bash
sudo wget http://download.opensuse.org/repositories/home:/DarkPlayer:/Pipelight/Fedora_19/home:DarkPlayer:Pipelight.repo -O /etc/yum.repos.d/pipelight.repo
```

Afterwards run the following command to install the package:
```bash
sudo yum install wine-compholio
```

Please note that you might run into trouble if the official Fedora package
(without compholio patches) is newer than the one from the repository above,
so if something doesn't work, always make sure that you have installed
our version. To do that just run:
```bash
/usr/bin/wine --patches
```

When you're using Wine-Compholio this will show to a list of all patches
included, for an unpatched version this command will fail.


![alt text](http://repos.fds-team.de/misc/images/mageia.png) Mageia 4
---------------------------------------------------------------------

As a first step please add the key for our repository
```bash
wget http://repos.fds-team.de/Release.key
rpm --import Release.key
```

If you're using a 32-bit version of Mageia just add the repository
for 32-bit packages:
```bash
sudo urpmi.addmedia "Compholio 32-bit" http://cdn.fds-team.de/stable/mageia/4/i586/
```

For a 64-bit version of Mageia you'll need both the 32-bit and the
64-bit repository:
```bash
sudo urpmi.addmedia "Compholio 32-bit" http://cdn.fds-team.de/stable/mageia/4/i586/
sudo urpmi.addmedia "Compholio 64-bit" http://cdn.fds-team.de/stable/mageia/4/x86_64/
```

Afterwards run the following commands to install the package:
```bash
sudo urpmi.update -a
sudo urpmi wine-compholio
```

Using Wine-Compholio
====================

Since we don't want to duplicate a lot of information here, we recommend
to take a look at the [official Wine FAQ](http://wiki.winehq.org/FAQ) for
general information about how to use Wine. The following part will mainly
concentrate on the differences between wine and Wine-Compholio.


Running Wine-Compholio
----------------------

**Using multiple Wine versions:** Unless you specify a special `WINEPREFIX`
environment variable, Wine-Compholio will use the same wineprefix `~/.wine`
(in your home directory) like regular wine. This allows you to use your
already installed programs directly, without much effort or reinstalling
them. Often you have both regular wine and Wine-Compholio installed at the
same time, which is *absolutely no problem* - by typing in either `wine`
(=regular wine) or `/opt/wine-compholio/bin/wine` you can decide, which
wine version you want to run. You can switch between versions as often as
you like - just make sure that all Windows programs have terminated before
starting them with a different version.

To run Wine-Compholio always type `/opt/wine-compholio/bin/wine`, for example:
```bash
cd ~/.wine/drive_c/<your path>/
/opt/wine-compholio/bin/wine game.exe
```

You also have to add `/opt/wine-compholio/bin/` when running other wine
related programs, here are some additional example:
```bash
# Initialize the wine prefix
/opt/wine-compholio/bin/wineboot

# Open the wine configuration
/opt/wine-compholio/bin/winecfg

# Run winepath to convert paths
/opt/wine-compholio/bin/winepath --unix 'c:\Windows'

# Kill the running wineserver instance
/opt/wine-compholio/bin/wineserver -k

...
```

If you're an experienced user, and always want to use Wine-Compholio, you
can also add `/opt/wine-compholio/bin` to your bash profile. We will not
go into detail here, because such a setup has the big disadvantage, that
it hides which version you're using - which is very important for getting
support or reporting bugs.


Submitting bugs
---------------

**Warning: Do not submit bug reports at bugs.winehq.org when using this
version!**

If you encounter any issues, the first thing you should do is to try it with
regular wine.  We're only a very small developer team, and although we would
like to do that, we probably cannot really solve all your Wine bugs. When
it turns out that the official Wine version also doesn't work, you can file
a bugreport at the official [Wine bugtracker](http://bugs.winehq.org/).
Feel free to mention that you also tested with Wine-Compholio, but all
bugreport related information (logs, crashdumps, ...) should concentrate
only on upstream wine.

If it turns out, that it works with upstream wine, but not with Wine-Compholio,
then it might be a regression caused by our patches. We would like you to
report this issue to us, so we can fix it in future versions. You can also
report issues, when testing with upstream Wine is impossible or it crashes
with a different error (for example much earlier).

When submitting a application related bug here on github, please make sure to
include at least the following information. Generally its always a good idea
to provide as much information as possible, since this will significantly
increase chances to provide support and to fix it.

1. **Which application triggers the bug**
    * Application name and version number
    * How to obtain it (download URL + checksum if public available)

2. **What exactly doesn't work**
    * Log of the terminal output of the application
    * For visual issues please additionally attach a screenshot, and describe
      what it should look like
    * *Optionally:* If you already know whats going wrong, please attach
      appropriate `WINEDEBUG` logs or excerpts showing the issue.

3. **Details about your WINEPREFIX**
    * *Recommended:* Test it in a new wine prefix, and report if this works
    * Did you install any overrides? (for examples by using `winetricks`)
    * Did you change any settings by running `winecfg`?

4. **Information about your Wine-Compholio version**
    * *Recommended:* Test with regular wine, and report if this works
    * Version number (`/opt/wine-compholio/bin/wine --version`)
    * Patches in your build (`/opt/wine-compholio/bin/wine --patches`)
    * Installed optional libraries (`/opt/wine-compholio/bin/wine --check-libs`)
