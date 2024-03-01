"""Manages command line arguments and returns an instance of a Simulator"""

import argparse
import sys
from collections import namedtuple
from typing import List, Optional

from glipy import from_conway_life, from_conway_rle, from_rle_url, random_conway
from glipy.color import Color
from glipy.cell import MooreCell, NeumannCell

from . import console

ArgResult = namedtuple("ArgResult", ["automaton", "start_kwargs"])


def parse_args(unparsed: Optional[List[str]] = None) -> ArgResult:
    """Parses user args into an automaton and the kwargs necessary to start a simulation.

    Returns:
        ArgResult (namedtuple): Contains the 'automaton' and 'start_kwargs' attrs, which are used to run the sim
    """

    parser = argparse.ArgumentParser(
        description="A cellular automaton simulator with support for terminal rendering"
    )

    parser.add_argument("target", nargs="?", default=None)

    parser.add_argument(
        "-r",
        "--refresh-rate",
        type=int,
        default=30,
        help="The refresh rate of the simulation",
    )

    parser.add_argument(
        "-g",
        "--generations",
        type=int,
        default=0,
        help="The number of generations the simulation should run for",
    )

    parser.add_argument(
        "-t",
        "--cell-type",
        type=str,
        choices=["moore", "neumann"],
        default="moore",
        help="The type of cell to use",
    )

    parser.add_argument("-c", "--colors", nargs="?")

    # parser.add_argument(
    #     "-n",
    #     "--no-render",
    #     dest="render",
    #     action="store_false",
    #     default=True,
    #     help="Disables simulation rendering to the terminal",
    # )

    args = vars(parser.parse_args(unparsed or sys.argv[1:]))

    match args["cell_type"]:
        case "moore":
            args["cell_type"] = MooreCell
        case "neumann":
            args["cell_type"] = NeumannCell

    if args["target"] is None:
        automaton = random_conway(
            xmax=console.width, ymax=console.height * 2, cell_type=args["cell_type"]
        )
    elif "http" in args["target"]:
        automaton = from_rle_url(args["target"], cell_type=args["cell_type"])
    elif ".rle" in args["target"]:
        with open(args["target"], "r") as f:
            data = f.read()
        automaton = from_conway_rle(data, cell_type=args["cell_type"])
    elif ".life" in args["target"]:
        with open(args["target"], "r") as f:
            data = f.read()
        automaton = from_conway_life(data, cell_type=args["cell_type"])

    if args["colors"] is not None:
        colors = [Color(color) for color in args["colors"].split(" ")]
        automaton.colors = colors

    del args["target"]
    del args["colors"]
    del args["cell_type"]

    return ArgResult(automaton, args)
