PYTHONKIT_DIR = $(dir $(CURDIR)/$(lastword $(MAKEFILE_LIST)))
GEDIT_PLUGIN_DIR = ~/.gnome2/gedit/plugins

install:
	@if [ ! -d $(GEDIT_PLUGIN_DIR) ]; then \
		mkdir -p $(GEDIT_PLUGIN_DIR);\
	fi
	@echo "installing pythonkit plugin";
	@cp -R $(PYTHONKIT_DIR)/plugin/pythonkit* $(GEDIT_PLUGIN_DIR);
	@rm -rf $(GEDIT_PLUGIN_DIR)/pythonkit/*.py[co];

uninstall:
	@echo "uninstalling pythonkit plugin";
	@rm -rf $(GEDIT_PLUGIN_DIR)/pythonkit*;

symlink:
	@echo "symlinking pythonkit plugin";
	@rm -rf $(GEDIT_PLUGIN_DIR)/pythonkit*;
	@ln -s $(PYTHONKIT_DIR)/plugin/pythonkit $(GEDIT_PLUGIN_DIR)/pythonkit;
	@ln -s $(PYTHONKIT_DIR)/plugin/pythonkit.gedit-plugin $(GEDIT_PLUGIN_DIR)/pythonkit.gedit-plugin;
