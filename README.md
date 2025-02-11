# CCT_task_2025

My submission for the route planning task. In this project, I have developed a Python program that calculates the optimal route plan for a fleet of vans delivering packages, with the objective of minimizing total fuel consumption. The solution includes two main functions:

*find_optimal_route_for_single_van – Finds the most fuel-efficient route for only one van.

*find_optimal_route_for_multiple_vans –  Finds the most fuel-efficient route for multiple vans. This function explores every possible assignment using an exhaustive search with backtracking.

  I chose to use a recursive backtracking (optimized exact permutation) algorithm for this task because:
*Problem Constraints: The maximum of 5 packages and 3 vans keeps the search space small, making an exhaustive approach optimal.
*Guaranteed Optimality: The backtracking method ensures that all valid routes are considered, which guarantees the optimal solution.
Another method I considered using was iterated modified simulated annealing (IMSA). I didn't choose it because it is used for large space solutions. Because in this task we have constraints with only 5 packages and 3 vans.That's why I can search every possible route. IMSA does not everytime find the best solution.
