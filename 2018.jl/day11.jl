function highest_sum_square(grid, size)
    max_sum = typemin(Int)
    max_x, max_y = 0, 0
    for x in 1:300-size+1
        for y in 1:300-size+1
            square_sum = sum(grid[y:y+size-1, x:x+size-1])
            if square_sum > max_sum
                max_sum = square_sum
                max_x, max_y = x, y
            end
        end
    end
    return max_x, max_y, max_sum
end

function main()
    grid = zeros(Int, 300, 300)
    serial_number = 18
    for x in 1:300
        for y in 1:300
            rack_id = x + 10
            power_level = (rack_id * y + serial_number) * rack_id
            power_level = mod(power_level, 1000) ÷ 100
            grid[y, x] = power_level - 5
        end
    end

    # part 1
    println(highest_sum_square(grid, 3))

    # part 2
    # quality brute force
    max_sum = typemin(Int)
    max_x, max_y, max_size = 0, 0, 0
    for i in 1:300
        i_x, i_y, i_max = highest_sum_square(grid, i)
        if i_max > max_sum
            max_sum = i_max
            max_x, max_y, max_size = i_x, i_y, i
        end
    end
    println(max_x, " ", max_y, " ", max_size)
end

main()