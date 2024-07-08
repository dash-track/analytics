import sys
import pathlib

# Added to make consistent import paths with respect to src
sys.path.append(f"{pathlib.Path(__file__).parent.resolve()}/..")

from src.services.dashtrack import DashTrackService


def main():
    """
    Entry point for the application.
    """
    # Initialize DashTrack service
    dashtrack = DashTrackService()
    dashtrack.run()


if __name__ == "__main__":
    main()
