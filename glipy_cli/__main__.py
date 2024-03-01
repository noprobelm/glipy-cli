"""Main entrypoint for running a simulation from the command line"""

from glipy.cell import MooreCell
from glipy.state import ConwayState

from . import console
from .args import parse_args
from .renderer import Renderer


def main() -> None:
    """Main entrypoint for running an automaton from the command line"""
    result = parse_args()

    renderer = Renderer(
        cell_type=MooreCell,
        initial_state=ConwayState,
        xmax=console.width,
        ymax=console.height * 2,
    )
    try:
        renderer.spawn(renderer.midpoint - result.automaton.midpoint, result.automaton)
        renderer.run(**result.start_kwargs)
    except Exception as e:
        print(
            f"{renderer.xmax}, {renderer.ymax}, {result.automaton.xmax}, {result.automaton.ymax}"
        )
        print(e)


if __name__ == "__main__":
    main()
