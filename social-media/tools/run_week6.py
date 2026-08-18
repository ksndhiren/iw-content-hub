"""Run all Week 6 generators in sequence."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import wk6_d1_salary
import wk6_d2_networking
import wk6_d3_personalstatement
import wk6_d4_referral
import wk6_d5_firstdays

BASE_OUT = "campaigns/outputs/week6"

def run():
    print("=== Week 6 — w/c 29th June ===\n")
    wk6_d1_salary.generate(f"{BASE_OUT}/d1-salary")
    wk6_d2_networking.generate(f"{BASE_OUT}/d2-networking")
    wk6_d3_personalstatement.generate(f"{BASE_OUT}/d3-personalstatement")
    wk6_d4_referral.generate(f"{BASE_OUT}/d4-referral")
    wk6_d5_firstdays.generate(f"{BASE_OUT}/d5-firstdays")
    print("\n=== All Week 6 graphics done ===")

if __name__ == "__main__":
    run()
