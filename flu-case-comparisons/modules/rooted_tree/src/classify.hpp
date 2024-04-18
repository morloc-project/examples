#ifndef __CLASSIFY_HPP__
#define __CLASSIFY_HPP__

#include "tree.hpp"


std::tuple<double,std::string>
passClade(std::string parent, double edge, std::string child)
{
  std::string newNode;
  if(child.size() == 0){
    newNode = parent;
  } else {
    newNode = child;
  }
  return std::make_tuple(edge, newNode);
}

std::tuple<std::string,int>
reset_leaf(std::vector<std::string> refmap, int index)
{
  return std::make_tuple(refmap[index], index);
}

// add clade information from reference table to the tree leaves
RootedTree<std::string, double, std::tuple<std::string,int>>
assign_reference_clades(std::vector<std::string> refmap, RootedTree<std::string, double, int> tree)
{
  auto reset_leaf_app = std::bind(reset_leaf, refmap, std::placeholders::_1);
  return mapLeaf<std::string,double,int,std::tuple<std::string,int>>(reset_leaf_app, tree);
}


// set the child clade to the parent clade
// : setLeaf p e (l, i) = (e, (p, i))
std::tuple<double,std::tuple<std::string,int>>
setLeaf(std::string parent, double edge, std::tuple<std::string,int> leaf)
{
  return std::make_tuple(edge, std::make_tuple(parent, std::get<1>(leaf)));
}

// set parent clade based on child clades
std::string
pullClade(std::vector<std::string> xs)
{
  std::string clade = "";
  for (size_t i = 0; i < xs.size(); i++){
    if (xs[i].size() > 0){
      if(xs[i] == clade){
        // Another child is in the same clade as the first classified child.
        // This is consistent with the currently assigned parent clade.
        continue;
      } else if (clade == "") {
        // This is the first classified child, so for now set the parent clade
        // to match the child.
        clade = xs[i];
      } else {
        // The children have multiple clades, so the parent's clade is
        // undefined.
        clade = "";
        break;
      }
    }
  }
  return clade;
}

// Classify clades across a tree given clades for a subset of leaf taxa
//
// Each leaf has the type `(string, int)`, where the first element is the
// clade (empty string if no clade is given) and the second element is the
// index that may be used to access the sequence and metadata stored in an
// external table.
RootedTree<std::string, double, std::tuple<std::string,int>>
classify(std::vector<std::string> refmap, RootedTree<std::string, double, int> tree)
{
  auto tree1 = assign_reference_clades(refmap, tree);

  auto tree2 = pullNode<std::string, double, std::tuple<std::string,int>, std::string>(
      fst<std::string,int>,
      pullClade,
      tree1
  );

  auto tree3 = push<std::string, double, std::tuple<std::string, int>, std::string, double, std::tuple<std::string, int>>(
      id<std::string>,
      passClade,
      setLeaf,
      tree2
  );

  return tree3;
}

#endif
