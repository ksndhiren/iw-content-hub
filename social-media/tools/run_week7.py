"""Run all Week 7 generators sequentially."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wk7_d1_videointerview as d1
import wk7_d2_hiddenmarket as d2
import wk7_d3_starmethod as d3
import wk7_d4_followup as d4
import wk7_d5_burnout as d5

print("=== Week 7 - w/c 6th July 2026 ===")
d1.generate("campaigns/outputs/week7/d1-videointerview")
d2.generate("campaigns/outputs/week7/d2-hiddenmarket")
d3.generate("campaigns/outputs/week7/d3-starmethod")
d4.generate("campaigns/outputs/week7/d4-followup")
d5.generate("campaigns/outputs/week7/d5-burnout")
print("=== All Week 7 graphics done ===")
