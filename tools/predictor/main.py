#!/usr/bin/env python3

"""
CLI utility for predictions and reports
"""

from argparse import ArgumentParser
from utils.report import generate_report_for_user


def main() -> None:
    """
    Main procedure of the predictor
    :return: None
    """
    parser = ArgumentParser(
        description='Predictor, a CLI tool for generating predictions and reports'
    )
    parser.add_argument(
        '--user',
        help='User ID',
        type=int,
        dest='user_id'
    )
    parser.add_argument(
        '--method',
        help='Prediction method',
        type=str,
        dest='prediction_method',
        default='bullet',
        choices=['bullet']
    )
    parser.add_argument(
        '--ratio',
        help='Trajectory split ratio',
        type=float,
        dest='ratio',
        default=0.5
    )
    parser.add_argument(
        '--threshold',
        help='Threshold',
        type=float,
        dest='threshold',
        default=10
    )
    parser.add_argument(
        '--time',
        help='Prediction time',
        type=float,
        dest='time',
        default=60
    )
    parser.add_argument(
        '--verbosity',
        help='Verbosity level (for debugging)',
        type=int,
        dest='verbosity',
        default=0
    )

    args = parser.parse_args()

    report = generate_report_for_user(
        user_id=args.user_id,
        method=args.prediction_method,
        ratio=args.ratio,
        threshold=args.threshold,
        time=args.time,
        verbosity=args.verbosity
    )
    print(report)


if __name__ == '__main__':
    main()
