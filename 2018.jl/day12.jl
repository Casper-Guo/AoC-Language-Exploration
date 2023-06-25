function pots_translate(pots)
    return Tuple(pot == '#' for pot in pots)
end

function process_rules(rule)
    m = match(r"(.*) => (.*)", rule)
    return pots_translate(m.captures[1]), m.captures[2] == "#"
end

function print_pots(pots)
    for (idx, pot) in sort(collect(pots))
        if pot
            print("#")
        else
            print(".")
        end
    end
    println()
end

function main()
    lines = readlines("input12.txt")
    initial = pots_translate(lines[1][16:end])
    rules = Dict()
    for rule in lines[3:end]
        pots, result = process_rules(rule)
        rules[pots] = result
    end

    pots = Dict(idx - 1 => pot for (idx, pot) in enumerate(initial))
end

main()