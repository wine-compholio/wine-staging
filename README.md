wine-compholio
==============

The Wine "Compholio" Edition repository includes a variety of patches for Wine to run common Windows applications under Linux.

Current patches include:

* Support for interface change notifications ([Wine Bug #32328](http://bugs.winehq.org/show_bug.cgi?id=32328))
* Support for stored file ACLs ([Wine Bug #31858](http://bugs.winehq.org/show_bug.cgi?id=31858))
* Support for inherited file ACLs ([Wine Bug #34406](http://bugs.winehq.org/show_bug.cgi?id=34406))
* Support for Junction Points ([Wine Bug #12401](http://bugs.winehq.org/show_bug.cgi?id=12401))
* Support for TransmitFile ([Wine Bug #5048](http://bugs.winehq.org/show_bug.cgi?id=5048))
* Support for GetVolumePathName
* Implement an Arial replacement font ([Wine Bug #32323](http://bugs.winehq.org/show_bug.cgi?id=32323))
* Workaround for TransactNamedPipe not being supported ([Wine Bug #17273](http://bugs.winehq.org/show_bug.cgi?id=17273))
* Fix incorrect scaling for DECIMAL values in VarDecAdd ([Wine Bug #31269](http://bugs.winehq.org/show_bug.cgi?id=31269))
* Return NULL-terminated list of arguments in CommandLineToArgvW ([Wine Bug #22829](http://bugs.winehq.org/show_bug.cgi?id=22829))
* XEMBED support for embedding Wine windows inside Linux applications
* Reduced SetTimer minimum value from 15 ms to 5 ms (improves Silverlight framerates)
* Lockfree algorithm for filedescriptor cache (improves file access speed)
* Workaround for shlwapi URLs with relative paths
* Support for PulseAudio backend for audio
* Other Pipelight specific enhancements
