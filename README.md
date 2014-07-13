wine-compholio
==============

The Wine "Compholio" Edition repository includes a variety of patches ") for
Wine to run common Windows applications under Linux.

These patches fix the following Wine bugs:

* Support for TransmitFile ([Wine Bug #5048](http://bugs.winehq.org/show_bug.cgi?id=5048 "Multiple applications and games need support for ws2_32 SIO_GET_EXTENSION_FUNCTION_POINTER TransmitFile (WSAID_TRANSMITFILE)"))
* Support for Junction Points ([Wine Bug #12401](http://bugs.winehq.org/show_bug.cgi?id=12401 "Support junction points, i.e. DeviceIoCtl(FSCTL_SET_REPARSE_POINT/FSCTL_GET_REPARSE_POINT)"))
* GetSecurityInfo returns NULL DACL for process object ([Wine Bug #15980](http://bugs.winehq.org/show_bug.cgi?id=15980 "Rhapsody 2 crashes on startup (GetSecurityInfo returns NULL DACL for process object)"))
* Workaround for TransactNamedPipe not being supported ([Wine Bug #17273](http://bugs.winehq.org/show_bug.cgi?id=17273 "Many apps and games need SetNamedPipeHandleState implementation (support for named pipe message mode)(FireFox+Flash, Win8/NET 4.x SDK/vcrun2012, WiX installers)"))
* Support for process ACLs ([Wine Bug #22006](http://bugs.winehq.org/show_bug.cgi?id=22006 "OpenProcess does not enforce ACL"))
* Add implementation of WTSEnumerateProcessesW ([Wine Bug #29903](http://bugs.winehq.org/show_bug.cgi?id=29903 "Some Microsoft debuggers fail to enumerate processes due to wtsapi32.WTSEnumerateProcessesW() being a stub (Microsoft Visual Studio 2005, DbgCLR from .NET 2.0 SDK)"))
* Support for stored file ACLs ([Wine Bug #31858](http://bugs.winehq.org/show_bug.cgi?id=31858 "Netflix on Firefox fails with Internet Connection Problem when loading bar is at 99%"))
* Implement an Arial replacement font ([Wine Bug #32323](http://bugs.winehq.org/show_bug.cgi?id=32323 "Netflix (Silverlight 4.x) and several .NET Framework 3.x/4.0 WPF apps require either Arial or Verdana to be installed"))
* Support for interface change notifications ([Wine Bug #32328](http://bugs.winehq.org/show_bug.cgi?id=32328 "Many .NET and Silverlight applications require SIO_ADDRESS_LIST_CHANGE for interface change notifications"))
* Support for inherited file ACLs ([Wine Bug #34406](http://bugs.winehq.org/show_bug.cgi?id=34406 "Finale Notepad 2012 doesn't copy/create user files on program start"))

Besides that the following additional changes are included:

* Lockfree algorithm for filedescriptor cache (improves file access speed)
* Other Pipelight specific enhancements
* Reduced SetTimer minimum value from 15 ms to 5 ms (improves Silverlight framerates)
* Support for GetVolumePathName
* Support for PulseAudio backend for audio
* Workaround for shlwapi URLs with relative paths
* XEMBED support for embedding Wine windows inside Linux applications

### Compiling wine-compholio

In order to wine-compholio, please use the recommended Makefile based approach which
will automatically decide whether to use 'git apply' or 'gitapply.sh'. The following
instructions (based on the [Gentoo Wiki](https://wiki.gentoo.org/wiki/Netflix/Pipelight#Compiling_manually))
will give a short overview how to compile wine-compholio, but of course not explain
details. Make sure to install all required wine dependencies before proceeding.

As the first step please grab the latest Wine source:
```bash
wget http://prdownloads.sourceforge.net/wine/wine-1.7.22.tar.bz2
wget https://github.com/compholio/wine-compholio-daily/archive/v1.7.22.tar.gz
```
Extract the archives:
```bash
tar xvjf wine-1*.tar.bz2
cd wine-1*
tar xvzf ../v1.7.22.tar.gz --strip-components 1
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
Before you continue you should make sure that ./configure doesn't show any warnings
(look at the end of the output). If there are any warnings, this most likely means
that you're missing some important header files. Install them and repeat the ./configure
step until all problems are fixed.

Afterwards compile it (and grab a cup of coffee):
```bash
make
```
And install it (you only need sudo for a system-wide installation):
```bash
sudo make install
```

### Excluding patches

It is also possible to apply only a subset of the patches, for example if you're compiling
for a distribution where PulseAudio is not installed, or if you just don't like a specific
patchset. Please note that some patchsets depend on each other, and requesting an impossible
situation might result in a failure to apply all patches.

Lets assume you want to exclude the patchset in directory DIRNAME, then just invoke make like that:
```bash
make -C ./patches DESTDIR=$(pwd) install -W DIRNAME.ok
```
