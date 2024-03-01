import sys
import time
from typing import Union

from glipy.automaton import Automaton
from rich.console import Console, ConsoleOptions, RenderResult
from rich.live import Live
from rich.segment import Segment
from rich.style import Style


class Renderer(Automaton):
    def run(
        self,
        refresh_rate: int = 30,
        generations: Union[float, int] = 0,
    ) -> None:
        """Sets initial parameters for the simluation, then runs it

        Args:
            generation (Union[float, int]): The number of generations the simulation should run for. Defaults to 0 (infinity)
            refresh_rate (int): The number of times the simluation should run before sleeping. Defaults to 0
            debug (bool): Controls if the simulation runs in debug mode. This will run cProfile and disable rendering
        """
        if refresh_rate == -1:
            sleep = 0.0
        elif refresh_rate == 0:
            sleep = float("inf")
        else:
            sleep = 1 / refresh_rate

        if generations == 0:
            generations = float("inf")

        try:
            with Live(self, screen=True, auto_refresh=False) as live:
                if sleep == float("inf"):
                    while True:
                        time.sleep(1)
                while self.generation < generations:
                    self.evolve()
                    live.update(self, refresh=True)
                    time.sleep(sleep)

        except KeyboardInterrupt:
            sys.exit(0)

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        """Renders each Cell in the simulation using the Rich Console Protocol

        Due to the typical 2:1 height/width aspect ratio of a terminal, each cell rendered from the CellMatrix simulation
        actually occupies 2 rows in the terminal. I picked up this trick from rich's __main__ module. Run
        'python -m rich and observe the color palette at the top of stdout for another example of what this refers to.

        Yields:
            2 cells in the simulation, row by row, until all cell states have been rendered.
        """
        for y in range(self.ymax)[::2]:
            for x in range(self.xmax + 1):
                bg = self.matrix[y][x].state.color
                fg = self.matrix[y + 1][x].state.color
                yield Segment("▄", Style(color=fg, bgcolor=bg))
            yield Segment.line()
