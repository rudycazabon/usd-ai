from pxr import Tf
from pxr.Usdviewq.plugin import PluginContainer


class TutorialPluginContainer(PluginContainer):

    def registerPlugins(self, plugRegistry, usdviewApi):

        sendMail = self.deferredImport(".sendMail")
        self._sendMail = plugRegistry.registerCommandPlugin(
            "TutorialPluginContainer.sendMail",
            "sendMail Message",
            sendMail.SendMail)

    def configureView(self, plugRegistry, plugUIBuilder):

        tutMenu = plugUIBuilder.findOrCreateMenu("Tutorial")
        tutMenu.addItem(self._sendMail)

Tf.Type.Define(TutorialPluginContainer)