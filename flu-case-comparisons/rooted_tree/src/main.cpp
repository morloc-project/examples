#ifndef __MAIN_HPP__
#define __MAIN_HPP__

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

RootedTree<int, double, int>
makeTree(int kmer_size, std::vector<std::string> seqs){
  return upgmaFromDist(makeDistMat(kmer_size, seqs));
}

PYBIND11_MODULE(rooted_tree, m) {
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

    py::class_<RootedTree<int, double, int>>(m, "RootedTreeIFI");

#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "0.1.0";
#endif
}


#endif
