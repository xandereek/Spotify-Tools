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
    std::unordered_map<std::string, std::vector<std::string>> artist_to_tracks;

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

    int skipped_tracks_count = 0;

    for (const auto& track : jsonData) {
        if (!track.contains("artist") || track["artist"].is_null()) {
            continue;
        }
        std::string artist_name = track["artist"].get<std::string>();
        std::string track_name = track["track"].get<std::string>();

        if (artist_name.empty()) {
            skipped_tracks_count++;
            continue;
        }

        artist_counts[artist_name] ++;
        artist_to_tracks[artist_name].push_back(track_name);
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

    if (skipped_tracks_count > 0) {
        std::cout << "\nNote: Skipped " << skipped_tracks_count << " tracks due to missing artist data." << std::endl;
    }

    std::string user_input;
    while(true) {
        std::cout << "\n> Enter a number (1-10) to see an artist's tracks (or type 'quit' to exit): " << std::endl;
        std::cout.flush();
        std::getline(std::cin, user_input);

        if (user_input == "quit") {
            break;
        }
        int choice = 0;
        try {
            choice = std::stoi(user_input);
        } catch (const std::invalid_argument& e){
            std::cout << "Invalid input. Please enter a number or 'quit'." << std::endl;
        }

        if (choice >= 1 && choice <= limit) {
            std::string chosen_artist = sorted_artists[choice - 1].first;
            std::cout << "\n Tracks by " << chosen_artist << ":" <<std::endl;

            for (const auto& track_title: artist_to_tracks.at(chosen_artist)) {
                std::cout << "- " << track_title << std::endl;
            }
        } else {
            std::cout << "Invalid number. Please enter a number between 1 and " << limit << "." << std::endl;
        }
    }
    return 0;
}