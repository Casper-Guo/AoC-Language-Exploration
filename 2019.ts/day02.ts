import fs from 'fs';
import { IntCode } from './intcode';

const instructions = fs.readFileSync("input02.txt", 'utf8');
const intCode = new IntCode(instructions);
intCode.memory[1] = 12;
intCode.memory[2] = 2;
intCode.run();
console.log(intCode.memory[0]);

for (let noun = 0; noun <= 99; noun++) {
    for (let verb = 0; verb <= 99; verb++) {
        intCode.resetProgram();
        intCode.memory[1] = noun;
        intCode.memory[2] = verb;
        intCode.run();
        if (intCode.memory[0] === 19690720) {
            console.log(100 * noun + verb);
            break;
        }
    }
}