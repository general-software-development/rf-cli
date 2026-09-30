import rf_cli

async def main():
    rf_cli.print("[bold]Hello, world!")
    rf_cli.print("test")

    numbers = []
    async for n in rf_cli.read():
        numbers.append(int(n))

    rf_cli.print(f"Output: {sum(numbers)}")

    rf_cli.print("> Name: ", end='')
    name = await rf_cli.read()

    await rf_cli.print(f"Hello, {name}!")

rf_cli.mainfn(__name__, main)
