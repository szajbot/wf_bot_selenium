from structure.Juice import Juice
from structure.Plantable import Plantable

juices = [
    Juice("Sok marchwiowy", "foodworld_selection_item130", 180),
    Juice("Sok pomidorowy", "foodworld_selection_item131", 180),
    Juice("Mleko truskawkowe", "foodworld_selection_item132", 90),
    Juice("Mleko rzodkiewkowe", "foodworld_selection_item134", 90)
]

farmPlants = [
    Plantable("Marchewki", "rackitem17", 1, 15),
    Plantable("Truskawki", "rackitem20", 1, 480),
    Plantable("Zboze", "rackitem1", 2, 20),
    Plantable("Kukurydza", "rackitem2", 4, 45),
    Plantable("Ogorki", "rackitem18", 1, 90),
    Plantable("Cebule", "rackitem22", 1, 500),
    Plantable("Koniczyna", "rackitem3", 2, 45),
    Plantable("Pomidory", "rackitem21", 1, 600),
    Plantable("Rzodkiewki", "rackitem19", 1, 240),
    Plantable("Szpinak", "rackitem23", 1, 800),
    Plantable("Kalafiory", "rackitem24", 1, 720),
    Plantable("Rzepak", "rackitem4", 4, 90),
    Plantable("Buraki pastewne", "rackitem5", 4, 120)
]

chickenPlants = [
    Plantable("Zboze", "rackitem1", 2, 20),
    Plantable("Kukurydza", "rackitem2", 4, 45)
]

cowPlants = [
    Plantable("Koniczyna", "rackitem3", 2, 45),
    Plantable("Rzepak", "rackitem4", 4, 90)
]

field = []
for x in range(1, 121):
    field.append("field" + str(x))