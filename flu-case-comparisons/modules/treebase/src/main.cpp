#include <vector>
#include <string>
#include <functional>

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/eigen.h>
#include <pybind11/functional.h>

namespace py = pybind11;

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

// These include statements contain the same C++ functions that are
// used in the morloc case study
#include "kmer.hpp"
#include "tree.hpp"
#include "upgma.hpp"
#include "io.hpp"
#include "classify.hpp"
#include "pack.hpp"

RootedTree<int, double, int>
makeTree(int kmer_size, std::vector<std::string> seqs)
{
  return upgmaFromDist(makeDistMat(kmer_size, seqs));
}

PYBIND11_MODULE(treebase, m) {
    m.doc() = R"pbdoc(
        RootedTree library
    )pbdoc";

    m.def("countKmers", &countKmers, R"pbdoc(
        Count k-mers in a string
    )pbdoc");

    m.def("kmerDistance", &kmerDistance, R"pbdoc(
        Calculate a distance between two k-mer count sets
    )pbdoc");

    m.def("makeTree", &makeTree, R"pbdoc(
        Make a tree from a kmer length and list of sequences
    )pbdoc");

    m.def("makeDistMat", &makeDistMat, R"pbdoc(
        Make a distance matrix from a kmer length and list of sequences
    )pbdoc");


    // With pybind11, no generics can be used after compilation
    // So we need to enumerate every combination of parameters we intend to use
    m.def("writeTree", &write_tree<int,int>, R"pbdoc(
        Write a tree with integer leaves and nodes
    )pbdoc");

    m.def("writeTree", &write_tree<std::string,std::string>, R"pbdoc(
        Write a tree with string leaves and nodes
    )pbdoc");

    m.def("writeTree", &write_tree<std::string,int>, R"pbdoc(
        Write a tree with string leaves and integer nodes
    )pbdoc");
    m.def("writeTree", &write_tree<int,std::string>, R"pbdoc(
        Write a tree with string leaves and integer nodes
    )pbdoc");


    // All the same, for strings rather than files
    m.def("writeTreeStr", &write_tree_str<int,int>, R"pbdoc(
        Write a tree with integer leaves and nodes
    )pbdoc");

    m.def("writeTreeStr", &write_tree_str<std::string,std::string>, R"pbdoc(
        Write a tree with string leaves and nodes
    )pbdoc");

    m.def("writeTreeStr", &write_tree_str<std::string,int>, R"pbdoc(
        Write a tree with string leaves and integer nodes
    )pbdoc");
    m.def("writeTreeStr", &write_tree_str<int,std::string>, R"pbdoc(
        Write a tree with string leaves and integer nodes
    )pbdoc");



    m.def("classify", &classify<std::string>, R"pbdoc(
        Classify all leaves in a tree given presence of a few leaves
    )pbdoc");

    m.def("classify", &classify<int>, R"pbdoc(
        Classify all leaves in a tree given presence of a few leaves
    )pbdoc");

    m.def("readTree", &read_tree, R"pbdoc(
        Read a tree newick file with string leaves and nodes
    )pbdoc");

    m.def("readTreeStr", &read_tree_str, R"pbdoc(
        Read a tree newick string with string leaves and nodes
    )pbdoc");


    m.def("getLeafs", &get_leafs<std::string, double, std::string>, R"pbdoc(
        Get vector of leafs
    )pbdoc");

    m.def("getLeafs", &get_leafs<std::string, double, std::tuple<std::string,int>>, R"pbdoc(
        Get vector of leafs
    )pbdoc");

    m.def("mapLeaf", &mapLeaf<std::string, double, std::tuple<std::string, int>, std::string>, R"pbdoc(Map a function over the leaves)pbdoc");
    m.def("mapLeaf", &mapLeaf<std::string, double, std::string, int>, R"pbdoc(Map a function over the leaves)pbdoc");
    m.def("mapLeaf", &mapLeaf<int, double, int, std::string>, R"pbdoc(Map a function over the leaves)pbdoc");

    m.def(
        "unpack",
        &unpack<std::string, double, std::string>,
        R"pbdoc(Represent a tree as a tuple of node names, edges lengths, and leaf names)pbdoc");

    py::class_<RootedTree<int, double, int>>(m, "RootedTreeIFI");
    py::class_<RootedTree<int, double, std::string>>(m, "RootedTreeIFS");
    py::class_<RootedTree<std::string, double, int>>(m, "RootedTreeSFI");
    py::class_<RootedTree<std::string, double, std::string>>(m, "RootedTreeSFS");
    py::class_<RootedTree<std::string, double, std::tuple<std::string,int>>>(m, "RootedTreeSFP");

#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "0.1.0";
#endif
}
