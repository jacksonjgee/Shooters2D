import asyncio
import pygame

from src.game.game import Game


async def main() -> None:
    game = Game()
    await game.run()


if __name__ == "__main__":
    asyncio.run(main())