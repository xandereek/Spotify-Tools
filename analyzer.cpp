#include <iostream>
#include <string>
#include <unordered_map>
#include <fstream>
#include <vector>
#include <utility>
#include <algorithm>
#include "json.hpp"

using json = nlohmann::json;

int main(int argc, char* argv[]) {
    std::unordered_map<std::string, int> artist_counts;

    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " <filename.json>" << std::endl;
    return 1;
    }

    std::string filename = argv[1];
    std::ifstream jsonFile(filename);

    if (!jsonFile.is_open()) {
        std::cerr << "Error: Could not open .json" << std::endl;
        return 1;
    }

    json jsonData;

    try {
        jsonData = json::parse(jsonFile);
    }
    catch (json::parse_error& e) {
        std::cerr << "JSON parsing error: " << e.what() << std::endl;
        return 1;
    }

    for (const auto& track : jsonData) {
        if (!track.contains("artist") || track["artist"].is_null()) {
            continue;
        }
        std::string artist_name = track["artist"].get<std::string>();

        if (artist_name.empty()) {
            continue;
        }

        artist_counts[artist_name] ++;
    }
    std::vector<std::pair<std::string, int>> sorted_artists(artist_counts.begin(), artist_counts.end());

    std::sort(sorted_artists.begin(), sorted_artists.end(), [](const auto& a, const auto& b){
        return a.second > b.second;
    });

    std::cout << "Top 10 Artists:" << std::endl;

    int limit = std::min(10, (int)sorted_artists.size());
    
    for (int i = 0; i < limit; i++) {
        std::cout << i + 1 << ". " << sorted_artists[i].first << "(" << sorted_artists[i].second << " songs)" << std::endl;
    }
}