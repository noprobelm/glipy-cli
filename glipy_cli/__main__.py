"""Main entrypoint for running a simulation from the command line"""

from glipy.state import ConwayState

from . import console
from .args import parse_args
from .renderer import Renderer


def main() -> None:
    """Main entrypoint for running an automaton from the command line"""
    result = parse_args()

    renderer = Renderer(
        cell_type=result.automaton.cell_type,
        initial_state=ConwayState(),
        xmax=console.width,
        ymax=console.height * 2,
    )
    renderer.spawn(renderer.midpoint - result.automaton.midpoint, result.automaton)
    renderer.run(**result.start_kwargs)


if __name__ == "__main__":
    main()
