#include <iostream>
#include <fstream>
#include <string>
#include <thread>
#include <chrono>

using namespace std;

void run_task(int id, double speed) {
    cout << "[TASK " << id << "] Initializing Substrate..." << endl;
    for(int i=0; i<=100; i+=25) {
        this_thread::sleep_for(chrono::milliseconds((int)(500 / speed)));
        cout << "  > Progress: " << i << "%" << (speed > 2.0 ? " [TURBO]" : " [LOCKED]") << endl;
    }
}

int main() {
    ifstream license("pro_mode.txt");
    string key;
    bool is_pro = false;

    if (license.is_open()) {
        getline(license, key);
        if (key == "GHOST_SECURE_5592_X") is_pro = true;
    }

    cout << "============================================" << endl;
    cout << "   GHOSTSEMI VIRTUAL SILICON ENGINE v1.5" << endl;
    cout << "      Architecture: Software-Defined  " << endl;
    cout << "============================================" << endl;

    auto start = chrono::high_resolution_clock::now();

    if (is_pro) {
        cout << ">> STATUS: PRO LICENSE VERIFIED" << endl;
        cout << ">> MODE: BATCH PROCESSING (5 TASKS)" << endl;
        for(int i=1; i<=5; i++) run_task(i, 4.2);
    } else {
        cout << ">> STATUS: EVALUATION MODE (LOCKED)" << endl;
        cout << ">> ALERT: Visit your dashboard to unlock Turbo." << endl;
        run_task(1, 1.8);
    }

    auto end = chrono::high_resolution_clock::now();
    chrono::duration<double> elapsed = end - start;

    // Telemetry Logging
    ofstream stats("stats.ghost");
    stats << "--- GHOSTSEMI PERFORMANCE REPORT ---" << endl;
    stats << "ENGINE_VERSION: 1.5" << endl;
    stats << "LICENSE: " << (is_pro ? "PRO_TURBO" : "EVAL_LOCKED") << endl;
    stats << "TASKS_COMPLETED: " << (is_pro ? 5 : 1) << endl;
    stats << "TOTAL_EXECUTION_TIME: " << elapsed.count() << "s" << endl;
    stats.close();

    cout << "TOTAL TIME: " << elapsed.count() << " seconds" << endl;
    cout << "GHOSTSEMI CORE SHUTDOWN COMPLETE." << endl;
    cout << "============================================" << endl;

    return 0;
}