#include <iostream>
#include <string> 
#include <unordered_map>
#include <fstream>
#include <vector>
#include <utility>
#include <algorithm>
#include "simdjson.h"



extern "C" {
    void display_top_10_artists(const char* raw_filename) {
        
        simdjson::ondemand::parser parser;
        simdjson::padded_string json;

        auto error  = simdjson::padded_string::load(raw_filename).get(json);

        if (error) {
            std::cerr << "Error: Could not load " << raw_filename << raw_filename << " (" << error_message(error) << ")" << std::endl;
            return;
        }

        simdjson::ondemand::document doc;
        error = parser.iterate(json).get(doc);
        if (error) {
            std::cerr << "JSON parsing error: " << simdjson::error_message(error) << std::endl;
        }

        std::unordered_map<std::string, int> artist_counts;

        for (auto track : doc) {
            std::string_view artist_sv;

            if (track["artist"].get(artist_sv) == simdjson::SUCCESS) {
                if (!artist_sv.empty()) {
                    artist_counts[std::string(artist_sv)]++;
                }
            }
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