#!/usr/bin/env python3
"""
TreeCatt - Main module
"""

import sys

from treecatt.core import TreeCatt
from treecatt.cli import parse_arguments


def main() -> int:
    """Main entry point for TreeCatt CLI"""
    parser  = parse_arguments()
    args    = parser.parse_args()

    treecatt = TreeCatt(
        root_path           = args.path,
        show_tree_only      = args.tree,
        show_tree_size      = args.tree_size,
        show_permissions    = args.permissions,
        show_dates          = args.dates,
        show_git_status     = args.git_status,
        sort_by             = args.sort,
        max_depth           = args.depth,
    )

    return treecatt.run()


if __name__ == '__main__':
    sys.exit(main())