function letter_freq(box_id)
    freq = Dict()

    for letter in box_id
        freq[letter] = get(freq, letter, 0) + 1
    end

    return freq
end

function check_freq(letter_freq)
    has_two, has_three = false, false

    for freq in values(letter_freq)
        if freq == 2
            has_two = true
        elseif freq == 3
            has_three = true
        end
    end

    return has_two, has_three
end

function find_correct_ids(id1, id2)
    num_diffs = 0
    for i in eachindex(id1)
        if id1[i] != id2[i]
            num_diffs += 1
        end
        if num_diffs > 1
            return false
        end
    end
    if num_diffs == 1
        println(id1)
        println(id2)
        return true
    end
    return false
end


function main()
    lines = readlines("input02.txt")

    # part 1
    exactly_two, exactly_three = 0, 0
    for line in lines
        has_two, has_three = check_freq(letter_freq(line))
        exactly_two += Int(has_two)
        exactly_three += Int(has_three)
    end

    println(exactly_two * exactly_three)
    i = 0
    found_match = false

    while !found_match
        for j in 1:i-1
            if find_correct_ids(lines[i], lines[j])
                found_match = true
                break
            end
        end
        i += 1
    end
end

main()