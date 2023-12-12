function react_once(polymer)
    # perform the first found reaction
    for i in eachindex(polymer)
        if i == 1
            continue
        end
        if abs(polymer[i] - polymer[i-1]) == 32
            return polymer[1:i-2] * polymer[i+1:end]
        end
    end
    return polymer
end

function full_reaction(polymer)
    reactant = polymer
    product = react_once(reactant)
    while product != reactant
        reactant = product
        product = react_once(reactant)
    end
    return product
end

function main()
    file = open("input05.txt")
    polymer = read(file, String)
    close(file)

    # part 1
    println(length(full_reaction(polymer)))

    # part 2
    shortest_product = typemax(Int)
    for i in 65:90
        reactant = replace(polymer, Char(i) => "", Char(i + 32) => "")
        product_length = length(full_reaction(reactant))
        if product_length < shortest_product
            shortest_product = product_length
        end
    end
    println(shortest_product)
end

main()