wine-compholio
==============

The Wine "Compholio" Edition repository includes a variety of patches for
Wine to run common Windows applications under Linux.

These patches fix the following Wine bugs:

* Support for TransmitFile ([Wine Bug #5048](http://bugs.winehq.org/show_bug.cgi?id=5048 "Multiple applications and games need support for ws2_32 SIO_GET_EXTENSION_FUNCTION_POINTER TransmitFile (WSAID_TRANSMITFILE)"))
* Need for Speed 3 installer requires devices in HKEY_DYN_DATA ([Wine Bug #7115](http://bugs.winehq.org/show_bug.cgi?id=7115 "Need for Speed III installer fails in Win9X mode, reporting \"Could not get 'HardWareKey' value\" (active PnP device keys in 'HKEY_DYN_DATA\\\\Config Manager\\\\Enum' missing)"))
* Support for Junction Points ([Wine Bug #12401](http://bugs.winehq.org/show_bug.cgi?id=12401 "Support junction points, i.e. DeviceIoCtl(FSCTL_SET_REPARSE_POINT/FSCTL_GET_REPARSE_POINT)"))
* Implement a Microsoft Yahei replacement font ([Wine Bug #13829](http://bugs.winehq.org/show_bug.cgi?id=13829 "Wine does not have CJK fonts"))
* GetSecurityInfo returns NULL DACL for process object ([Wine Bug #15980](http://bugs.winehq.org/show_bug.cgi?id=15980 "Rhapsody 2 crashes on startup (GetSecurityInfo returns NULL DACL for process object)"))
* Fix for ConnectNamedPort return value in overlapped mode ([Wine Bug #16550](http://bugs.winehq.org/show_bug.cgi?id=16550 "ConnectNamedPort should never return OK in overlapped mode (affects chromium ui_tests.exe)"))
* Workaround for TransactNamedPipe not being supported ([Wine Bug #17273](http://bugs.winehq.org/show_bug.cgi?id=17273 "Many apps and games need SetNamedPipeHandleState implementation (support for named pipe message mode)(FireFox+Flash, Win8/NET 4.x SDK/vcrun2012, WiX installers)"))
* ATL IOCS data should not be stored in GWLP_USERDATA ([Wine Bug #21767](http://bugs.winehq.org/show_bug.cgi?id=21767 "JLC's Internet TV crashes on startup"))
* Support for process ACLs ([Wine Bug #22006](http://bugs.winehq.org/show_bug.cgi?id=22006 "OpenProcess does not enforce ACL"))
* Create AppData\LocalLow in user profile directory ([Wine Bug #22896](http://bugs.winehq.org/show_bug.cgi?id=22896 "Multiple applications and games need support for shell32 FOLDERID_LocalAppDataLow (.NET based Unity Engine games, Java JRE 6 in Vista mode)"))
* Return correct IMediaSeeking stream positions in quartz ([Wine Bug #23174](http://bugs.winehq.org/show_bug.cgi?id=23174 "Fallout 3: Diologue and Video/sound issues"))
* Add implementation of WTSEnumerateProcessesW ([Wine Bug #29903](http://bugs.winehq.org/show_bug.cgi?id=29903 "Some Microsoft debuggers fail to enumerate processes due to wtsapi32.WTSEnumerateProcessesW() being a stub (Microsoft Visual Studio 2005, DbgCLR from .NET 2.0 SDK)"))
* Fix race conditions and deadlocks in strmbase/quartz ([Wine Bug #31566](http://bugs.winehq.org/show_bug.cgi?id=31566 "Fallout 3: regression causes block at critical section when radio is enabled"))
* Support for stored file ACLs ([Wine Bug #31858](http://bugs.winehq.org/show_bug.cgi?id=31858 "Netflix on Firefox fails with Internet Connection Problem when loading bar is at 99%"))
* Implement an Arial replacement font ([Wine Bug #32323](http://bugs.winehq.org/show_bug.cgi?id=32323 "Netflix (Silverlight 4.x) and several .NET Framework 3.x/4.0 WPF apps require either Arial or Verdana to be installed"))
* Support for interface change notifications ([Wine Bug #32328](http://bugs.winehq.org/show_bug.cgi?id=32328 "Many .NET and Silverlight applications require SIO_ADDRESS_LIST_CHANGE for interface change notifications"))
* Support for AllocateAndGetTcpExTableFromStack ([Wine Bug #34372](http://bugs.winehq.org/show_bug.cgi?id=34372 "Add missing function AllocateAndGetTcpExTableFromStack() to iphlpapi.dll"))
* Support for inherited file ACLs ([Wine Bug #34406](http://bugs.winehq.org/show_bug.cgi?id=34406 "Finale Notepad 2012 doesn't copy/create user files on program start"))
* SHCreateSessionKey not implemented ([Wine Bug #35630](http://bugs.winehq.org/show_bug.cgi?id=35630 "SHCreateSessionKey is unimplemented"))
* Add Dynamic DST exceptions for Israel Standard Time ([Wine Bug #36374](http://bugs.winehq.org/show_bug.cgi?id=36374 "Israel timezone handled incorrectly"))

Besides that the following additional changes are included:

* Add default ACLs for user shell folders
* Add support for Dynamic DST (daylight saving time) information in registry
* Lockfree algorithm for filedescriptor cache (improves file access speed)
* Other Pipelight specific enhancements
* Reduced SetTimer minimum value from 10 ms to 5 ms (improves Silverlight framerates)
* Support for GetVolumePathName
* Support for PulseAudio backend for audio
* Workaround for shlwapi URLs with relative paths
* XEMBED support for embedding Wine windows inside Linux applications


How to install wine-compholio
=============================

Ready-to-use packages for wine-compholio are available for a variety of different
Linux distributions directly for download. Just follow the instructions below to
install it (and all required dependencies). After the installation, please take a
look at the next section for instructions how to use it in order to run your desired
application.

**Important:** If you already have pipelight installed on your system, there is a
good chance that you already have wine-compholio. Take a look at the next section
on how to find out if this is the case.

If your distribution is not listed below, feel free to add a feature request - if the
demand is high enough we might consider packaging it for additional distributions.


![alt text](http://cdn.fds-team.de/misc/images/ubuntu.png) Ubuntu / Linux Mint
------------------------------------------------------------------------------

Please run the following commands from a terminal, one line after each other.
```bash
sudo add-apt-repository ppa:pipelight/stable
sudo apt-get update
sudo apt-get install --install-recommends wine-compholio
```

![alt text](http://cdn.fds-team.de/misc/images/arch.png) Arch Linux
-------------------------------------------------------------------------

In order to add our repository, you have to add the following lines to your
`/etc/pacman.conf`:
```
[compholio]
Server = http://cdn.fds-team.de/stable/arch/$arch
```

Afterwards you have to import the key for our repository, and set the trust level to
trusted:
```bash
sudo pacman-key -r E49CC0415DC2D5CA
sudo pacman-key --lsign-key E49CC0415DC2D5CA
```

Now you can install wine-compholio directly using `pacman`:
```bash
sudo pacman -Sy wine-compholio
```

![alt text](http://cdn.fds-team.de/misc/images/debian.png) Debian Jessie/Sid
----------------------------------------------------------------------------

*(Instructions for Debian Wheezy can be found below)*

In order to install i386 packages on a 64-bit system, you have to run the following
command as a first step:
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


![alt text](http://cdn.fds-team.de/misc/images/debian.png) Debian Wheezy
------------------------------------------------------------------------

In order to install i386 packages on a 64-bit system, you have to run the following
command as a first step:
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


![alt text](http://cdn.fds-team.de/misc/images/opensuse.png) OpenSUSE
---------------------------------------------------------------------

All the following steps have to be executed as root user. As a first step you have
to add the repository - this step depends on the openSUSE version you're using.

| openSUSE version    | Path component          |
| ------------------- | ----------------------- |
| openSUSE 12.2       | `/openSUSE_12.2/`       |
| openSUSE 12.3       | `/openSUSE_12.3/`       |
| openSUSE 13.1       | `/openSUSE_13.1/`       |
| openSUSE Factory    | `/openSUSE_Factory/`    |
| openSUSE Tumbleweed | `/openSUSE_Tumbleweed/` |

The following commandline is an example for openSUSE 13.1, for a different version
just replace the path component according to the table above:
```bash
zypper ar --refresh http://download.opensuse.org/repositories/home:/DarkPlayer:/Pipelight/openSUSE_13.1/home:DarkPlayer:Pipelight.repo
```

Afterwards just run the following commands to install it:
```bash
zypper ref
zypper install wine-compholio
```


![alt text](http://cdn.fds-team.de/misc/images/fedora.png) Fedora
-----------------------------------------------------------------

**Warning:** In contrary to other distributions, its not possible to have both a
regular wine version and wine-compholio installed at the same time - using the
instructions below will replace your regular version. Moreover it will be installed
to `/usr/bin/wine` in contrary to `/opt/wine-compholio/bin/wine`.

As a first step you have to add the repository - this step depends on the Fedora
version you're using.

| Fedora version  | Patch component |
| --------------- | --------------- |
| Fedora 18       | `/Fedora_18/`   |
| Fedora 19       | `/Fedora_19/`   |
| Fedora 20       | `/Fedora_20/`   |

The following commandline is an example for Fedora 19, for a different version just
replace the path component according to the table above:
```bash
sudo wget http://download.opensuse.org/repositories/home:/DarkPlayer:/Pipelight/Fedora_19/home:DarkPlayer:Pipelight.repo -O /etc/yum.repos.d/pipelight.repo
```

Afterwards run the following command to install the package:
```bash
sudo yum install wine-compholio
```

Please note that you might run into trouble if the official Fedora package (without
compholio patches) is newer than the one from the repository above, so if something
doesn't work, always make sure that you have installed our version. To do that just
run:
```bash
/usr/bin/wine --patches
```
When you're using wine-compholio this will show to a list of all patches included, for
an unpatched version this command will fail.


![alt text](http://cdn.fds-team.de/misc/images/mageia.png) Mageia 4
-------------------------------------------------------------------

As a first step please add the key for our repository
```bash
wget http://repos.fds-team.de/Release.key
rpm --import Release.keyy
```

If you're using a 32-bit version of Mageia just add the repository for 32-bit packages:
```bash
sudo urpmi.addmedia "Compholio 32-bit" http://cdn.fds-team.de/stable/mageia/4/i586/
```

For a 64-bit version of Mageia you'll need both the 32-bit and the 64-bit repository:
```bash
sudo urpmi.addmedia "Compholio 32-bit" http://cdn.fds-team.de/stable/mageia/4/i586/
sudo urpmi.addmedia "Compholio 64-bit" http://cdn.fds-team.de/stable/mageia/4/x86_64/
```

Afterwards run the following commands to install the package:
```bash
sudo urpmi.update -a
sudo urpmi wine-compholio
```


Compiling wine-compholio
========================

**Warning:** Please note that starting with wine-compholio 1.7.23 it is deprecated
to manually apply patches without using the Makefile. To avoid typical pitfalls for
package maintainers (like trying to use the patch commandline utility for binary patches
or not updating the patchlist) it is highly recommended to use the Makefile in order
to apply all patches. This ensures that the the correct patch utility is used, that
the list of patches is updated appropriately, and so on. Please note that it is still
possible to exclude patches if desired, take a look at the end of this document for
more details.

Instructions
------------

The following instructions (based on the
[Gentoo Wiki](https://wiki.gentoo.org/wiki/Netflix/Pipelight#Compiling_manually))
will give a short overview how to compile wine-compholio, but of course not explain
all details. Make sure to install all required Wine dependencies before proceeding.

As the first step please grab the latest Wine source:
```bash
wget http://prdownloads.sourceforge.net/wine/wine-1.7.23.tar.bz2
wget https://github.com/compholio/wine-compholio-daily/archive/v1.7.23.tar.gz
```
Extract the archives:
```bash
tar xvjf wine-1*.tar.bz2
cd wine-1*
tar xvzf ../v1.7.23.tar.gz --strip-components 1
```
And apply the patches:
```bash
make -C ./patches DESTDIR=$(pwd) install
```
Afterwards run configure (you can also specify a prefix if you don't want to install
wine-compholio system-wide):
```bash
./configure --with-xattr
```
Before you continue you should make sure that `./configure` doesn't show any warnings
(look at the end of the output). If there are any warnings, this most likely means
that you're missing some important header files. Install them and repeat the `./configure`
step until all problems are fixed.

Afterwards compile it (and grab a cup of coffee):
```bash
make
```
And install it (you only need sudo for a system-wide installation):
```bash
sudo make install
```

Excluding patches
-----------------

It is also possible to apply only a subset of the patches, for example if you're
compiling for a distribution where PulseAudio is not installed, or if you just don't
like a specific patchset. Please note that some patchsets depend on each other, and
requesting an impossible situation might result in a failure to apply all patches.

Lets assume you want to exclude the patchset in directory `DIRNAME`, then just invoke the
Makefile like this:
```bash
make -C ./patches DESTDIR=$(pwd) install -W DIRNAME.ok
```

Using the same method its also possible to exclude multiple patchsets. If you want to
exclude a very large number of patches, it is easier to do specify a list of patches
which should be included instead. To apply for example only the patchsets in directory
`DIRNAME1` and `DIRNAME2`, you can use:
```bash
make -C ./patches DESTDIR=$(pwd) PATCHLIST="DIRNAME1.ok DIRNAME2.ok" install
```
