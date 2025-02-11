class IntCode {
    public instructions: number[];
    public memory: number[];
    private instructionPointer = 0;

    constructor(instructions: string) {
        this.instructions = instructions.split(',').map(Number);
        this.memory = this.instructions.slice();
    }

    public resetMemory(): void {
        this.memory = this.instructions.slice();
    }

    public resetProgram(): void {
        this.instructionPointer = 0;
        this.resetMemory();
    }

    public execute(opcode: number, param1: number, param2: number, param3: number): void {
        switch (opcode) {
            case 1:
                this.memory[param3] = this.memory[param1] + this.memory[param2];
                this.instructionPointer += 4;
                break;
            case 2:
                this.memory[param3] = this.memory[param1] * this.memory[param2];
                this.instructionPointer += 4;
                break;
            default:
                throw Error(`Invalid opcode: ${opcode}`);
        }
    }

    public run(): void {
        while (this.instructions[this.instructionPointer] !== 99) {
            const opcode: number = this.instructions[this.instructionPointer];
            const param1: number = this.instructions[this.instructionPointer + 1];
            const param2: number = this.instructions[this.instructionPointer + 2];
            const param3: number = this.instructions[this.instructionPointer + 3];
            
            this.validate_params(param1, param2, param3);
            this.execute(opcode, param1, param2, param3);
        }
    }

    private validate_params(param1: number, param2: number, param3: number): void {
        if (param1 >= this.instructions.length) {
            throw RangeError(`Operand 1 out of range: ${param1}`);
        }
        if (param2 >= this.instructions.length) {
            throw RangeError(`Operand 2 out of range: ${param2}`);
        }
        if (param3 >= this.instructions.length) {
            throw RangeError(`Operand 3 out of range: ${param3}`);
        }
    }
}

export { IntCode };