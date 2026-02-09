#!/usr/bin/env python3
"""
TreeCatt - Main module
"""

import os
import sys
import argparse

from treecatt.core import TreeCatt
from treecatt.cli import parse_arguments, parse_size

VERSION = "0.1.4"


def main() -> int:
    """Main entry point for TreeCatt CLI"""
    parser = parse_arguments()
    args = parser.parse_args()

    # Validation: enable checksums if duplicates requested
    if args.duplicates and not args.checksums:
        args.checksums = 'md5'

    # Parse max file size
    max_file_size = parse_size(args.max_size)
    
    # Create TreeCatt instance
    treecatt = TreeCatt(
        root_path               = args.path,
        ignore_patterns         = args.ignore,
        view_sensitive          = args.view,
        max_file_size           = max_file_size,
        show_tree               = args.tree,
        show_tree_size          = args.tree_size,
        show_line_numbers       = args.line_numbers,
        show_git_status         = args.git_status,
        show_permissions        = args.permissions,
        show_dates              = args.dates,
        show_checksums          = bool(args.checksums),
        checksum_type           = args.checksums or 'md5',
        filter_by_date          = args.filter_date,
        search_content          = args.search,
        show_duplicates         = args.duplicates,
        sort_by                 = args.sort,
        max_depth               = args.depth,
        include_only            = args.include,
        no_default_ignore       = args.no_default_ignore
    )

    # Run TreeCatt
    return treecatt.run()


if __name__ == '__main__':
    sys.exit(main())