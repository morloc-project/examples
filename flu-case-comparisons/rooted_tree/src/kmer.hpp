#ifndef __KMER_HPP__
#define __KMER_HPP__

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
double kmerDistance(const std::map<std::string,int>& x, const std::map<std::string,int>& y){
    double square_distance = 0.0;

    // Iterate through kmers in sequence x, find distance to y
    for (const auto& pair : x){
        std::string key = pair.first;
        int xcount = pair.second;
        int ycount = 0; 
        if(y.find(key) != y.end()){
            ycount = y.at(key); 
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
Eigen::Matrix<B, Eigen::Dynamic, Eigen::Dynamic> selfcmp(std::function<B(A, A)> f, std::vector<A> xs){
    int size = xs.size();

    Eigen::Matrix<B, Eigen::Dynamic, Eigen::Dynamic> mat(size, size);

    for (int i = 0; i < size; ++i) {
        for (int j = 0; j < size; ++j) {
            mat(i, j) = f(xs[i], xs[j]);
        }
    }

    return mat;
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

#endif
