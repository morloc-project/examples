#ifndef __TREE_HPP__
#define __TREE_HPP__

#include <utility>
#include <vector>
#include <variant>
#include <iostream>


// from mlcmoroctypes header file
template <typename Node, typename Edge, typename Leaf>
struct RootedTree {
    Node data;
    std::vector<std::variant<RootedTree<Node, Edge, Leaf>, Leaf>> children;
    std::vector<Edge> edges;
};

template <class A, class B>
std::vector<B>
map(std::function<B(A)> f, std::vector<A> xs)
{
    std::vector<B> ys(xs.size());
    std::transform(xs.begin(), xs.end(), ys.begin(), f);
    return ys;
}

template<typename A>
A
id(A x)
{
  return x;
}

template <class A, class B>
B
snd(std::tuple<A,B> x)
{
  return(std::get<1>(x));
}

template <class A, class B>
A
fst(std::tuple<A,B> x)
{
  return(std::get<0>(x));
}
 


template <typename Node, typename Edge, typename Leaf, typename NewLeaf>
RootedTree<Node, Edge, NewLeaf>
mapLeaf(
    std::function<NewLeaf(Leaf)> func, 
    RootedTree<Node, Edge, Leaf> tree
) {
    RootedTree<Node, Edge, NewLeaf> newRootedTree;
    newRootedTree.data = tree.data;
    newRootedTree.edges = tree.edges;

    for (const auto& child : tree.children) {
        if (std::holds_alternative<Leaf>(child)) {
            // It's a leaf. Apply the function to it and add it to newRootedTree.
            Leaf oldLeaf = std::get<Leaf>(child);
            NewLeaf newLeaf = func(oldLeaf);
            newRootedTree.children.push_back(newLeaf);
        }
        else if (std::holds_alternative<RootedTree<Node, Edge, Leaf>>(child)) {
            // It's a tree. Recursively call mapLeafs on it and add it to newRootedTree.
            const RootedTree<Node, Edge, Leaf>& oldSubtree = std::get<RootedTree<Node, Edge, Leaf>>(child);
            RootedTree<Node, Edge, NewLeaf> newSubtree = mapLeaf(func, oldSubtree);
            newRootedTree.children.push_back(newSubtree);
        }
    }

    return newRootedTree;
}



// push :: (n -> n')
//      -> (n' -> e -> n -> (e', n'))
//      -> (n' -> e -> l -> (e', l'))
//      -> RootedTree n e l
//      -> RootedTree n' e' l'
template<typename Node, typename Edge, typename Leaf, typename NodePrime, typename EdgePrime, typename LeafPrime>
RootedTree<NodePrime, EdgePrime, LeafPrime>
push(
    std::function<NodePrime(Node)> handleRoot,
    std::function<std::tuple<EdgePrime, NodePrime>(NodePrime, Edge, Node)> alterChildNode,
    std::function<std::tuple<EdgePrime, LeafPrime>(NodePrime, Edge, Leaf)> alterLeaf,
    RootedTree<Node, Edge, Leaf> oldRoot
) {
    NodePrime newRootNode = handleRoot(oldRoot.data);
    return push_r(alterChildNode, alterLeaf, newRootNode, oldRoot);
}

// push_r :: (n' -> e -> n -> (e', n'))
//        -> (n' -> e -> l -> (e', l'))
//        -> n'
//        -> RootedTree n e l
//        -> RootedTree n' e' l'
template<typename Node, typename Edge, typename Leaf, typename NodePrime, typename EdgePrime, typename LeafPrime>
RootedTree<NodePrime, EdgePrime, LeafPrime>
push_r(
    std::function<std::tuple<EdgePrime, NodePrime>(NodePrime, Edge, Node)> alterChildNode,
    std::function<std::tuple<EdgePrime, LeafPrime>(NodePrime, Edge, Leaf)> alterLeaf,
    NodePrime newNode,
    RootedTree<Node, Edge, Leaf> oldTree
) {
    RootedTree<NodePrime, EdgePrime, LeafPrime> newTree;
    newTree.data = newNode;
    for(std::size_t i = 0; i < oldTree.children.size(); i++){
        auto child = oldTree.children[i];
        auto edge = oldTree.edges[i];
        if (std::holds_alternative<Leaf>(child)) {
            Leaf oldLeaf = std::get<Leaf>(child);
            auto newEdgeAndLeaf = alterLeaf(newNode, edge, oldLeaf);
            newTree.edges.push_back(std::get<0>(newEdgeAndLeaf));
            newTree.children.push_back(std::get<1>(newEdgeAndLeaf));
        }
        else if (std::holds_alternative<RootedTree<Node, Edge, Leaf>>(child)) {
            RootedTree<Node, Edge, Leaf> oldSubtree = std::get<RootedTree<Node, Edge, Leaf>>(child);
            auto newEdgeAndNode = alterChildNode(newNode, edge, oldSubtree.data);
            RootedTree<NodePrime, EdgePrime, LeafPrime> newSubtree = push_r(alterChildNode, alterLeaf, std::get<1>(newEdgeAndNode), oldSubtree);
            newTree.edges.push_back(std::get<0>(newEdgeAndNode));
            newTree.children.push_back(newSubtree);
        }
    }
    return newTree;
}



// pull :: (l -> n')
//      -> (n -> e -> n' -> e')
//      -> (n -> [(e', n')] -> n')
//      -> RootedTree n e l
//      -> RootedTree n' e' l
template<typename Leaf, typename NodePrime, typename Node, typename Edge, typename EdgePrime>
RootedTree<NodePrime, EdgePrime, Leaf>
pull(
    std::function<NodePrime(Leaf)> handleLeaf,
    std::function<EdgePrime(Node, Edge, NodePrime)> updateEdge,
    std::function<NodePrime(Node, std::vector<std::tuple<EdgePrime, NodePrime>>)> updateNode,
    RootedTree<Node, Edge, Leaf> initialTree
) {
    RootedTree<NodePrime, EdgePrime, Leaf> newTree;
    std::vector<std::tuple<Edge, NodePrime>> links;
    for (std::size_t i = 0; i < initialTree.children.size(); i++){
        auto child = initialTree.children[i];
        auto edge = initialTree.edges[i];
        if (std::holds_alternative<Leaf>(child)) {
            // It's a leaf. Do not change the leaf, keep it in the new tree.
            // But from the leaf, synthesize a node value that will be
            // used to synthesize parent nodes.
            Leaf oldLeaf = std::get<Leaf>(child);
            NodePrime synthesizedNode = handleLeaf(oldLeaf);
            newTree.children.push_back(oldLeaf);
            links.push_back(std::make_tuple(edge, synthesizedNode));
        }
        else if (std::holds_alternative<RootedTree<Node, Edge, Leaf>>(child)) {
            // It's a tree. Recursively call pull on it and add it to newTree.
            RootedTree<Node, Edge, Leaf> oldSubtree = std::get<RootedTree<Node, Edge, Leaf>>(child);
            RootedTree<NodePrime, EdgePrime, Leaf> newSubtree = pull(handleLeaf, updateEdge, updateNode, oldSubtree);
            newTree.children.push_back(newSubtree);
            links.push_back(std::make_tuple(edge, newSubtree.data));
        }
        else {
        }
    }

    std::vector<std::tuple<EdgePrime, NodePrime>> updatedLinks;
    for (auto link : links){
        // synthesize new edge
        EdgePrime newEdge = updateEdge(initialTree.data, std::get<0>(link), std::get<1>(link));
        newTree.edges.push_back(newEdge);
        // add element to [(e', n')] vector
        updatedLinks.push_back(std::make_tuple(newEdge, std::get<1>(link)));
    }

    // synthesize new node from original node and [(e', n')] vector
    newTree.data = updateNode(initialTree.data, updatedLinks);
    return newTree;
}


// -- pull values from leaf to root
// pullNode :: (l -> n') -> ([n'] -> n') -> RootedTree n e l -> RootedTree n' e l
// pullNode f g = pull
//     (\l -> f l) -- generate n' using f
//     (\n e n' -> e) -- do not change the edge
//     (\n es -> g (map snd es)) -- create new node from child nodes, ignore the current node value
template<typename Node, typename Edge, typename Leaf, typename NodePrime>
RootedTree<NodePrime,Edge,Leaf>
pullNode(
  std::function<NodePrime(Leaf)> f,
  std::function<NodePrime(std::vector<NodePrime>)> g,
  RootedTree<Node,Edge,Leaf> tree
) {
  auto handleLeaf = [f](Leaf l) { return f(l); }; 
  auto updateEdge = [](Node n, Edge e, NodePrime n2) { return e; };
  auto updateNode = [g](auto x, auto xs)
    { return g(
        map<std::tuple<Edge,NodePrime>, NodePrime>(
          snd<Edge,NodePrime>, xs));
    };

  return pull<Leaf,NodePrime,Node,Edge,Edge>(handleLeaf, updateEdge, updateNode, tree);
}

#endif
