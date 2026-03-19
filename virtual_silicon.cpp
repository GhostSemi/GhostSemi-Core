#include <iostream>
#include <fstream>
#include <string>
#include <chrono>
#include <thread>

using namespace std;

int main() {
    cout << "--- GHOSTSEMI VIRTUAL SILICON ENGINE v1.1 ---" << endl;
    
    // Check for the Pro License Flag created by Python
    ifstream licenseFile("pro_mode.txt");
    bool isPro = licenseFile.good();

    if (isPro) {
        cout << "[SYSTEM] PRO LICENSE DETECTED. UNLOCKING TURBO FREQUENCY..." << endl;
        cout << "[SYSTEM] CLOCKS: 4.2 GHz | CORES: ALL ACTIVE" << endl;
    } else {
        cout << "[SYSTEM] EVALUATION MODE. CLOCKS LOCKED AT 1.8 GHz." << endl;
        cout << "[SYSTEM] VISIT GHOSTSEMI.IO TO UPGRADE." << endl;
    }

    // Simulated Processing Loop
    for(int i = 0; i <= 100; i += 10) {
        cout << "Processing Substrate... " << i << "%" << endl;
        // Pro mode processes 3x faster
        int delay = isPro ? 100 : 300; 
        this_thread::sleep_for(chrono::milliseconds(delay));
    }

    cout << "\n[SUCCESS] Computation Complete." << endl;
    return 0;
}