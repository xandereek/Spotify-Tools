#include <iostream>
#include <string> 
#include <unordered_map>
#include <fstream>
#include <vector>
#include <utility>
#include <algorithm>
#include "json.hpp"

using json = nlohmann::json;

extern "C" {
    void display_top_10_artists(const char* raw_filename) {
        std::string filename = raw_filename;
        std::ifstream jsonFile(filename);

        if (!jsonFile.is_open()) {
            std::cerr << "Error: Could not open " << filename << std::endl;
            return;
        }

        json jsonData;

        try {
            jsonData = json::parse(jsonFile);
        } 
        catch (json::parse_error& e){
            std::cerr << "JSON parsing error: " << e.what() << std::endl;
            return;
        }

        std::unordered_map<std::string, int> artist_counts;

        for (const auto& track : jsonData) {
            if (!track.contains("artist") || track["artist"].is_null()) continue;

            std::string artist_name = track["artist"].get<std::string>();
            if (artist_name.empty()) continue;
            
            artist_counts[artist_name]++;
        }

        std::vector<std::pair<std::string, int>> sorted_artists(artist_counts.begin(), artist_counts.end());

        std::sort(sorted_artists.begin(), sorted_artists.end(), [](const auto& a, const auto& b){return a.second > b.second;});

        std::cout << "Top 10 artists:" << "\n";

        int limit = std::min(10, (int)sorted_artists.size());
        for (int i = 0; i < limit; ++i) {
            std::cout << i + 1 << ". " << sorted_artists[i].first << " - " << sorted_artists[i].second << " songs" << "\n";
        }
    }
}