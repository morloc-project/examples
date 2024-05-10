#ifndef __PACK_HPP__
#define __PACK_HPP__

#include <utility>
#include <vector>
#include <variant>

template <typename Node, typename Edge, typename Leaf>
int rooted_count_nodes(const RootedTree<Node, Edge, Leaf> &tree) {
    
    int count = 1;
    for (const auto& child : tree.children) {
        if (std::holds_alternative<RootedTree<Node, Edge, Leaf>>(child)) {
            count += rooted_count_nodes(std::get<RootedTree<Node, Edge, Leaf>>(child));
        }
    }

    return count;
}


template <typename Node, typename Edge, typename Leaf>
std::tuple<std::vector<Node>, std::vector<std::tuple<int, int, Edge>>, std::vector<Leaf>>
unpack(const RootedTree<Node, Edge, Leaf> &tree)
{
    std::vector<Node> nodes;
    std::vector<Leaf> leafs;
    std::vector<std::tuple<int, int, Edge>> edges;

    int number_of_nodes = rooted_count_nodes(tree);

    unpack_r(tree, nodes, leafs, edges, number_of_nodes, 0);

    return {nodes, edges, leafs};
}


template <typename Node, typename Edge, typename Leaf>
void unpack_r(const RootedTree<Node, Edge, Leaf>& tree, std::vector<Node>& nodes,
                       std::vector<Leaf>& leafs, std::vector<std::tuple<int, int, Edge>>& edges, int number_of_nodes, int index)
{
    nodes.push_back(tree.data);
    for (size_t i = 0; i < tree.children.size(); i++){
        if (std::holds_alternative<RootedTree<Node, Edge, Leaf>>(tree.children[i])) {
            const auto& child_tree = std::get<RootedTree<Node, Edge, Leaf>>(tree.children[i]);
            edges.push_back(std::make_tuple(index, nodes.size(), tree.edges[i]));
            unpack_r(child_tree, nodes, leafs, edges, number_of_nodes, nodes.size());
        } else {
            leafs.push_back(std::get<Leaf>(tree.children[i]));
            edges.push_back(std::make_tuple(index, leafs.size() + number_of_nodes - 1, tree.edges[i]));
        }

    }
}


#endif
