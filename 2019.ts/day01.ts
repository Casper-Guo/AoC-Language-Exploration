import * as fs from 'fs';

function part1_fuel(mass: number): number {
    return Math.trunc(mass / 3) - 2;
}

function part2_fuel(mass: number): number {
    let total_fuel: number = part1_fuel(mass);
    let additional_fuel: number = part1_fuel(total_fuel);

    while (additional_fuel >= 0) {
        total_fuel += additional_fuel;
        additional_fuel = part1_fuel(additional_fuel);
    }

    return total_fuel;
}

const masses: number[] = fs.readFileSync('input01.txt', 'utf8').split('\n').map((line: string) => parseInt(line, 10));

console.log(masses.map(part1_fuel).reduce((a, b) => a + b, 0))
console.log(masses.map(part2_fuel).reduce((a, b) => a + b, 0))
