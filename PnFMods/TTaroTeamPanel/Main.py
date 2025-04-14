API_VERSION = 'API_v1.0'
MOD_NAME = 'TTaroTeamPanel'

"""
{
    'maxShips': X,
    'minShips': Y,
    'maxRepeatingShips': Z,
    'classes': {
        'AirCarrier': (0, -1),
        'Battleship': (0, -1),
        'Cruiser': (0, -1),
        'Destroyer': (0, 6),
        'Submarine': (0, -1),
    },
    'limitedShips': [
        {
            'ships': ['PJSB018_Yamato_1944', 'PJSB918_Yamato_1944', 'PJSB700_ARP_Yamato'],
            'limit': 1,
        },
        {
            'ships': ['PJSD518_Asashio'],
            'limit': 2,
        }
    ],
    'combinedClasses': {
        'min': 1,
        'max': 4,
        'classes': ['AirCarrier', 'Battleship']
    },
    'filters': {
        'excludedShips': (someBadDestroyer,),
        'classes': ('Battleship', 'Cruiser', 'Destroyer'),
        'tiers': (6, 7,),
    }
}
"""

try:
    import events, ui, utils, dataHub, constants
except:
    pass

from EntityController import EntityController


CC = constants.UiComponents
ShipTypes = constants.ShipTypes
PLAYABLE_SHIP_TYPES = (ShipTypes.AIRCARRIER, ShipTypes.BATTLESHIP, ShipTypes.CRUISER, ShipTypes.DESTROYER, ShipTypes.SUBMARINE)

RES_MODS_FOLDER = utils.getModDir() + '/../../'
SHIP_RESTRICTION_FILE = RES_MODS_FOLDER + 'ship_restrictions.json'


class ShipRestriction(object):
    RESTRICTION_DATA = None

    @classmethod
    def init(cls):
        cls.__loadRestrictions()

    @classmethod
    def validateShipsCount(cls, avatars):
        """
        Return set of invalid ships
        """
        maxShips = cls.RESTRICTION_DATA.get('maxShips', -1)
        minShips = cls.RESTRICTION_DATA.get('minShips', 0)
        maxShips = cls.__convertInfinite(maxShips)
        if not (minShips <= len(avatars) <= maxShips):
            return set(avatar.ship.ref.ship.fullName for avatar in avatars)
        return set()
    
    @classmethod
    def validateMaxRepeatingShips(cls, avatars):
        """
        Return set of invalid ships
        """
        counter = {}
        maxRepeatingShips = cls.RESTRICTION_DATA.get('maxRepeatingShips', -1)
        maxRepeatingShips = cls.__convertInfinite(maxRepeatingShips)

        for avatar in avatars:
            shipName = avatar.ship.ref.ship.fullName
            counter.setdefault(shipName, 0)
            counter[shipName] += 1
        return set(sName for sName, count in counter.iteritems() if count > maxRepeatingShips)
    
    @classmethod
    def validateClasses(cls, avatars):
        """
        Return set of invalid ships
        """
        classLimits = cls.RESTRICTION_DATA.get('classes', {})
        shipTypes = [avatar.shipType for avatar in avatars]
        invalidShips = set()

        for shipType in PLAYABLE_SHIP_TYPES:
            classLimit = classLimits.get(shipType, (0, -1))
            minShips = classLimit[0]
            maxShips = cls.__convertInfinite(classLimit[1])
            if not minShips <= shipTypes.count(shipType) <= maxShips:
                invalidShips |= set(avatar.ship.ref.ship.fullName for avatar in avatars if shipType == avatar.shipType)
        return invalidShips
    
    @classmethod
    def validateLimitedShips(cls, avatars):
        """
        Return set of invalid ships
        """
        shipLimits = cls.RESTRICTION_DATA.get('limitedShips', [])

        counter = {}
        for avatar in avatars:
            shipName = avatar.ship.ref.ship.fullName
            counter.setdefault(shipName, 0)
            counter[shipName] += 1

        invalidShips = set()
        for shipLimit in shipLimits:
            limit = cls.__convertInfinite( shipLimit.get('limit', -1) )
            ships = set(shipLimit.get('ships', []))
            count = sum(counter.get(sName, 0) for sName in ships)
            if count > limit:
                invalidShips |= ships
                
        return invalidShips
    
    @classmethod
    def validateCombinedClasses(cls, avatars):
        """
        Return set of invalid ships
        """
        combinedClassesLimit = cls.RESTRICTION_DATA.get('combinedClasses', {})
        minCount = combinedClassesLimit.get('min', 0)
        maxCount = combinedClassesLimit.get('max', -1)
        maxCount = cls.__convertInfinite(maxCount)
        shipTypes = combinedClassesLimit.get('classes', [])

        affectedShips = [avatar.ship.ref.ship.fullName for avatar in avatars if avatar.shipType in shipTypes]

        if not minCount <= len(affectedShips) <= maxCount:
            return set(affectedShips)
        return set()
    
    @classmethod
    def validateFilters(cls, avatars):
        """
        Return set of invalid ships
        """
        filter = cls.RESTRICTION_DATA.get('filters', {})
        excludedShips = filter.get('excludedShips', [])
        shipTypes = filter.get('classes', PLAYABLE_SHIP_TYPES)
        shipTiers = filter.get('tiers', [i for i in range(11)])

        invalidShips = set()
        for avatar in avatars:
            ship = avatar.ship.ref.ship
            shipName = ship.fullName

            if shipName in excludedShips:
                invalidShips.add(shipName)
            elif avatar.shipType not in shipTypes:
                invalidShips.add(shipName)
            elif ship.level not in shipTiers:
                invalidShips.add(shipName)
        
        return invalidShips
    
    @classmethod
    def getInvalidShipNames(cls, avatars):
        """
        Return tuple of invalid ships
        """
        if cls.RESTRICTION_DATA is None or len(cls.RESTRICTION_DATA) == 0:
            return tuple()
        return tuple(
                cls.validateShipsCount(avatars) | 
                cls.validateMaxRepeatingShips(avatars) | 
                cls.validateClasses(avatars) | 
                cls.validateLimitedShips(avatars) | 
                cls.validateCombinedClasses(avatars) | 
                cls.validateFilters(avatars)
            )

    @classmethod
    def __convertInfinite(cls, value):
        return 1000 if value < 0 else value
    
    @classmethod
    def __loadRestrictions(cls):
        if not utils.isFile(SHIP_RESTRICTION_FILE):
            utils.logInfo('[TTaroTeamPanel] No ship restriction found.')
            cls.RESTRICTION_DATA = {}
            return

        else:
            with open(SHIP_RESTRICTION_FILE, 'r') as f:
                restrictions = f.read()
                if not restrictions:
                    utils.logInfo('[TTaroTeamPanel] No ship restriction found.')
                    cls.RESTRICTION_DATA = {}
                    return
                try:
                    cls.RESTRICTION_DATA = utils.jsonDecode(restrictions)
                    utils.logInfo('[TTaroTeamPanel] Ship restrictions found.')
                except:
                    cls.RESTRICTION_DATA = {}
                    utils.logInfo('[TTaroTeamPanel] Unknown error occured while parsing ship restrictions. Ship restrictions are disabled')


ShipRestriction.init()


class ShipRestrictionChecker(object):
    """
    Checks the ship compositions in a match
    """
    COMPONENT_KEY = 'modTTaroTeamPanelBannedShips'

    def __init__(self):
        self.entityController = EntityController(ShipRestrictionChecker.COMPONENT_KEY)
        events.onBattleShown(self.__onBattleStart)
        events.onBattleQuit(self.__onBattleEnd)

    def __onBattleStart(self, *args):
        # Works only in the training room
        if not self._isRestrictionAvailable:
            return

        avatarsByTeam = {}
        for entity in dataHub.getEntityCollections('avatar'):
            teamId = entity[CC.avatar].teamId
            avatars = avatarsByTeam.setdefault(teamId, [])
            avatars.append(entity[CC.avatar])

        data = {str(i): ShipRestriction.getInvalidShipNames(avatarsByTeam.get(i, [])) for i in range(2)}

        self.entityController.createEntity()
        self.entityController.updateEntity({'bannedShipsByTeam': data})

        avatarsByTeam.clear()

    def __onBattleEnd(self, *args):
        self.entityController.removeEntity()

    def _isRestrictionAvailable(self):
        entity = dataHub.getSingleEntity('battleInfo')
        if entity:
            return entity[CC.battleInfo].battleType == 'TrainingBattle'
        return False

compChecker = ShipRestrictionChecker()


class ShipConsumableChecker(object):
    """
    Checks the ship consumables in a match
    """
    COMPONENT_KEY = 'modTTaroTeamPanelConsumableRanges'
    TITLE_TO_INFO = {
        'RLSSearch'         : {'type': 'rls',               'attr': 'distShip'},
        'SonarSearch'       : {'type': 'sonar',             'attr': 'distShip'},
        'SubmarineLocator'  : {'type': 'submarineLocator',  'attr': 'acousticWaveMaxDist_submarine_detection'},
        'Hydrophone'        : {'type': 'hydrophone',        'attr': 'hydrophoneWaveRadius'},
    }

    def __init__(self):
        self.entityController = EntityController(ShipConsumableChecker.COMPONENT_KEY)
        events.onBattleShown(self.__onBattleStart)
        events.onBattleQuit(self.__onBattleEnd)

    def __onBattleStart(self, *args):
        self.entityController.createEntity()
        data = self._getAllConsumablesData()
        self.entityController.updateEntity(data)

        utils.logInfo('[TTaroTeamPanel] Ship consumables have been updated.')

    def __onBattleEnd(self, *args):
        self.entityController.removeEntity()

    def _getAllConsumablesData(self):
        consumablesData = {}
        for entity in dataHub.getEntityCollections('shipBattleInfo'):
            ship = entity[CC.shipBattleInfo]
            data = self._getConsumablesDataByShip(ship)
            if data is not None:
                consumablesData[ship.playerId] = data

        return consumablesData
    
    def _getConsumablesDataByShip(self, ship):
        data = {}
        allConsumables = ship.mainConsumables + [cons for consList in ship.altConsumables for cons in consList]
        for cons in allConsumables:
            consInfo = self.__getConsumableInfo(cons)
            if consInfo is None:
                continue
            consType = consInfo['type']
            data[consType] = self.__getConsumableRange(cons, consInfo)

        if len(data) > 0:
            return data
        return None

    def __getConsumableInfo(self, consumable):
        consName = consumable.title
        for ident, consInfo in ShipConsumableChecker.TITLE_TO_INFO.iteritems():
            if ident.upper() in consName:
                return consInfo
        return None

    def __getConsumableRange(self, consumable, consInfo):
        paramName = consInfo['attr']
        for attr in consumable.activeAttributes.neutral:
            if attr.paramName == paramName:
                return attr.measuredValue
            
consChecker = ShipConsumableChecker()