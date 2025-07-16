import asyncio


async def periodic():
    while True:
        print('periodic')
        await asyncio.sleep(1)


def main():
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(periodic())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f'Uncaught exception found {e}')


if __name__ == "__main__":
    main()
