import addonHandler
addonHandler.initTranslation()
import api
import wx
import webbrowser as wb
import os
from . import data
from .import g
datapath = os.path.abspath(os.path.dirname(data.__file__))
import json
from ui import message, reportTextCopiedToClipboard
from tones import beep

class search(wx.Dialog):
	def __init__(self, parent):
		if not os.path.exists(os.path.join(datapath, "data.json")):
			return wx.MessageBox(_("there is no category or data file to search"), _("error"), parent=parent, style=wx.ICON_ERROR)
		with open(os.path.join(datapath, "data.json")) as f:
			self.data = json.loads(f.read())
		if not data:
			return wx.MessageBox(_("there is no category or data file to search"), _("error"), parent=parent, style=wx.ICON_ERROR)
		title = _("search")
		super().__init__(parent, -1, title=title)
		self.p = wx.Panel(self)
		self.rl = wx.StaticText(self.p, -1, name="r")
		self.results = wx.ListBox(self.p, -1, name="r")
		wx.StaticText(self.p, -1, _("search word"))
		self.searchWord = wx.TextCtrl(self.p, -1)
		wx.StaticText(self.p, -1, _("category"))
		self.category = wx.Choice(self.p, -1)
		self.by = wx.RadioBox(self.p, -1, _("search by"), choices=[_("name"), _("link")])
		go = wx.Button(self.p, -1, _("search"))
		go.SetDefault()
		go.Bind(wx.EVT_BUTTON, self.OnGo)
		self.results.Bind(wx.EVT_KEY_DOWN, self.OnLink)
		cancel = wx.Button(self.p, wx.ID_CANCEL, _("cancel"))
		for i in self.p.GetChildren():
			if i.Name=="r": i.Hide()
		for i in self.data:
			self.category.Append(i)
		self.category.Selection = 0
		wx.CallAfter(self.Show)

	def OnGo(self, event):
		if self.FindFocus() == self.results:
			message(_("opening {url}").format(url=self.results.StringSelection.split(" : ")[1]))
			wb.open(self.results.StringSelection.split(" : ")[1])
			return
		if not self.searchWord.Value: return message(_("write search word"))
		if self.results.Strings: self.results.Clear()
		data = self.data[self.category.StringSelection]
		for result in data:
			where = result[0] if self.by.Selection ==0 else result[1]
			if self.searchWord.Value in where:
				self.results.Append(f"{result[0]} : {result[1]}")
		if self.results.IsEmpty():
			return wx.MessageBox(_("no results found"), _("there are no results"))
		for i in self.p.GetChildren():
			if i.Name=="r": i.Show()
		self.rl.Label = _("results list: {count} results found").format(count=self.results.Count)
		self.results.Selection = 0 
		self.results.SetFocus()

	def OnLink(self, event):
		key = event.GetKeyCode()
		if event.controlDown and key == ord("C"):
			if api.copyToClip(self.results.StringSelection.split(" : ")[1]):
				reportTextCopiedToClipboard(self.results.StringSelection.split(" : ")[1])
				beep(1000, 20)
		event.Skip()