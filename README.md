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
