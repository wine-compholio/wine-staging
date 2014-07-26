Patch attribution for wine-compholio
==============

The Wine "Compholio" Edition repository expects all patches to conform to Wine's attribution guidelines.  There are a variety of ways to attribute patches, but they all involve an additional line to the patch subject:

    commit 0000000000000000000000000000000000000000
    Author: Example Author <example.email@email-provider.com>
    Date:   Sat Jul 26 12:31:50 2014 -0600
    
        Name of patch.
        
        TYPE-OF-ATTRIBUTION.

TYPE-OF-ATTRIBUTION can be any of the following:

Found/Spotted by FINDER:
The resolved issue was found by FINDER, they should receive appropriate credit for finding the problem - even though their patch was not used in the final implementation.

Based on patch by AUTHOR:
The patch created by AUTHOR was a starting point for the patch, some modifications were made to their patch - but they should receive credit since the original implementation was theirs.
