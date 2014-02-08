install:
	# Apply our patches to Wine
	for DIR in $$(find $(CURDIR) -type d | sort); do \
		for FILE in $$(ls $$DIR | sort | grep '\.patch$$'); do \
			SHORTNAME=$$(echo "$$DIR/$$FILE" | sed 's|$(CURDIR)|\.|g' ); \
			printf "Applying patch '$$SHORTNAME'...\n"; \
			patch -d $(DESTDIR) -N -p0 --strip=1 < $$DIR/$$FILE || cat || exit 1; \
		done \
	done

	# Update the configure script
	cd $(DESTDIR); autoreconf;

	# Update the wineserver protocol request data
	cd $(DESTDIR); ./tools/make_requests;

uninstall:
	# Remove our patches from Wine
	for DIR in $$(find $(CURDIR) -type d | sort -r); do \
		for FILE in $$(ls $$DIR | sort -r | grep '\.patch$$'); do \
			SHORTNAME=$$(echo "$$DIR/$$FILE" | sed 's|$(CURDIR)|\.|g' ); \
			printf "Reversing patch '$$SHORTNAME'...\n"; \
			patch -d $(DESTDIR) -R -N -p0 --strip=1 < $$DIR/$$FILE || exit 1; \
		done \
	done

	# Update the configure script
	cd $(DESTDIR); autoreconf;

	# Update the wineserver protocol request data
	cd $(DESTDIR); ./tools/make_requests;

