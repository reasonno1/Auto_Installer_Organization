import os

plugin_list_path = "D:\\CanPy\\Auto_Installer\\Extra_iC7\\iC_plugin_list.txt"
plugin_list = []

file = open(plugin_list_path)
for line in file:
    line = line.replace("\n", "")
    plugin_list.append(line)



for p in plugin_list:
    print p