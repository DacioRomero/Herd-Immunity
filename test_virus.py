import random
from virus import Virus


class TestPerson:
    def test_init(self):
        virus_name = "Ebola"
        mortality_rate = 0.8
        basic_repro_num = 0.1
        virus = Virus(virus_name, mortality_rate, basic_repro_num)

        assert virus.name is virus_name
        assert virus.mortality_rate is mortality_rate
        assert virus.basic_repro_num is basic_repro_num
