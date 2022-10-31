import addonHandler
addonHandler.initTranslation()
import wx
import os
from . import data
from .import g
datapath = os.path.abspath(os.path.dirname(data.__file__))
import json
import api
from ui import message

class AddDialog(wx.Dialog):
	def __init__(self, parent):
#translaters: this is the title of the add new link dialog
		title = _("add new link")
		super().__init__(parent, -1, title=title)
		p = wx.Panel(self)
		wx.StaticText(p, -1, _("the link name"))
		self.linkName = wx.TextCtrl(p, -1)
		wx.StaticText(p, -1, _("the link"))
		self.link = wx.TextCtrl(p, -1)
		wx.StaticText(p, -1, _("category"))
		self.category = wx.Choice(p, -1)
		newCategory = wx.Button(p, -1, _("create new category"))
		add = wx.Button(p, -1, _("add"))
		cancel = wx.Button(p, wx.ID_CANCEL, _("cancel"))
		add.SetDefault()
		add.Bind(wx.EVT_BUTTON, self.OnAdd)
		newCategory.Bind(wx.EVT_BUTTON, self.OnNewCategory)
		try:
			if g.GetUrl(api.getClipData()):
				self.link.Value = g.GetUrl(api.getClipData())[0]
		except: pass
		self.LoadCategorys()
		wx.CallAfter(self.Show)

	def LoadCategorys(self):
		self.category.Clear()
		if os.path.exists(os.path.join(datapath, "data.json")):
			with open(os.path.join(datapath, "data.json")) as f:
				data = json.loads(f.read())
			for category in data:
				self.category.Append(category)
			self.category.Selection = 0
		else:
			data = {}
			with open(os.path.join(datapath, "data.json"), "w") as f:
				f.write(json.dumps(data, indent=4))

	def OnNewCategory(self, event):
		cate = wx.GetTextFromUser(_("enter the new category name"), _("category name"))
		if not cate: return
		if os.path.exists(os.path.join(datapath, "data.json")):
			with open(os.path.join(datapath, "data.json")) as f:
				data = json.loads(f.read())
		else:
			data = {}
		if cate in data:
			return wx.MessageBox(_("this category already exists"), _("category exists"), parent=self)
		else:
			data[cate] = []
		data = json.dumps(data, indent=4)
		with open(os.path.join(datapath, "data.json"), "w") as f:
			f.write(data)
		wx.MessageBox(_("category added successfully"), _("success"), parent=self)
		g.gp.load()
		self.LoadCategorys()

	def OnAdd(self, event):
		if not self.category.StringSelection:
			return wx.MessageBox(_("you must add at least one category to add new link"), _("error"), parent=self, style=wx.ICON_ERROR)
		if os.path.exists(os.path.join(datapath, "data.json")):
			with open(os.path.join(datapath, "data.json")) as f:
				data = json.loads(f.read())
		else:
			data = {}
		if not self.linkName.Value: return self.linkName.SetFocus()
		if not self.link.Value: return self.link.SetFocus()
		if not g.GetUrl(self.link.Value):
			return self.link.SetFocus()
		if self.category.StringSelection in data:
			data[self.category.StringSelection].append([self.linkName.Value, g.GetUrl(self.link.Value)[0]])
		else:
			data[self.category.StringSelection] = [[self.linkName.Value, g.GetUrl(self.link.Value)[0]]]
		data = json.dumps(data, indent=4)
		with open(os.path.join(datapath, "data.json"), "w") as f:
			f.write(data)
		g.gp.load()
		wx.MessageBox(_("link added successfully"), _("success"), parent=self)