import random
from person import Person
from virus import Virus


class TestPerson:
    def test_init(self):
        ebola = Virus("Ebola", 0.8, 0.1)
        person = Person(0, False, ebola)

        assert person.infection is ebola
        assert person.is_alive is True
        assert person.is_vaccinated is False
        assert person._id is 0

    def test_did_survive_infection(self):
        ebola = Virus("Ebola", 0.8, 0.1)
        person = Person(0, False, ebola)

        if person.did_survive_infection():
            assert person.is_alive is True
            assert person.is_vaccinated is True
            assert person.infection is None
        else:
            assert person.is_alive is False
