using CircularList

function main()
    current_marble = 1
    circle = circularlist(0)
    current_player = 1
    num_players = 459
    scores = Dict(i => 0 for i in 1:num_players)

    while current_marble <= 7210300
        if mod(current_marble, 23) == 0
            scores[current_player] += current_marble
            shift!(circle, 7, :backward)
            scores[current_player] += current(circle).data
            delete!(circle)
            forward!(circle)
        else
            forward!(circle)
            insert!(circle, current_marble)
        end
        current_marble += 1
        current_player = mod1(current_player + 1, num_players)
    end
    println(maximum(values(scores)))
end

main()