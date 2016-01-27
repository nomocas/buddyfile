import sublime, sublime_plugin, os.path, re

def show_label(view, position):
	if not view.is_loading():
		occurence = view.find(position, 0)
		if occurence:
			view.show_at_center(occurence)
	else:
		sublime.set_timeout(lambda: show_label(view, position), 10)

def get_buddy_path(fullPath):
	fileFolder = os.path.dirname(fullPath)
	fline = open(fullPath, encoding='utf-8').readline().rstrip()
	matched = re.search('--buddyfile:\s*([^\s@]+)\s*(@.+)?\s*', fline);
	if matched:
		buddyPath = os.path.normpath(os.path.join(fileFolder, matched.group(1)))
		position = matched.group(2)
		if position: # remove @
			position = '--buddylabel: '+position[1:]
		if os.path.exists(buddyPath):
			return (buddyPath, position)
	return (None, None)

def show_buddy(view, focusOnBuddy=0):
	buddyPath, position = get_buddy_path(view.file_name())
	if buddyPath:
		window = view.window()
		cells = window.get_layout()['cells']
		nbrCells = len(cells)
		if nbrCells == 1: # create 2 cells
			window.set_layout({
				"cols": [0.0, 1.0],
				"rows": [0.0, 0.5, 1.0],
				"cells": [[0, 0, 1, 1], [0, 1, 1, 2]]
			})

		if window.active_group() != 0: # place master file in first cell
			window.set_view_index(view, 0, 0)

		buddyView = window.find_open_file(buddyPath)
		if not buddyView:
			buddyView = window.open_file(buddyPath)

		# place buddy file in second cell
		window.set_view_index(buddyView, 1, 0)
		window.focus_view(buddyView) # force focus for preventing bug with mouse click
		if position:
			show_label(buddyView, position)
		if not focusOnBuddy:
			window.focus_view(view)



def close_buddy(masterPath):
	buddyPath, position = get_buddy_path(masterPath)
	if buddyPath:
		window = sublime.active_window()
		buddyView = window.find_open_file(buddyPath)
		if buddyView:
			buddyView.close()
			views = window.views_in_group(1);
			if len(views) == 0: # remove the second cell
				window.set_layout({
					"cols": [0.0, 1.0],
					"rows": [0.0,  1.0],
					"cells": [[0, 0, 1, 1]]
				})
			else:
				window.focus_group(0);

class BuddyfileListener(sublime_plugin.EventListener):
	def __init__(self):
		self._settings = sublime.load_settings('buddyfile.sublime-settings')

	def on_load_async(self, view):
		if self._settings.get('check_buddy_on_load'):
			show_buddy(view)

	def on_close(self, view):
		if self._settings.get('close_buddy_on_close'):
			fullPath = view.file_name()
			if fullPath:
				close_buddy(fullPath)

class CheckBuddyfileCommand(sublime_plugin.WindowCommand):
	
	def run(self):
		show_buddy(self.window.active_view())

class JumpToBuddyfileCommand(sublime_plugin.WindowCommand):
	
	def run(self):
		show_buddy(self.window.active_view(), 1)	

class CloseBuddyfileCommand(sublime_plugin.WindowCommand):
	
	def run(self):
		fullPath = self.window.active_view().file_name()
		if fullPath:
			close_buddy(fullPath)
