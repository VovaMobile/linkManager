import sys
import globalPluginHandler
import ui
import gui
import wx
import json
import os
import addonHandler
addonHandler.initTranslation()
import config
import webbrowser as wb
from scriptHandler import script
from tones import beep
from .import g
from .import add_dialog
from . import data
from . import search_dialog
from . import from_clipboard

datapath = os.path.abspath(os.path.dirname(data.__file__))


g.ConfigInit()

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self, *args, **kwargs):
		super(GlobalPlugin, self).__init__(*args, **kwargs)
		self.linksList = {}
		self.index = 0
		self.category = 0
		self.categoryLength = 0
		g.gp=self
		self.load()

	def load(self):
		if self.linksList:
			self.linksList = {}
		self.categoryLength = 0
		if not os.path.exists(os.path.join(datapath, "data.json")): return
		with open(os.path.join(datapath, "data.json"),) as f:
			data = json.loads(f.read())
		if data:
			for category in data:
				self.linksList[self.categoryLength] = [category, data[category]]
				self.categoryLength +=1

	@script(
		description=_("moves to next URL"),
		category="link_manager",
		gesture="kb:control+shift+f12"
	)
	def script_next(self, gesture):
		try:
			self.linksList[self.category][1]
		except KeyError:
			return beep(200, 100)
		if self.index<len(self.linksList[self.category][1])-1:
			self.index+=1
		else:
			beep(250, 50)
		msg = f"{self.linksList[self.category][1][self.index][0]}"
		if g.get("read_urls"):
			msg = msg+" "+self.linksList[self.category][1][self.index][1]
		ui.message(msg)
#		ui.message(f"{self.linksList}")

	@script(
		description=_("moves to previous URL"),
		category="link_manager",
		gesture="kb:control+shift+f11"
	)
	def script_previous(self, gesture):
		try:
			self.linksList[self.category][1]
		except KeyError:
			return beep(200, 100)
		if self.index>0:
			self.index-=1
		else:
			beep(200, 50)
		msg = f"{self.linksList[self.category][1][self.index][0]}"
		if g.get("read_urls"):
			msg = msg+" "+self.linksList[self.category][1][self.index][1]
		ui.message(msg)

	@script(
		description=_("moves to next category"),
		category="link_manager",
		gesture="kb:control+shift+f10"
	)
	def script_NextCategory(self, gesture):
		if not self.linksList:
			return beep(200, 100)
		if self.category<len(self.linksList)-1:
			self.category+=1
		else:
			beep(250, 50)
		self.index = len(self.linksList[self.category][1])-1
		if len(self.linksList[self.category][1])>1:
			lnk = _("links")
		else:
			lnk = _("link")
		msg = _("{category}: Contains {length} {l}").format(category=self.linksList[self.category][0], length=len(self.linksList[self.category][1]), l=lnk)
		ui.message(msg)

	@script(
		description=_("moves to previous category"),
		category="link_manager",
		gesture="kb:control+shift+f9"
	)
	def script_PreviousCategory(self, gesture):
		if not self.linksList:
			return beep(200, 100)
		if self.category>0:
			self.category-=1
		else:
			beep(250, 50)
		msg = f"{self.linksList[self.category][0]}"
		self.index = len(self.linksList[self.category][1])-1
		if len(self.linksList[self.category][1])>1:
			lnk = _("links")
		else:
			lnk = _("link")
		msg = _("{category}: Contains {length} {l}").format(category=self.linksList[self.category][0], length=len(self.linksList[self.category][1]), l=lnk)
		ui.message(msg)

	@script(
		description=_("add a new URL"),
		category="link_manager",
		gesture="kb:NVDA+shift+a"
	)
	def script_AddNew(self, gesture):
		wx.CallAfter(
			add_dialog.AddDialog,
			gui.mainFrame
		)

	@script(
		description=_("open any link from clipboard"),
		category="link_manager",
		gesture="kb:NVDA+z"
	)
	def script_FromClip(self, gesture):
		wx.CallAfter(
			from_clipboard.FromClipboard,
			gui.mainFrame
		)

	@script(
		description=_("search for a URL in the category"),
		category="link_manager",
		gesture="kb:NVDA+shift+g"
	)
	def script_search(self, gesture):
		wx.CallAfter(
			search_dialog.search,
			gui.mainFrame
		)

	@script(
		description=_("Toggle displaying of URL after name."),
		category="link_manager",
		gesture="kb:control+shift+l"
	)
	def script_ReadUrls(self, gesture):
		if g.get("read_urls"):
			ui.message(_("read URL after name turned off"))
		else:
			ui.message(_("read URL after name turned on"))
		g.set("read_urls", not g.get("read_urls"))

	@script(
	description=_("open the current selected URL"),
	category="link_manager",
	gesture="kb:control+shift+enter"
)
	def script_OpenUrl(self, gesture):
		wb.open(self.linksList[self.category][1][self.index][1])
		ui.message(_("opening {url}").format(url=self.linksList[self.category][1][self.index][1]))

	@script(
		description=_("remove a URL from category"),
		category="link_manager",
		gesture="kb:nvda+shift+control+delete"
	)
	def script_delete(self, gesture):
		if not self.linksList: return
		msg = _("Are you shore you want to delete {url} from the category?").format(url=self.linksList[self.category][1][self.index][1])
		wx.CallAfter(
			self.delete,
			msg=msg,
			title=_("delete"),
			style=wx.YES_NO,
			parent=gui.mainFrame
		)

	def delete(self, msg, title, style, parent):
		ask = wx.MessageBox(msg, title, style=style, parent=parent)
		if ask == wx.YES:
			with open(os.path.join(datapath, "data.json")) as f:
				data = json.loads(f.read())
			data[self.linksList[self.category][0]].pop(self.index)
			with open(os.path.join(datapath, "data.json"), "w") as f:
				f.write(json.dumps(data, indent=4))
		if self.index>=len(self.linksList[self.category][1])-1:
			self.index = len(self.linksList[self.category][1])-2
		else:
			self.index+=1
		self.load()

	@script(
		description=_("Delete a category from the category list"),
		category="link_manager",
		gesture="kb:nvda+shift+r"
	)
	def script_DeleteCategory(self, gesture):
		if not self.linksList: return
		msg = _("are you shore that you want to delete {category} from the category list?").format(category=self.linksList[self.category][0])
		wx.CallAfter(
			self.DeleteCategory,
			msg=msg,
			title=_("delete"),
			style=wx.YES_NO,
			parent=gui.mainFrame
		)

	def DeleteCategory(self, msg, title, style, parent):
		ask = wx.MessageBox(msg, title, style=style, parent=parent)
		if ask == wx.YES:
			with open(os.path.join(datapath, "data.json")) as f:
				data = json.loads(f.read())
			del data[self.linksList[self.category][0]]
			with open(os.path.join(datapath, "data.json"), "w") as f:
				f.write(json.dumps(data, indent=4))
		if self.category>=len(self.linksList)-1:
			self.category = len(self.linksList)-2
		else:
			self.category+=1
		self.load()
		self.index = len(self.linksList[self.category][1][self.index])-1

	@script(
		description=_("moves to first link in the category"),
		category="link_manager",
		gesture="kb:nvda+shift+control+f11"
	)
	def script_first(self, gesture):
		self.index = 0
		msg = f"{self.linksList[self.category][1][self.index][0]}"
		if g.get("read_urls"):
			msg = msg+" "+self.linksList[self.category][1][self.index][1]
		ui.message(msg)

	@script(
		description=_("moves to last link in the category"),
		category="link_manager",
		gesture="kb:nvda+shift+control+f12"
	)
	def script_last(self, gesture):
		self.index = len(self.linksList[self.category][1])-1
		msg = f"{self.linksList[self.category][1][self.index][0]}"
		if g.get("read_urls"):
			msg = msg+" "+self.linksList[self.category][1][self.index][1]
		ui.message(msg)
