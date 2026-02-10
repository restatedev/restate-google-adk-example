import hypercorn.asyncio
import asyncio
import restate

from agent import weather_service

app = restate.app(services=[weather_service])


def main():
    """Entry point for running the app."""
    conf = hypercorn.Config()
    conf.bind = ["0.0.0.0:9080"]
    asyncio.run(hypercorn.asyncio.serve(app, conf))


if __name__ == "__main__":
    main()
