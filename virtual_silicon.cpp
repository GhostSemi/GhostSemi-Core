#include <iostream>
#include <fstream>
#include <chrono>

using namespace std;

int main() {
    // 1. Performance Test
    auto start = chrono::high_resolution_clock::now();
    long long count = 0;
    for(int i=0; i<50000000; i++) { count += (i ^ 0x55); }
    auto end = chrono::high_resolution_clock::now();
    
    double elapsed = chrono::duration<double>(end - start).count();
    double mips = (50.0 / elapsed); // Simple MIPS calculation

    // 2. FORCE WRITE TO FILE
    // We use a full path or simple name to ensure it lands in the GhostSemi folder
    ofstream outfile("stats.ghost", ios::trunc); 
    if (outfile.is_open()) {
        outfile << mips;
        outfile.close();
        cout << "SUCCESS: Telemetry written to stats.ghost" << endl;
        cout << "GHOST_SIGNAL: " << mips << " MIPS" << endl;
    } else {
        cout << "ERROR: Could not create telemetry file!" << endl;
    }

    return 0;
}