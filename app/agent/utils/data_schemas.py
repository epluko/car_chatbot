from enum import Enum
from pydantic import BaseModel, Field


class FuelType(str, Enum):
    GAS = "gasoline"
    DIESEL = "diesel"
    E85 = "ethanol"
    CNG = "compressed natural gas"
    LPG = "liquefied petroleum gas"
    HYDROGEN = "hydrogen"
    ELECTRIC = "electric"
    BIOFUEL = "biofuel"
    METHANOL = "methanol"
    PROPANE = "propane"


class CarBodyType(str,Enum):
    SEDAN = "sedan"
    HATCHBACK = "hatchback"
    COUPE = "coupe"
    CONVERTIBLE = "convertible"
    SPORTS_COUPLE = "sports coupe"
    SPORTS_CAR = "sports car"
    WAGON = "wagon"
    SPORTS_WAGON = "sports wagon"
    SUV = "suv"
    CROSSOVER = "crossover"
    PICKUP = "pickup"
    VAN = "van"
    MINIVAN = "minivan"
    MUSCLE_CAR = "muscle car"
    ROADSTER = "roadster"
    TARGA = "targa"
    PANEL_VAN = "panel van"
    LIMOUSINE = "limousine"


class CarColor(str, Enum):
    BLACK = "black"
    WHITE = "white"
    SILVER = "silver"
    GREY = "grey"
    RED = "red"
    BLUE = "blue"
    GREEN = "green"
    YELLOW = "yellow"
    ORANGE = "orange"
    BROWN = "brown"
    BEIGE = "beige"
    GOLD = "gold"
    PINK = "pink"
    PURPLE = "purple"
    TAN = "tan"
    BRONZE = "bronze"
    TURQUOISE = "turquoise"
    CHAMPAGNE = "champagne"


class CarProperties(BaseModel):
    make : str | None = Field(
        description = "Official name of car make",
        default=None
    )
    model : str | None = Field(
        description = "Official name of car model",
        default=None
    )
    body_type : CarBodyType | None = Field(
        description = "Body type of a car",
        default=None
    )
    fuel_type : FuelType | None = Field(
        description = "Type of fuel used by a car",
        default=None
    )
    color : CarColor | None = Field(
        description = "Color of a car",
        default=None
    )
