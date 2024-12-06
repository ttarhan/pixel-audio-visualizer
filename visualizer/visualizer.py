import os
import time
from typing import Iterable, Set
import numpy as np
import sacn

from .config import ELEMENTS, DMX_FPS, DATA_SOURCES, CLOCK_SOURCE

np.set_printoptions(threshold=500000)

BIND_ADDRESS = os.environ.get("BIND_ADDRESS", "0.0.0.0")


class Visualizer:
    """
    The audio analyzer
    """

    def __init__(self) -> None:
        self.sender: sacn.sACNsender = None
        self.all_universes = tuple(universe for element in ELEMENTS for universe in element.get_universes())
        self.active_universes: Set[int] = set()

    def _start_universe(self, universe: int) -> None:
        print(f"Start universe: {universe}")
        self.sender.activate_output(universe)
        self.sender[universe].multicast = True

    def _stop_universe(self, universe: int) -> None:
        print(f"Stop universe: {universe}")
        self.sender.deactivate_output(universe)

    def _manage_universes(self, desired_active_universes: Iterable[int]) -> None:
        for universe in self.all_universes:
            if universe in desired_active_universes and universe not in self.active_universes:
                self._start_universe(universe)
                self.active_universes.add(universe)
            elif universe not in desired_active_universes and universe in self.active_universes:
                self._stop_universe(universe)
                self.active_universes.discard(universe)

    def run(self) -> None:
        """
        Starts listening for audio
        """
        # Startup
        self.sender = sacn.sACNsender(fps=DMX_FPS, universeDiscovery=False, bind_address=BIND_ADDRESS)

        self.sender.start()

        for datasource in DATA_SOURCES.values():
            datasource.start()

        CLOCK_SOURCE.start()

        # Main loop
        lt = time.time()  # pylint:disable=unused-variable
        run = True

        print("Running")

        while run:
            # Clock cycle
            CLOCK_SOURCE.tick()

            # Data source processing
            for datasource in DATA_SOURCES.values():
                datasource.process()

            # Get ready to process elements
            elements_to_process = tuple(element for element in ELEMENTS if element.is_active())
            universes_to_process = tuple(
                universe for element in elements_to_process for universe in element.get_universes()
            )
            self._manage_universes(universes_to_process)

            # Process elements
            universe_data = {}

            for e in elements_to_process:
                render_result = e.render(DATA_SOURCES)
                universe_data.update(render_result)

            # Process output
            for universe, current_universe_data in universe_data.items():
                flatened = np.reshape(current_universe_data, -1)  # Flatten RGB
                flatened_bytes = tuple(flatened.tobytes())
                self.sender[universe].dmx_data = flatened_bytes

            # print(f'Diff: {round(time.time()-lt,4)}')
            lt = time.time()

        # Cleanup
        self.sender.stop()
