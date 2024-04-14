#ifndef __IO_HPP__
#define __IO_HPP__

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <variant>

// Quote a string and escape inner quotes
std::string quoted(std::string str) {
    size_t pos = str.find('"');
    while (pos != std::string::npos) {
        str.replace(pos, 1, "\\\""); // Escape internal quote with backslash
        pos = str.find('"', pos + 2); // Find next quote starting from the next character
    }
    return "\"" + str + "\"";
}

// Quote anything that can be converted to a string
template<typename T>
std::string quoted(T value) {
    std::string str = std::to_string(value);
    return quoted(str);
}

// Unquote a string
std::string unquote(std::string str) {
    // Remove leading and trailing double quotes if present
    if (str.size() >= 2 && str.front() == '"' && str.back() == '"') {
        str = str.substr(1, str.size() - 2);
    }

    // Find and replace escaped characters within double quotes
    size_t pos = str.find("\\\"");
    while (pos != std::string::npos) {
        str.replace(pos, 2, "\""); // Replace escaped quote with unescaped quote
        pos = str.find("\\\"", pos + 1); // Find next escaped quote starting from the next character
    }

    return str;
}

// Helper function to trim whitespace from both ends of a string
std::string trim(const std::string& str) {
    size_t first = str.find_first_not_of(' ');
    if (std::string::npos == first) {
        return str;
    }
    size_t last = str.find_last_not_of(' ');
    return str.substr(first, (last - first + 1));
}




// Recursive function to write Newick representation of the tree
template <typename Node, typename Leaf>
void write_tree_recursive(const RootedTree<Node, double, Leaf>& tree, std::ofstream& ofs) {
    // If it's a leaf, write its name
    if (tree.children.empty()) {
        ofs << quoted(tree.data);
    } else {
        // If it's a node, write its children recursively
        for (size_t i = 0; i < tree.children.size(); ++i) {

            if (i > 0) ofs << ",";
            if (std::holds_alternative<RootedTree<Node, double, Leaf>>(tree.children[i])) {
                const auto& subtree = std::get<RootedTree<Node, double, Leaf>>(tree.children[i]);
                ofs << "(";
                write_tree_recursive(subtree, ofs);
                ofs << ")";

                // Write node's name if it is defined (string of length greater than 0)
                std::string node_name = quoted(subtree.data);
                if(node_name.size() > 2){
                  ofs << node_name;
                }

            } else {
                const auto& leaf = std::get<Leaf>(tree.children[i]);
                ofs << quoted(leaf);
            }

            // Write edge length if greater than 0
            if((tree.edges.size() > i) && (tree.edges[i] > 0)){
              ofs << ":" << tree.edges[i];
            }
        }
    }
}


// Function to write tree to Newick file
template <typename Node, typename Leaf>
void write_tree(const RootedTree<Node, double, Leaf>& tree, const std::string& filename) {
    std::ofstream ofs(filename);
    if (ofs.is_open()) {
        write_tree_recursive(tree, ofs);
        ofs << ";" << std::endl; // End with semicolon
        ofs.close();
        std::cout << "Newick file written to " << filename << std::endl;
    } else {
        std::cerr << "Unable to open file " << filename << " for writing." << std::endl;
    }
}

void write_int_tree(const RootedTree<int, double, int>& tree, const std::string& filename) {
  write_tree(tree, filename);
}

void write_str_tree(const RootedTree<std::string, double, std::string>& tree, const std::string& filename) {
  write_tree(tree, filename);
}


// Parse a name and length string
// For example: 
//   "Unicorn":4.20
// Quotes are optional
// There may be spaces
void parse_name_and_length (const std::string& newick_str, size_t& pos, std::string& name, double& length){
   // Parse node or leaf name with optional branch length
   size_t end_pos = newick_str.find_first_of(",);", pos);
   std::string token = trim(newick_str.substr(pos, end_pos - pos));

   pos = end_pos;

   // Check if the token contains a branch length
   size_t colon_pos = token.find(':');
   if (colon_pos != std::string::npos) {
       length = std::stod(trim(token.substr(colon_pos + 1)));
       token = trim(token.substr(0, colon_pos));
   }
   name = unquote(token);
}


// Recursive function to parse Newick representation and construct the tree
RootedTree<std::string, double, std::string> parse_newick(const std::string& newick_str, size_t& pos) {
    RootedTree<std::string, double, std::string> tree;
    std::string token;
    char current_char;

    while (pos < newick_str.size()) {
        current_char = newick_str[pos];
        ++pos;

        if (current_char == '(') {
            tree.children.push_back(parse_newick(newick_str, pos));
        } else if (current_char == ')') {
            std::string name = "";
            double length = 0;
            parse_name_and_length(newick_str, pos, name, length);
            tree.data = name;
            tree.edges.push_back(length);
            return tree;
        } else if (current_char == ',') {
            continue;
        } else if (current_char == ';') {
            return tree;
        } else {
            std::string name = "";
            double length = 0;

            --pos;
            parse_name_and_length(newick_str, pos, name, length);

            tree.children.push_back(name);
            tree.edges.push_back(length);
        }
    }

    return tree;
}



// Function to read tree from Newick file
RootedTree<std::string, double, std::string> read_tree(const std::string& filename) {
    std::ifstream ifs(filename);
    if (!ifs.is_open()) {
        throw std::runtime_error("Failed to open file: " + filename);
    }

    std::stringstream buffer;
    buffer << ifs.rdbuf();
    std::string newick_str = buffer.str();

    size_t pos = 0;
    return parse_newick(newick_str, pos);
}

#endif
