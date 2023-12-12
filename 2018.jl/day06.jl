function process_line(line)
    m = match(r"(\d+), (\d+)", line)
    return map(x -> parse(Int64, x), m.captures)
end

function manhattan_dist(self, other)
    return abs(self[1] - other[1]) + abs(self[2] - other[2])
end

function find_nearest(current, coords)
    dist = map(coord -> manhattan_dist(current, coord), coords)

    if count(i -> i == minimum(dist), dist) > 1
        return length(coords) + 1
    end
    return argmin(dist)
end

function check_inf(idx, coords)
    self_x, self_y = coords[idx]

    # constraint on the four directions
    left, right, up, down = false, false, false, false

    for i in eachindex(coords)
        if i == idx
            continue
        end
        other_x, other_y = coords[i]
        diff_x, diff_y = abs(other_x - self_x), abs(other_y - self_y)

        if other_x == self_x
            if other_y < self_y
                up = true
            elseif other_y > self_y
                down = true
            end
        elseif other_x > self_x
            if other_y == self_y
                right = true
            elseif other_y < self_y
                if diff_x == diff_y
                    right = true
                    up = true
                elseif diff_x > diff_y
                    right = true
                else
                    # diff_x < diff_y
                    up = true
                end
            else
                # other_y > self_y
                if diff_x == diff_y
                    right = true
                    down = true
                elseif diff_x > diff_y
                    right = true
                else
                    # diff_x < diff_y
                    down = true
                end
            end
        else
            # other_x < self_x
            if other_y == self_y
                left = true
            elseif other_y < self_y
                if diff_x == diff_y
                    left = true
                    up = true
                elseif diff_x > diff_y
                    left = true
                else
                    # diff_x < diff_y
                    up = true
                end
            else
                # other_y > self_y
                if diff_x == diff_y
                    left = true
                    down = true
                elseif diff_x > diff_y
                    left = true
                else
                    # diff_x < diff_y
                    down = true
                end
            end
        end
    end

    return !(left && right && up && down)
end

function main()
    lines = readlines("input06.txt")
    coords = [process_line(line) for line in lines]

    # Part 1
    inf_area = [check_inf(i, coords) for i in eachindex(coords)]

    # add a dummy for the tied coordinates
    push!(inf_area, true)

    min_x, max_x = extrema(map(x -> x[1], coords))
    min_y, max_y = extrema(map(x -> x[2], coords))

    # add one for the dummy
    areas = zeros(length(coords) + 1)

    for x in min_x:max_x
        for y in min_y:max_y
            nearest_coord = find_nearest([x, y], coords)
            areas[nearest_coord] += 1
        end
    end

    max_area = 0
    for (idx, area) in enumerate(areas)
        if !inf_area[idx] && area > max_area
            max_area = area
        end
    end

    println(max_area)

    # part 2
    region_size = 0
    max_dist = 10000
    search_range = ceil(max_dist / length(coords))

    for x in (min_x-search_range):(max_x+search_range)
        for y in (min_y-search_range):(max_y+search_range)
            if sum(map(coord -> manhattan_dist([x, y], coord), coords)) < max_dist
                region_size += 1
            end
        end
    end

    println(region_size)
end

main()