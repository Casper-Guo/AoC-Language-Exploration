function process_line(line)
    m = match(r"#\d+ @ (\d+),(\d+): (\d+)x(\d+)", line)
    return map(x -> parse(Int64, x), m.captures)
end

function main()
    grid = zeros(Int16, 1000, 1000)
    lines = readlines("input3.txt")

    for line in lines
        col_start, row_start, col_range, row_range = process_line(line)
        grid[col_start+1:col_start+col_range, row_start+1:row_start+row_range] .+= 1
    end

    # part 1
    mask = map(x -> x > 1, grid)
    println(length(grid[mask]))

    for i in eachindex(lines)
        col_start, row_start, col_range, row_range = process_line(lines[i])
        claim = grid[col_start+1:col_start+col_range, row_start+1:row_start+row_range]
        if sum(claim) == col_range * row_range
            println(i)
            break
        end
    end
end

main()