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


// adapted from morloc bio.algo module
std::map<std::string,int> countKmers(int k, std::string seq){
    std::map<std::string,int> kmers;
   
    if(k <= 0){
        throw std::invalid_argument("k must be an integer greater than or equal to 1");
    }

    for(int i = 0; (i + k) <= seq.size(); i++){
        std::string kmer = seq.substr(i, k);
        if(kmers.find(kmer) != kmers.end()){
            kmers[kmer]++;
        } else {
            kmers[kmer] = 1;
        }
    }

    return kmers;
}



// adapted from morloc bio.algo module
double kmerDistance(std::map<std::string,int> x, std::map<std::string,int> y){
    double square_distance = 0.0;

    // Iterate through kmers in sequence x, find distance to y
    for (const auto& pair : x){
        std::string key = pair.first;
        int xcount = pair.second;
        int ycount = 0; 
        if(y.find(key) != y.end()){
            ycount = y[key]; 
        }
        square_distance += (xcount - ycount) * (xcount - ycount) / (xcount + ycount);
    }

    // Iterate through kmers in y, if they are missing from x, then they would
    // not have been accounted for in the prior loop, and the distance is simply
    // y^2
    for (const auto& pair : y){
        std::string key = pair.first;
        int ycount = pair.second;
        if(x.find(key) == x.end()){
            square_distance += ycount * ycount;
        }
    }

    return std::sqrt(square_distance);
}



// adapted from morloc matrix module
template <typename A, typename B>
Eigen::Matrix<B, Eigen::Dynamic, Eigen::Dynamic> selfcmp(std::function<B(A,A)> f, std::vector<A> xs){
    int size = xs.size();

    Eigen::Matrix<B, Eigen::Dynamic, Eigen::Dynamic> mat(size, size);

    for (int i = 0; i < size; ++i) {
        for (int j = 0; j < size; ++j) {
            mat(i, j) = f(xs[i], xs[j]);
        }
    }

    return mat;
}



// from mlcmoroctypes header file
template <typename Node, typename Edge, typename Leaf>
struct RootedTree {
    Node data;
    std::vector<std::variant<RootedTree<Node, Edge, Leaf>, Leaf>> children;
    std::vector<Edge> edges;
};



// internal struct used in tree building
// adapted from morloc bio.tree module
typedef struct Edge{
  int child;
  double dist;
} Edge;



// adapted from morloc bio.tree module
RootedTree<int, double, int> edge_map_to_tree(int root, std::vector<std::vector<Edge>> edges){
    RootedTree<int, double, int> tree;

    for(int i = 0; i < edges[root].size(); i++){
        tree.edges.push_back(edges[root][i].dist);
        int childIndex = edges[root][i].child;

        if(edges[childIndex].size() == 0){
          // child is a leaf
          tree.children.push_back(childIndex);
        } else {
          // child is a subtree
          RootedTree<int, double, int> childTree = edge_map_to_tree(childIndex, edges);
          tree.children.push_back(childTree); 
        }
    }

    return tree;
}



// adapted from morloc bio.tree module
// upgmaFromDist :: Matrix Real -> RootedTree () Real Int This is a naive cubic
// time algorithm. Quadratic time algorithms are possible, this implementation
// just serves as a baseline.
RootedTree<int, double, int> upgmaFromDist(
  Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic> mat
){

    int Nleafs = mat.cols();
    int Nnodes = 0;

    std::vector<std::vector<Edge>> edges(Nleafs * 2 - 1);
    std::vector<double> sizes(Nleafs * 2 - 1, 0);

    // initialize the indices to the leafs
    //
    // as vertices are paired, indices will either be mapped to -1 or mapped to
    // internal node indices
    //
    // matrix indices map into the `indices` vector to find the tree indices
    std::vector<int> indices(Nleafs);
    for(int i = 0; i < indices.size(); i++){
      indices[i] = i;
      sizes[i] = 1; // the size of each leaf is 1
    }

    // Maximum distance between any two points
    double globalMax = mat.maxCoeff();

    int root = -1;
    bool not_done = true;
    while(not_done){
      not_done = false;
      double min_dist = globalMax;
      int min_i = 0;
      int min_j = 0;

      // Find closest pair of taxa
      for(int row_id = 0; row_id < Nleafs; row_id++){
        // if the index was already used, it would have been set to -1, which
        // means it should be skipped
        if(indices[row_id] >= 0){
          for(int col_id = 0; col_id < row_id; col_id++){
            // likewise for j
            if(indices[col_id] >= 0){
              // we've reached a pair of indices that have not been used
              not_done = true;
              double ij_dist = mat(row_id, col_id);
              if(ij_dist < min_dist){
                min_dist = ij_dist;
                min_i = row_id;
                min_j = col_id;
              }
            }
          }
        }
      }

      if(not_done){
        Nnodes++;
        int parent = Nnodes + Nleafs - 1;

        Edge left;
        left.child = indices[min_i];
        left.dist = min_dist / 2;

        Edge right;
        right.child = indices[min_j];
        right.dist = min_dist / 2;

        edges[parent].push_back(left);
        edges[parent].push_back(right);

        int ni = sizes[indices[min_i]];
        int nj = sizes[indices[min_j]];
        sizes[parent] = ni + nj;

        //      j
        //      |
        //    01234567             01834567
        //   1 0                  1 0
        //   2 -0                 8 +0
        //   3  |0                3  +*
        // i-4**m*0     [1 / 9]   4*****
        //   5  |* 0              5  +* 0
        //   6  |*  0             6  +*  0
        //   7  |*   0            7  +*   0
        int new_node = min_j; // to save space, we will reuse the min_j'th col
        for(int col_id = 0; col_id < min_j; col_id++){
          if(indices[col_id] >= 0){
            mat(new_node,col_id) = (mat(min_j,col_id) * nj + mat(min_i,col_id) * ni) / (nj + ni);
          }
        }
        for(int row_id = min_j + 1; row_id < Nleafs; row_id++){
          if(indices[row_id] >= 0){
            mat(row_id,new_node) = (mat(row_id,min_j) * nj + mat(min_i,row_id) * ni) / (nj + ni);
          }
        }

        // at the end of the loop this will be the root of the tree
        root = parent;

        indices[min_j] = parent;
        indices[min_i] = -1; // this row will no longer be used
      }
    }

    RootedTree<int, double, int> finalTree = edge_map_to_tree(root, edges);

    return finalTree;
}



Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic>
makeDistMat(int kmer_size, std::vector<std::string> seqs){
  std::vector<std::map<std::string,int>> kmermaps;
  for (size_t i = 0; i < seqs.size(); i++){
    std::map<std::string,int> kmermap = countKmers(kmer_size, seqs[i]);
    kmermaps.push_back(kmermap);
  }
  // selfcmp is a generic function, writing it otherwise is awkward
  // but I cannot use generic functions through the FFI without writing a
  // type-specific instance, which is also awkward.
  Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic> mat = selfcmp(std::function<double(std::map<std::string,int>, std::map<std::string,int>)>(kmerDistance), kmermaps);
  return mat;
}



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
