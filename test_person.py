import random
from person import Person
from virus import Virus


class TestPerson:
    def test_init(self):
        ebola = Virus("Ebola", 0.8, 0.1)
        person = Person(0, False, ebola)

        assert person.infected is ebola
        assert person.is_alive is True
        assert person.is_vaccinated is False
        assert person._id is 0

    def test_did_survive_infection(self):
        ebola = Virus("Ebola", 0.8, 0.1)
        person = Person(0, False, ebola)

        person.did_survive_infection()

        if person.infected:
            assert person.is_alive is False
        else:
            assert person.is_vaccinated is True
