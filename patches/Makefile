#
# This file is deprecated and will be deleted in the future.
# Please use patchinstall.sh instead, to apply the Wine Staging patches.
#

CURDIR ?= ${.CURDIR}

.PHONY: install
install:
	@echo "WARNING: Using this Makefile is deprecated!" >&2
	"$(CURDIR)/patchinstall.sh" DESTDIR="$(DESTDIR)" --all

.PHONY: install-git
install-git:
	@echo "WARNING: Using this Makefile is deprecated!" >&2
	"$(CURDIR)/patchinstall.sh" DESTDIR="$(DESTDIR)" --all --backend=git-am

.PHONY: series
series:
	@echo "ERROR: Using this Makefile is deprecated!" >&2
	@false
