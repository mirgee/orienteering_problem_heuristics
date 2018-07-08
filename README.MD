# Arc Orienteering Problem metaheuristics

During my project of applying counterfactual regret minimization technique for finding epsilon Nash equilibria to the domain of Protection Assistant for 
Wildlife Seurity (PAWS), I came across the need of fast heuristic for solving (Arc) Orienteering Problem. I adapted Tsiligirides' 
 and  Greedy Adaptive Search Procedure (GRASP) algorithms for AOP, and compared with several existing implementations of OP mheuristics.

The whole report can be found [here|].

### Run the Tsiligirides experiment
To run the Tsiligires resp. GRASP algorithm, enter `./TSILI_AOP` resp. `./GRASP_AOP`, enter your preferred experiment configuration in
`tsiligirides_aop.py` resp. `main.py` and run:

``python3.6 tsiligirides_aop.py``

resp.

``python3.6 main.py``.

The output you see are vertices along the found path and corresponding scores, resp. score, time and variant of GRASP used to obtain the result.

The appropriate input instance data format can be seen in the `./data` folder. The distance matrix is precomputed to improve performance.
