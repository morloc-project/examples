#ifndef __TREE_HPP__
#define __TREE_HPP__

// from mlcmoroctypes header file
template <typename Node, typename Edge, typename Leaf>
struct RootedTree {
    Node data;
    std::vector<std::variant<RootedTree<Node, Edge, Leaf>, Leaf>> children;
    std::vector<Edge> edges;
};

#endif
