import addonHandler
addonHandler.initTranslation()
import api
import wx
import webbrowser as wb
from . import g
from ui import message, reportTextCopiedToClipboard

class FromClipboard(wx.Dialog):
	def __init__(self, parent):
		try:
			clip = api.getClipData()
			if len(g.GetUrl(clip))<1: raise OSError("there is no links")
		except OSError:
			return message(_("It appears that the clipboard is empty or there is no link in it."))
		if len(g.GetUrl(clip))==1:
			message(_("opening {url}").format(url=g.GetUrl(clip)[0]))
			return wb.open(g.GetUrl(clip)[0])
		super().__init__(parent, -1, _("choos a link to open"))
		p = wx.Panel(self)
		wx.StaticText(p, -1, _("{count} links found").format(count=len(g.GetUrl(clip))))
		self.linksList = wx.ListBox(p, -1)
		openUrl = wx.Button(p, -1, _("open"))
		openUrl.SetDefault()
		openUrl.Bind(wx.EVT_BUTTON, self.OnOpen)
		copy = wx.Button(p, -1, _("copy to clipboard"))
		copy.Bind(wx.EVT_BUTTON, self.OnCopy)
		close = wx.Button(p, wx.ID_CANCEL, _("close"))
		for link in g.GetUrl(clip):
			self.linksList.Append(link)
		self.linksList.Selection = 0
		wx.CallAfter(self.Show)

	def OnOpen(self, event):
		message(_("opening {url}").format(url=self.linksList.StringSelection))
		wb.open(self.linksList.StringSelection)

	def OnCopy(self, event):
		if api.copyToClip(self.linksList.StringSelection):
			reportTextCopiedToClipboard(self.linksList.StringSelection)