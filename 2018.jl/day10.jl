using Plots

function process_line(line)
    m = match(r"position=<(.+), (.+)> velocity=<(.+), (.+)>", line)
    return map(x -> parse(Int, x), m.captures)
end

function main()
    lines = readlines("input10.txt")
    points = [process_line(line) for line in lines]
    pos = [[point[1] for point in points] [point[2] for point in points]]
    velocity = [[point[3] for point in points] [point[4] for point in points]]

    # selected by bounding box size
    for i in 1:10900
        pos .+= velocity
    end

    anim = @animate for i = 1:10
        pos .+= velocity
        scatter(pos[:, 1], [-y for y in pos[:, 2]], # flipped y coordinates
            xlims=(120, 200),
            ylims=(-220, -180),
            title="frame $i",
            legend=false)
    end
    gif(anim, "Day10_anim.gif", fps=1)
end

main()