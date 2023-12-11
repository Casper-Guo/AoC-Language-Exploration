function sum_metadata(tree, num_children, num_metadata)
    if num_children == 0
        # at the beginning of a leaf node
        return sum(tree[1:num_metadata]), tree[num_metadata+1:end]
    end

    tree_sum = 0
    for i in 1:num_children
        child_sum, tree = sum_metadata(tree[3:end], tree[1], tree[2])
        tree_sum += child_sum
    end
    return tree_sum + sum(tree[1:num_metadata]), tree[num_metadata+1:end]
end

function root_node(tree, num_children, num_metadata)
    if num_children == 0
        # at the beginning of a leaf node
        return sum(tree[1:num_metadata]), tree[num_metadata+1:end]
    end

    child_nodes = []
    for i in 1:num_children
        child_sum, tree = root_node(tree[3:end], tree[1], tree[2])
        push!(child_nodes, child_sum)
    end

    node_value = 0
    for i in tree[1:num_metadata]
        if i <= num_children && i != 0
            node_value += child_nodes[i]
        end
    end
    return node_value, tree[num_metadata+1:end]
end

function main()
    tree = map(x -> parse(Int, x), split(readline("input8.txt"), " "))
    println(sum_metadata(tree[3:end], tree[1], tree[2]))
    println(root_node(tree[3:end], tree[1], tree[2]))
end

main()