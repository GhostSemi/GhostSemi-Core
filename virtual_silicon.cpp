#include <iostream>
#include <fstream>
#include <string>
#include <thread>
#include <chrono>

using namespace std;

// Updated Task Logic with real-time Turbo feedback
void run_task(int id, double speed) {
    bool is_turbo = (speed >= 4.0);
    cout << "[TASK " << id << "] Initializing Substrate..." << endl;
    for(int i=0; i<=100; i+=25) {
        // Higher speed (4.2) = shorter sleep (faster execution)
        this_thread::sleep_for(chrono::milliseconds((int)(500 / speed)));
        cout << "  > Progress: " << i << "%" << (is_turbo ? " [TURBO: 4.2GHz]" : " [LOCKED: 1.8GHz]") << endl;
    }
}

int main() {
    // 1. Check for Pro License
    ifstream license("pro_mode.txt");
    // 2. Check for Alpha Trial (New Feature for v2.6)
    ifstream trial("trial_mode.txt");
    
    string key;
    bool is_pro = false;
    bool is_trial = false;

    // Check Pro Key
    if (license.is_open()) {
        getline(license, key);
        if (key == "GHOST_SECURE_5592_X") {
            is_pro = true;
        }
        license.close();
    }

    // Check Trial Status
    if (trial.is_open()) {
        is_trial = true;
        trial.close();
    }

    cout << "============================================" << endl;
    cout << "   GHOSTSEMI VIRTUAL SILICON ENGINE v2.6" << endl;
    cout << "      Architecture: Software-Defined      " << endl;
    cout << "        Stable Build: X64 [STABLE]        " << endl;
    cout << "============================================" << endl;

    auto start = chrono::high_resolution_clock::now();

    if (is_pro) {
        cout << ">> STATUS: PRO LICENSE VERIFIED [ACTIVE]" << endl;
        cout << ">> MODE: BATCH PROCESSING (5 TASKS @ 4.2GHz)" << endl;
        for(int i = 1; i <= 5; i++) {
            run_task(i, 4.2);
        }
    } 
    else if (is_trial) {
        cout << ">> STATUS: ALPHA TRIAL ACTIVE (24H LIMIT)" << endl;
        cout << ">> MODE: TURBO ENABLED (1 TASK @ 4.2GHz)" << endl;
        run_task(1, 4.2); 
    }
    else {
        cout << ">> STATUS: EVALUATION MODE (LOCKED)" << endl;
        cout << ">> MODE: SINGLE TASK ONLY (1.8GHz)" << endl;
        cout << ">> ALERT: Verify License to unlock Turbo." << endl;
        run_task(1, 1.8);
    }

    auto end = chrono::high_resolution_clock::now();
    chrono::duration<double> elapsed = end - start;

    // Save Performance Telemetry
    ofstream stats("stats.ghost");
    stats << "--- GHOSTSEMI PERFORMANCE REPORT ---" << endl;
    stats << "ENGINE_VERSION: 2.6-STABLE" << endl;
    stats << "LICENSE_TYPE: " << (is_pro ? "PRO_TURBO" : (is_trial ? "TRIAL_TURBO" : "EVAL_LOCKED")) << endl;
    stats << "TASKS_COMPLETED: " << (is_pro ? 5 : 1) << endl;
    stats << "TOTAL_EXECUTION_TIME: " << elapsed.count() << "s" << endl;
    stats << "STATUS: ALL_SYSTEMS_OPTIMAL" << endl;
    stats.close();

    cout << "\nTOTAL EXECUTION TIME: " << elapsed.count() << " seconds" << endl;
    cout << "GHOSTSEMI CORE SHUTDOWN COMPLETE." << endl;
    cout << "============================================" << endl;

    return 0;
}