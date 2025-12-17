import argparse

class CliParser:
    @staticmethod
    def parse():
        parser = argparse.ArgumentParser(description="Filter candidates and store in MongoDB.")
        parser.add_argument('--industry', type=str, help='Industry to filter by')
        parser.add_argument('--skills', type=str, help='Comma-separated list of required skills')
        parser.add_argument('--min-years', type=float, help='Minimum total years of experience')
        parser.add_argument('--mongo-uri', type=str, default='mongodb://localhost:27017', help='MongoDB URI')
        parser.add_argument('--db', type=str, default='test', help='MongoDB database name')
        return parser.parse_args()
