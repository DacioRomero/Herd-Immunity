import random
import sys
from person import Person
from logger import Logger
from virus import Virus

random.seed(42)


class Simulation():
    '''
    Main class that will run the herd immunity simulation program. Expects
    initialization parameters passed as command line arguments when file is
    run.

    Simulates the spread of a virus through a given population. The percentage
    of the population that are vaccinated, the size of the population, and the
    amount of initially infected people in a population are all variables that
    can be set when the program is run.

    _____Attributes______

    logger: Logger object. The helper object that will be responsible for
    writing all logs to the simulation.

    population_size: Int. The size of the population for this simulation.

    population: [Person]. A list of person objects representing all people in
    the population.

    next_person_id: Int. The next available id value for all created person
    objects. Each person should have a unique _id value.

    virus_name: String. The name of the virus for the simulation. This will be
    passed to the Virus object upon instantiation.

    mortality_rate: Float between 0 and 1. This will be passed to the Virus
    object upon instantiation.

    basic_repro_num: Float between 0 and 1. This will be passed to the Virus
    object upon instantiation.

    vacc_percentage: Float between 0 and 1. Represents the total percentage of
    population vaccinated for the given simulation.

    current_infected: Int. The number of currently people in the population
    currently infected with the disease in the simulation.

    total_infected: Int. The running total of people that have been infected
    since the simulation began, including any people currently infected.

    total_dead: Int. The number of people that have died as a result of the
    infection during this simulation. Starts at zero.


    _____Methods_____

    __init__(population_size, vacc_percentage, virus_name, mortality_rate,
     basic_repro_num, initial_infected=1):
        -- All arguments will be passed as command-line arguments when the file
            is run.
        -- After setting values for attributes, calls self._create_population()
            in order to create the population array that will be used for this
            simulation.

    _create_population(self, initial_infected):
        -- Expects initial_infected as an Int.
        -- Should be called only once, at the end of the __init__ method.
        -- Stores all newly created Person objects in a local variable,
            population.
        -- Creates all infected person objects first. Each time a new one is
            created, increments infected_count variable by 1.
        -- Once all infected person objects are created, begins creating

            healthy person objects. To decide if a person is vaccinated or not,
            generates a random number between 0 and 1. If that number is
            smaller than self.vacc_percentage, new person object will be
            created with is_vaccinated set to True. Otherwise, is_vaccinated
            will be set to False.
        -- Once len(population) is the same as self.population_size, returns
            population.
    '''

    def __init__(self, population_size, vacc_percentage, virus_name,
                 mortality_rate, basic_repro_num, initial_infected=1):
        self.population_size = population_size
        self.vacc_percentage = vacc_percentage
        self.total_infected = initial_infected
        self.current_infected = initial_infected
        self.next_person_id = 0
        self.total_dead = 0

        self.virus = Virus(virus_name, mortality_rate, basic_repro_num)
        file_name = (f'{virus_name}_simulation_pop_{population_size}_vp_'
                     f'{vacc_percentage}_infected_{initial_infected}.txt')
        self.logger = Logger(file_name)

        self.newly_infected = []
        self.population = self._create_population(initial_infected)

    def _create_population(self, initial_infected):
        population = []
        infected_count = 0

        while len(population) != pop_size:
            if infected_count != initial_infected:
                population.append(Person(self.next_person_id,
                                         is_vaccinated=False,
                                         infected=self.virus))
                infected_count += 1
            else:
                is_vaccinated = random.random() < self.vacc_percentage
                population.append(Person(self.next_person_id, is_vaccinated))

            self.next_person_id += 1

        return population

    def _simulation_should_continue(self):
        return (self.current_infected > 0 and
                self.total_dead < self.population_size)

    def run(self):
        time_step_counter = 0
        should_continue = self._simulation_should_continue()

        while should_continue:
            self.time_step()
            self.logger.log_time_step(time_step_counter)
            time_step_counter += 1

            should_continue = self._simulation_should_continue()

        print(f'The simulation has ended after {time_step_counter} turns.')

    def time_step(self):
        alive = list(filter(lambda p: p.is_alive, self.population))
        infected = list(filter(lambda p: p.infected, alive))

        for person in infected:
            for i in range(100):
                self.interaction(person, random_person=random.choice(alive))

        for person in infected:
            if person.did_survive_infection():
                self.logger.log_survival(person, did_die_from_infection=False)
            else:
                self.logger.log_survival(person, did_die_from_infection=True)
                self.total_dead += 1

        self._infect_newly_infected()

    def interaction(self, person, random_person):
        assert person.is_alive is True
        assert random_person.is_alive is True

        if random_person.is_vaccinated:
            self.logger.log_interaction(person, random_person,
                                        person2_vacc=True)
        elif random_person.infected:
            self.logger.log_interaction(person, random_person,
                                        person2_sick=True)
        else:
            if random.random() < person.infected.basic_repro_num:
                self.newly_infected.append(random_person._id)
                self.total_infected += 1
                self.logger.log_interaction(person, random_person,
                                            did_infect=True)
            else:
                self.logger.log_interaction(person, random_person,
                                            did_infect=False)

    def _infect_newly_infected(self):
        infected_people = list(filter(lambda p: p._id in self.newly_infected,
                                      self.population))

        for person in infected_people:
            person.infected = self.virus

        self.current_infected = len(infected_people)
        self.total_infected += self.current_infected
        self.newly_infected = []


if __name__ == '__main__':
    params = sys.argv[1:]

    pop_size = int(params[0])
    vacc_percentage = float(params[1])
    virus_name = str(params[2])
    mortality_rate = float(params[3])
    basic_repro_num = float(params[4])

    if len(params) == 6:
        initial_infected = int(params[5])
    else:
        initial_infected = 1

    simulation = Simulation(pop_size, vacc_percentage, virus_name,
                            mortality_rate, basic_repro_num, initial_infected)
    simulation.run()
