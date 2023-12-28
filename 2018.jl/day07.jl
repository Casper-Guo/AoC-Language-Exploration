using DataStructures

@kwdef mutable struct Worker
    task::Char = ' '
    timer::Int = 0
    runtime::Int = 0
end

function map_dependencies(dependencies)
    # turn a list of dependent relations
    # into a map of step : required prior steps pairs
    dependency_map = Dict()
    for (prior, post) in dependencies
        if haskey(dependency_map, post)
            dependency_map[post][prior] = false
        else
            dependency_map[post] = Dict(prior => false)
        end

        if !haskey(dependency_map, prior)
            dependency_map[prior] = Dict()
        end
    end

    return dependency_map
end

function find_ready_steps(dependency_map)
    # find all steps that are ready to go
    steps = []
    for step in keys(dependency_map)
        if length(dependency_map[step]) == 0
            push!(steps, step)
        end
    end
    return steps
end

function update_dependencies(dependecy_map, step)
    for priors in values(dependecy_map)
        delete!(priors, step)
    end
end

function process_line(line)
    m = match(r"Step ([A-Z]).+([A-Z]).+", line)
    return map(x -> only(x), m.captures)
end

function main()
    lines = readlines("input07.txt")
    dependencies = [process_line(line) for line in lines]

    dependency_map = map_dependencies(dependencies)
    part1_map = deepcopy(dependency_map)

    # part 1
    step_queue = PriorityQueue()
    while length(part1_map) > 0 || length(step_queue) > 0
        ready_steps = find_ready_steps(part1_map)
        for step in ready_steps
            delete!(part1_map, step)
            step_queue[step] = Int(step)
        end
        next_step = dequeue!(step_queue)
        print(next_step)
        update_dependencies(part1_map, next_step)
    end
    println()

    # part 2
    num_workers = 5
    part2_map = deepcopy(dependency_map)
    workers = Worker[]

    for i in 1:num_workers
        push!(workers, Worker())
    end

    time = 0
    while length(part2_map) > 0 || length(step_queue) > 0
        for worker in workers
            if worker.timer != 0
                worker.timer -= 1
            end

            if worker.timer == 0
                # finish old task
                update_dependencies(part2_map, worker.task)
                # ready to accept new task
                ready_steps = find_ready_steps(part2_map)
                for step in ready_steps
                    delete!(part2_map, step)
                    step_queue[step] = Int(step)
                end
            end
        end

        for (idx, worker) in enumerate(workers)
            if worker.timer == 0
                if length(step_queue) != 0
                    worker.task = dequeue!(step_queue)
                    worker.timer = Int(worker.task) - 4
                    worker.runtime = time + worker.timer
                end
            end
        end
        time += 1
    end

    println([worker.runtime for worker in workers][1])
end

main()