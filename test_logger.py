import random
import string
import os
from logger import Logger


class TestLogger:
    def test_init(self):
        filename = self._generate_filename()
        logger = Logger(filename)
        assert logger.file_name is filename

    def test_write_metadata(self):
        filename = self._generate_filename()
        logger = Logger(filename)

        logger.write_metadata(pop_size=1000, vacc_percentage=0.2,
                              virus_name='Ebola', mortality_rate=0.8,
                              basic_repro_num=0.05)

        with logger.open_file() as file:
            output = file.read()

        os.remove(filename)

        expected = '1000\t0.2\tEbola\t0.8\t0.05\n'

        assert output == expected

    def test_log_interaction(self):
        filename = self._generate_filename()
        logger = Logger(filename)

        person1 = type('Person', (object,), {'_id': 0})
        person2 = type('Person', (object,), {'_id': 1})

        logger.log_interaction(person1, person2, did_infect=True)
        logger.log_interaction(person1, person2, person2_vacc=True)
        logger.log_interaction(person1, person2, person2_sick=True)

        with logger.open_file() as file:
            output = file.read()

        expected = ('0 infects 1\n'
                    '0 didn\'t infect 1 because vaccinated\n'
                    '0 didn\'t infect 1 because already sick\n')

        os.remove(filename)

        assert output == expected

    def test_log_time_step(self):
        filename = self._generate_filename()
        logger = Logger(filename)

        logger.log_time_step(time_step_number=42,
                             newly_infected_count=21, newly_dead_count=4,
                             total_infected=43, total_dead=2)

        with logger.open_file() as file:
            output = file.read()

        os.remove(filename)

        expected = ('Time step 42 ended, '
                    '21 are infected, '
                    '4 recently died, '
                    '43 got infected, '
                    '2 have died, '
                    'beginning 43...\n')

        assert output == expected

    # https://stackoverflow.com/a/2257449
    def _generate_filename(self, length=64):
        chars = ''.join(random.choices(string.ascii_letters, k=length))
        return f'test_{chars}.txt'
