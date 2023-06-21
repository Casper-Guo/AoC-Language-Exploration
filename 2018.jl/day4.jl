function extract_timestamp(line)
    m = match(r"\[(\d+)\-(\d+)\-(\d+) (\d+):(\d+)\]", line)
    return map(x -> parse(Int64, x), m.captures)
end

function main()
    lines = readlines("input4.txt")
    perm = sortperm(lines, by=extract_timestamp)
    lines = lines[perm]
    sleep_tracker = Dict()
    guard = -1
    awake, sleep = -1, -1

    for line in lines
        if occursin("Guard", line)
            guard = parse(Int64, match(r"#(\d+)", line).captures[1])
            if !haskey(sleep_tracker, guard)
                sleep_tracker[guard] = zeros(60)
            end
        elseif occursin("wakes", line)
            awake = extract_timestamp(line)[5]
            sleep_tracker[guard][sleep+1:awake] .+= 1
        elseif occursin("asleep", line)
            sleep = extract_timestamp(line)[5]
        else
            throw(ArgumentError("Unexpected line formatting."))
        end
    end

    # in order:
    # the id of the guard who spent the most minutes sleeping
    # the amount of minutes he spent sleeping
    # the minute he spent sleeping the most
    part1_id, part1_minutes, part1_minute = -1, -1, -1

    # in order
    # the id of the guard who most frequently sleep on the same minute
    # the number of times he is asleep at that minute
    # the minute he sleeps at most frequently
    part2_id, part2_freq, part2_minute = -1, -1, -1
    for (id, minutes) in sleep_tracker
        # part 1
        minutes_asleep = sum(minutes)
        if minutes_asleep > part1_minutes
            part1_minutes = minutes_asleep
            part1_id = id
            part1_minute = findmax(minutes)[2] - 1
        end

        # part 2
        freq, minute = findmax(minutes)
        # convert 1-indexing
        minute -= 1

        if freq > part2_freq
            part2_id = id
            part2_freq = freq
            part2_minute = minute
        end
    end
    println(part1_id * part1_minute)
    println(part2_id * part2_minute)
end

main()