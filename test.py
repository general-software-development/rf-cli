import rf_cli

async def main():
    rf_cli.print("[bold]Hello, world!")
    rf_cli.print("test")

    numbers = []
    async for n in rf_cli.read():
        numbers.append(int(n))

    await rf_cli.print(f"Output: {sum(numbers)}")

    rf_cli.print(1 + '3')

rf_cli.mainfn(__name__, main)
