Developers and maintainers guide
================================

This document will provide some information targeted at developers, who
either want to build/package Wine-Compholio for their distribution, but also
for developers who would like to contribute their patches to Wine-Compholio,
to get them included in future releases.



Compiling Wine-Compholio
========================

**Warning:** Please note that starting with Wine-Compholio 1.7.23 it is
deprecated to manually apply patches without using the Makefile. To avoid
typical pitfalls for package maintainers (like trying to use the patch
commandline utility for binary patches or not updating the patchlist) it is
highly recommended to use the Makefile in order to apply all patches. This
ensures that the the correct patch utility is used, that the list of patches
is updated appropriately, and so on. Please note that it is still possible
to exclude patches if desired, take a look at the end of this document for
more details.

Instructions
------------

The following instructions (based on the [Gentoo
Wiki](https://wiki.gentoo.org/wiki/Netflix/Pipelight#Compiling_manually))
will give a short overview how to compile Wine-Compholio, but of course not
explain all details. Make sure to install all required Wine dependencies
before proceeding.

As the first step please grab the latest Wine source:
```bash
wget http://prdownloads.sourceforge.net/wine/wine-1.7.25.tar.bz2
wget https://github.com/compholio/wine-compholio-daily/archive/v1.7.25.tar.gz
```

Extract the archives:
```bash
tar xvjf wine-1*.tar.bz2
cd wine-1*
tar xvzf ../v1.7.25.tar.gz --strip-components 1
```

And apply the patches:
```bash
make -C ./patches DESTDIR=$(pwd) install
```

Afterwards run configure (you can also specify a prefix if you don't want to install
Wine-Compholio system-wide):
```bash
./configure --with-xattr
```

Before you continue you should make sure that `./configure` doesn't show any
warnings (look at the end of the output). If there are any warnings, this
most likely means that you're missing some important header files. Install
them and repeat the `./configure` step until all problems are fixed.

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

It is also possible to apply only a subset of the patches, for example if
you're compiling for a distribution where PulseAudio is not installed, or
if you just don't like a specific patchset. Please note that some patchsets
depend on each other, and requesting an impossible situation might result
in a failure to apply all patches.

Lets assume you want to exclude the patchset in directory `DIRNAME`, then
just invoke the Makefile like this:
```bash
make -C ./patches DESTDIR=$(pwd) install -W DIRNAME.ok
```

Using the same method its also possible to exclude multiple patchsets. If you
want to exclude a very large number of patches, it is easier to do specify
a list of patches which should be included instead. To apply for example
only the patchsets in directory `DIRNAME1` and `DIRNAME2`, you can use:
```bash
make -C ./patches DESTDIR=$(pwd) PATCHLIST="DIRNAME1.ok DIRNAME2.ok" install
```


Contributing to Wine-Compholio
==============================

Please note that Wine-Compholio is not just an arbitrary collection of Wine
patches. We see Wine-Compholio as a **testing version** in preparation for
patches to be submitted to upstream Wine. This implies that all patches should
at least have a minimum standard quality. Unlike some other PPAs/AURs which
provide heavily patched Wine versions, we will not accept hacks for very
specific games. Such hacks often break compatibility with other applications,
which means we probably don't want to include them, sorry.

If you think your patches are indeed a proper implementation, then feel free
to contribute them.  Please note that to allow possible later inclusion
into upstream Wine, we will require you to pay attention to the same
[rules](http://wiki.winehq.org/SubmittingPatches). Please be patient and
give us up to about a week to review them - we're a very small team, so
it might take some time, and we want to make sure that the implementation
doesn't contain any critical errors, which could cause regressions. If you
want to contribute huge sets of patches, we would really like you to *stay
contributing* in the future. Even if we accepted your patches, this doesn't
necessary mean we understand all of it, and if you cannot or don't want
to maintain them (especially in case of errors, or difficult rebasing),
we will probably end up removing them again.

You can also suggest adding patches written by other people - in this case
your request should include who wrote the patch. Anonymous patches which
don't include the author information aren't welcome, similar to the rules
for upstream Wine.


Attribution guidelines
----------------------

The Wine "Compholio" Edition repository expects all patches to conform to
Wine's (undocumented) attribution guidelines. There are a variety of ways
to attribute patches, but they all involve an additional line to the patch
subject:

```
commit 0000000000000000000000000000000000000000
Author: Example Author <example.email@email-provider.com>
Date:   Sat Jul 26 12:31:50 2014 -0600

    Name of patch.
    
    TYPE-OF-ATTRIBUTION.
```

TYPE-OF-ATTRIBUTION can be any of the following:

`Found/Spotted by FINDER.`: The resolved issue was found by FINDER, they
should receive appropriate credit for finding the problem - even though
their patch was not used in the final implementation.

`Based on patch by AUTHOR.`: The patch created by AUTHOR was a starting point
for the patch, some modifications were made to their patch - but they should
receive credit since the original implementation was theirs.