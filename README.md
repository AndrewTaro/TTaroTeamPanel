# TTaro Team Panel
The mod supports almost all the features that the traditional team panels have.  
You can personalize it to be the simplest team panel, or the most info-flooded one.

# Overview
![The simplest to the middle ground](https://github.com/AndrewTaro/TTaroTeamPanel/assets/36262823/bccff306-0957-4506-b68d-f86cb37dcd83)
![Or you can display everything at once. Even then you are still able to hide them while Alt key is not pressed!](https://github.com/AndrewTaro/TTaroTeamPanel/assets/36262823/b6577fe1-a8d8-4139-8dfc-ad14bfb6ebb8)

# Features
- Each element can be separately shown/hidden.
- You can set the ship stats (such as torpedo range, radar range, etc) to be visible only when you press the ALT key. So that they no longer occupy half of the screen for an entire battle!
- The ship stats include the airstrike range, range of alternative torpedo, AA range, underwater speed, air detection, etc. which were often not present in the existing mods.
- Hovering the mouse on the player allows you to check the detailed stats of the ship. For example, Main gun DPM, the number of AA bubbles, and Depth charge parameters.
- When Regen Monitor is installed, the HP bar also reflects the regeneratable HP of your allies.
- (Technical aspect): The mod is built with Unbound2 technology, which is a better framework in terms of maintenance, performance, and code-readability compared to Unbound1 which the current panels are using.

# Install
1. Download a zip.
2. Unzip the archive and you should get `gui`, `PnFMods` folders, and `PnFModsLoader.py`.
3. Move them to `(wows)/bin/(latest_number)/res_mods/`. So the path will look like `res_mods/gui/unbound2/mods/ttaro_teampanel.unbound`
4. Done!

# Config
[TTaro Mod Config](../../../TTaroModConfig) supports this mod.  You can adjust many features from that menu.

# Ship Restriction Highlight
This feature highlights the invalid ships or composition in the teams, making it easier to identify the forfeit in tournaments.

Creating `ship_restrictions.json` file in `res_mods` folder will activate it.  (So the path will be `res_mods/ship_restrictions.json`)
- `minShips`: Minimum number of ships to be a valid team.
- `maxShips`: Maximum number of ships to be a valid team.
- `maxRepeatingShips`: Maximum number of duplicating ships in a team.
- `classes`: Minimum and maximum number of classes in a team. `-1` indicates unlimited.
- `limitedShips`: So-called bracket bans. There can be multiple brackets.
    - `ships`: Ships in a bracket
    - `limit`: Maximum number of ships in this bracket
- `combinedClasses`: Restriction on the number of ships from multiple classes combined.
    - `min`: Minimum number of ships
    - `max`: Maximum number of ships
    - `classes`: List of classes to combine
- `filters`: Various filters.
    - `excludedShips`: Prohibited ships.
    - `classes`: Allowed classes.
    - `tiers`: Allowed tiers.
```json
{
    "minShips": 7,
    "maxShips": 9,
    "maxRepeatingShips": -1,
    "classes": {
        "AirCarrier": [0, 0],
        "Battleship": [0, 2],
        "Cruiser": [0, -1],
        "Destroyer": [0, -1],
        "Submarine": [0, 0]
    },
    "limitedShips": [
        {
            "ships": [
				"PRSB110_Sovetskaya_Rossiya",
				"PASB510_Ohio",
				"PBSB210_St_Vincent",
				"PASB110_Vermont"
			],
            "limit": 1
        }
    ],
    "combinedClasses": {
        "min": 0,
        "max": 2,
        "classes": ["Battleship"]
    },
    "filters": {
        "excludedShips": [
			"PJSD890_AZUR_Shimakaze",
			"PJSB700_ARP_Yamato",
			"PBSC810_Defence",
			"PJSC610_Kitakami",
			"PFSD810_Colorful_Kleber",
			"PZSD510_Lushun",
			"PISC590_Black_Napoli",
			"PASC610_Puerto_Rico",
			"PASB720_Rhode_Island",
			"PWSD610_Smaland",
			"PRSC610_Smolensk",
			"PRSC530_Black_Smolensk",
			"PASD510_Somers",
			"PBSB510_Thunderer",
			"PASB730_Wisconsin",
			"PJSC590_Black_Yoshino",
			"PRSC210_Pr_84_Alexander_Nevsky",
			"PGSC710_Hildebrand",
			"PRSC810_Komissar",
			"PASB210_Louisiana"
		],
        "classes": ["Battleship", "Cruiser", "Destroyer"],
        "tiers": [10]
    }
}
```
