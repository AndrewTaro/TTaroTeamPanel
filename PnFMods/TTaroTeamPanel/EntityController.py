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


class EntityControllersCollection(object):
    def __init__(self, componentKeyBase):
        """
        Each entity will have `indexKeyBase + '_' + key`
        """
        self.__componentKeyBase = componentKeyBase
        self.__controllers = {}
        pass

    def addController(self, key, data=None):
        key = self.__createKey(key)
        if key in self.__controllers:
            utils.logError('[EntityControllersCollection] Failed to add controller. Key already exists: {}'.format(key))
            return
        controller = EntityController(key)
        controller.createEntity(data)
        self.__controllers[key] = controller

    def removeController(self, key):
        key = self.__createKey(key)
        if key not in self.__controllers:
            utils.logError('[EntityControllersCollection] Failed to remove controller. Key does not exist: {}'.format(key))
            return
        controller = self.__controllers.pop(key)
        controller.removeEntity()

    def updateController(self, key, data):
        key = self.__createKey(key)
        if key in self.__controllers:
            utils.logError('[EntityControllersCollection] Failed to update controller. Key does not exist: {}'.format(key))
            return
        self.__controllers[key].updateEntity(data)

    def removeAll(self):
        for key in self.__controllers.keys():
            controller = self.__controllers.pop(key)
            controller.removeEntity()

    def __createKey(self, key):
        return '{}_{}'.format(self.__componentKeyBase, key)