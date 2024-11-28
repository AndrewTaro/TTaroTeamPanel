try:
    import events, ui, utils, dataHub, constants
except:
    pass


CC = constants.UiComponents


class EntityController(object):
    """
    Controll datahub entity
    """
    def __init__(self, componentKey):
        self._entityId = None
        self._componentKey = componentKey

    def createEntity(self, data=None):
        """
        Create DH entity
        """
        if self._entityId is not None:
            self.removeEntity()
        self._entityId = ui.createUiElement()
        ui.addDataComponentWithId(self._entityId, self._componentKey, data)

    def removeEntity(self):
        """
        Remove DH entity
        """
        try:
            if self._entityId is not None:
                ui.deleteUiElement(self._entityId)
            self._entityId = None
        except:
            pass

    def updateEntity(self, data):
        """
        Update datahub
        """
        ui.updateUiElementData(self._entityId, dict(data))