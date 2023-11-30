function process_rules(rule)
    m = match(r"(.*) => (.*)", rule)
    return m.captures
end

function get_surrounding(idx, pots)
    return pots[idx-2:idx+2]
end

function evolve(pots, rules)
    new_pot = [".", "."]

    for i in 3:length(pots)-2
        push!(new_pot, get(rules, get_surrounding(i, pots), "."))
    end

    push!(new_pot, "..")

    return join(new_pot)
end

function main()
    lines = readlines("input12.txt")
    initial = lines[1]
    rules = Dict()
    for rule in lines[3:end]
        pots, result = process_rules(rule)
        rules[pots] = result
    end

    num_gen = 20
    evolved = repeat('.', num_gen) * initial * repeat('.', num_gen)

    for i in 1:num_gen
        evolved = evolve(evolved, rules)
    end

    # part 1
    plant_sum = 0
    indices = []

    for (idx, pot) in enumerate(evolved)
        if pot == '#'
            push!(indices, idx - num_gen - 1)
            plant_sum += (idx - num_gen - 1)
        end
    end

    println(plant_sum)

    # part 2
    # testing shows that the cycle stablizes at generation 120
    # and then after the pattern shifts right by one per generation
    # so we simulate to generation 120 and record the indices
    stable_indices = [49, 65, 91, 96, 101, 109, 117, 122, 128, 133, 141, 149, 157, 163, 168, 173, 181, 186, 194, 202, 210, 216]

    println(sum(stable_indices) + (50000000000 - 120) * length(stable_indices))
end

main()