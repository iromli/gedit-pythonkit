GEDIT_PLUGIN_DIR = ~/.local/share/gedit/plugins

install:
	@if [ ! -d $(GEDIT_PLUGIN_DIR) ]; then \
		mkdir -p $(GEDIT_PLUGIN_DIR);\
	fi
	@echo "installing pythonkit plugin";
	@rm -rf $(GEDIT_PLUGIN_DIR)/pythonkit*;
	@cp -R pythonkit* $(GEDIT_PLUGIN_DIR);

uninstall:
	@echo "uninstalling pythonkit plugin";
	@rm -rf $(GEDIT_PLUGIN_DIR)/pythonkit*;
