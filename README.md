wine-compholio-daily
====================

Daily updates for the Wine "Compholio" Edition.

Current patches include:
* Support for interface change notifications (http://bugs.winehq.org/show_bug.cgi?id=32328)
* Support for stored file ACLs (http://bugs.winehq.org/show_bug.cgi?id=31858)
* Support for inherited file ACLs (http://bugs.winehq.org/show_bug.cgi?id=34406)
* Support for Junction Points (http://bugs.winehq.org/show_bug.cgi?id=12401)
* Support for TransmitFile (http://bugs.winehq.org/show_bug.cgi?id=5048)
* Support for GetVolumePathName
* Implement an Arial replacement font (http://bugs.winehq.org/show_bug.cgi?id=32323)
* Workaround for TransactNamedPipe not being supported (http://bugs.winehq.org/show_bug.cgi?id=17273)
* Avoid unloading modules while hook is still active (http://bugs.winehq.org/show_bug.cgi?id=22091)
* XEMBED support for embedding Wine windows inside Linux applications
* Reduced SetTimer minimum value from 15 ms to 5 ms (improves Silverlight framerates)
* Lockfree algorithm for filedescriptor cache (improves file access speed)
* Workaround for shlwapi URLs with relative paths
* Support for PulseAudio backend for audio
* Other Pipelight specific enhancements
