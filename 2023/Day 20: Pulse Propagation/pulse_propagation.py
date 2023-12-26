"""Day 20: Pulse Propagation"""


from collections import defaultdict, deque
from functools import cached_property
from math import prod, lcm


LOW = 0
HIGH = 1


class ModuleConfiguration:
    """A configuration of modules."""

    def __init__(self, configs, modules):
        self.configs = configs
        self.modules = modules

    def __str__(self):
        return '\n'.join(
            f'{module_name}: {module}'
            for module_name, module in self.modules.items()
        )

    @cached_property
    def reversed_configs(self):
        """Return the reversed configuration."""
        reversed_configs = defaultdict(list)
        for source, destinations in self.configs.items():
            for destination in destinations:
                reversed_configs[destination].append(source)

        return dict(reversed_configs)

    def get_module(self, name):
        """Return the module with the given name."""
        return self.modules[name]

    def get_destinations(self, name):
        """Return the destinations of the module with the given name."""
        return self.configs[name]

    def find_conjunctions(self, final_module):
        """Find all conjunctions connected to the final module."""
        conjunctions = []
        queue = [*self.reversed_configs[final_module]]
        while queue:
            source = queue.pop()
            if not isinstance(self.modules[source], Conjunction):
                continue

            if all(
                isinstance(self.modules[destination], FlipFlop)
                for destination in self.reversed_configs[source]
            ):
                conjunctions.append(source)
            else:
                queue.extend(self.reversed_configs[source])

        return conjunctions

    def find_flipflop_chains(self):
        """Find all flip-flop chains in the configuration."""
        return [
            self._find_flipflop_chain(module)
            for module in self.configs['broadcaster']
            if isinstance(self.modules[module], FlipFlop)
        ]

    def _find_flipflop_chain(self, start):
        chain = []
        queue = [start]
        while queue:
            chain.append(flip_flop := queue.pop())
            for destination in self.configs[flip_flop]:
                if isinstance(self.modules[destination], FlipFlop):
                    queue.append(destination)

        return chain


class Module:
    """Base class for all communication modules."""

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f'{self.name}'

    @property
    def state(self):
        """Return the state of the module."""
        return 0

    def receive(self, pulse, source=None):
        """Receive a pulse from a source."""


class Broadcaster(Module):
    """A broadcaster module."""

    def receive(self, pulse, source=None):
        return pulse


class FlipFlop(Module):
    """A flip-flop module."""

    def __init__(self, name):
        super().__init__(name)
        self._state = False

    def __str__(self):
        return f'{self.name}: {self._state}'

    @property
    def state(self):
        return int(self._state)

    def receive(self, pulse, source=None):
        if pulse == LOW:
            if self._state:
                self._state = False
                return LOW

            self._state = True
            return HIGH

        return None


class Conjunction(Module):
    """A conjunction module."""

    def __init__(self, name):
        super().__init__(name)
        self._state = {}

    def __str__(self):
        return f'{self.name}: {self._state}'

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self._state = state

    def receive(self, pulse, source=None):
        self._state[source] = pulse
        return LOW if all(self._state.values()) else HIGH


def parse(filename):
    """Parse a module configuration file."""
    configs = {}
    modules = {}
    conjunction_names = []
    with open(filename, 'r', encoding='utf-8') as file_:
        for line in file_:
            module_name, _, destination_names = line.partition('->')
            module_name = module_name.strip()
            if module_name.startswith('%'):
                module_name = module_name[1:]
                modules[module_name] = FlipFlop(module_name)
                configs[module_name] = parse_destinations(destination_names)
            elif module_name.startswith('&'):
                module_name = module_name[1:]
                modules[module_name] = Conjunction(module_name)
                configs[module_name] = parse_destinations(destination_names)
                conjunction_names.append(module_name)
            elif module_name.startswith('broadcaster'):
                modules[module_name] = Broadcaster(module_name)
                configs[module_name] = parse_destinations(destination_names)
            else:
                raise ValueError(f'Unknown module: {module_name}')

    for conjunction_name in conjunction_names:
        modules[conjunction_name].state = {
            source: LOW
            for source, destination_names in configs.items()
            if conjunction_name in destination_names
        }

    return ModuleConfiguration(configs, modules)


def parse_destinations(destination_names):
    """Parse a module's destinations from a string."""
    return [name.strip() for name in destination_names.strip().split(',')]


def count_pulses(module_config, times):
    """Count the number of pulses in the given module configuration."""
    high = low = 0
    for _ in range(times):
        queue = deque([('button', LOW, 'broadcaster')])
        while queue:
            source, pulse, destination = queue.popleft()
            if pulse is None:
                continue

            if pulse == HIGH:
                high += 1
            elif pulse == LOW:
                low += 1

            try:
                module = module_config.get_module(destination)
            except KeyError:
                continue

            pulse = module.receive(pulse, source)
            source = destination
            queue.extend(
                (source, pulse, destination)
                for destination in module_config.get_destinations(source)
            )

    return {'high': high, 'low': low}


def count_button_presses(module_config, final_module):
    """Return the fewest number of button presses required to deliver a
    single low pulse to the given module name.
    """
    numbers = {
        module: 2 ** chain.index(module)
        for chain in module_config.find_flipflop_chains()
        for module in chain
    }
    conjunctions = [
        module_config.get_module(module)
        for module in module_config.find_conjunctions(final_module)
    ]
    return lcm(*(
        sum(numbers[module] for module in conjunction.state)
        for conjunction in conjunctions
    ))


def main():
    """Main program."""
    module_config = parse('input')
    assert prod(count_pulses(module_config, times=1000).values()) == 819397964
    assert count_button_presses(module_config, 'rx') == 252667369442479


if __name__ == '__main__':
    main()
