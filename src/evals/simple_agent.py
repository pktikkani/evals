import asyncio


async def guess_city(question: str) -> str:
    proc = await asyncio.create_subprocess_exec(
        'claude',
        '-p',
        question,
        '--append-system-prompt',
        'Answer with the city name only, lowercase, no punctuation.',
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    out, err = await proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(f'claude failed: {err.decode().strip()}')
    return out.decode().strip()
