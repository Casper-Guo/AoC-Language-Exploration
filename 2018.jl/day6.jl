using DataStructures

function distance(p1, p2)
    return abs(p1[1] - p2[1]) + abs(p1[2] - p2[2])
end

function find_closest(p1, points)
    distances = [distance(p1, point) for point in points]

    if count(x == minimum(distances) for x in distances) > 1
        return -1
    else
        return findmin(distances)[2]
    end
end

function convex_hull(points)
    # Implements Andrew's monotone chain algorithm
    # Input: points - vector of tuples (x,y)
    # Ouput: the subset of points that define the convex hull

    # not enough points
    if length(points) <= 1
        return copy(points)
    end

    # sort the points by x and then by y
    points = sort(points)

    # function for calculating the cross product of vectors OA and OB
    cross(o, a, b) = (a[1] - o[1]) * (b[2] - o[2]) - (a[2] - o[2]) * (b[1] - o[1])

    # build lower hull
    lower = eltype(points)[]
    for p in points
        while length(lower) >= 2 && cross(lower[end-1], lower[end], p) <= 0
            pop!(lower)
        end
        push!(lower, p)
    end

    # build upper hull
    upper = eltype(points)[]
    for i in length(points):-1:1
        p = points[i]
        while length(upper) >= 2 && cross(upper[end-1], upper[end], p) <= 0
            pop!(upper)
        end
        push!(upper, p)
    end

    # concatenates lower hull to upper hull to obtain the convex hull
    vcat(lower[1:end-1], upper[1:end-1])
end

function main()
    points = [parse.(Int, split(line, ", ")) for line in readlines("input6.txt")]
    # sort by ascending x and then ascending y
    hull = Dict(findfirst(x -> x == point, points) => true for point in convex_hull(points))

    minx, maxx = extrema(point[1] for point in points)
    miny, maxy = extrema(point[2] for point in points)
    areas = zeros(Int, maxy - miny + 1, maxx - minx + 1)

    for x in minx:maxx
        for y in miny:maxy
            x_idx = x - minx + 1
            y_idx = y - miny + 1
            closest = find_closest([x, y], points)
            closest = haskey(hull, closest) ? -1 : closest
            areas[y_idx, x_idx] = closest
        end
    end

    println(sort(collect(counter(areas)), by=x -> x[2]))
end

main()