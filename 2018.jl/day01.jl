function main()
    lines = readlines("input1.txt")

    frequency = 0
    reached = Dict(0 => true)
    found_repeat = false

    # part 1
    for line in lines
        frequency += parse(Int64, line)
        if haskey(reached, frequency)
            println("Repeat: ", frequency)
            found_repeat = true
        end
        reached[frequency] = true
    end
    println(frequency)

    while !found_repeat
        for line in lines
            frequency += parse(Int64, line)
            if haskey(reached, frequency)
                println("Repeat: ", frequency)
                found_repeat = true
                break
            end
        end
        reached[frequency] = true
    end
end

main()