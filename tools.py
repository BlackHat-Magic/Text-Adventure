from mcp.server.fastmcp import FastMCP
from typing import Any

import random, re, httpx

mcp = FastMCP("dice")

@mcp.tool()
def roll_die(expression: str, repeat_number: int = 1, reroll_below: int = 1, drop_lowest: int = 0, advantage: bool = False, disadvantage: bool = False) -> str:
    results = []
    for _ in range(repeat_number):
        expression_results = []
        parts = re.split(r'([+-])', expression)
        current_sum = 0
        for i in range(0, len(parts), 2):
            value = parts[i]
            if 'd' in value:
                num, die = value.split('d')
                num = int(num) if num else 1
                die = int(die)
                rolls = []
                if die == 20 and (advantage or disadvantage):
                    for _ in range(num):
                        roll1 = random.randint(1, die)
                        roll2 = random.randint(1, die)
                        if advantage and not disadvantage:
                            roll = max(roll1, roll2)
                        elif disadvantage and not advantage:
                            roll = min(roll1, roll2)
                        else:
                            roll = roll1
                        rerolls = 0
                        while roll < reroll_below and rerolls < 100:
                            roll = random.randint(1, die)
                            rerolls += 1
                        rolls.append(roll)
                else:
                    for _ in range(num):
                        roll = random.randint(1, die)
                        rerolls = 0
                        while roll < reroll_below and rerolls < 100:
                            roll = random.randint(1, die)
                            rerolls += 1
                        rolls.append(roll)
                if drop_lowest > 0 and num > 1:
                    rolls.sort()
                    rolls = rolls[drop_lowest:]
                expression_results.append(f'{num}d{die}: {rolls}')
                current_sum += sum(rolls)
            else:
                try:
                    num = int(value)
                    current_sum += num
                    expression_results.append(str(num))
                except ValueError:
                    pass
        results.append(f'{expression}: {current_sum} ({', '.join(expression_results)})')
    return '\n'.join(results)

if __name__ == "__main__":
    mcp.run(transport="stdio")