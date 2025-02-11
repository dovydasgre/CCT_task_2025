# CCT Task 2025 – Optimal Route Planning  

## Project Overview  
This project implements a Python program to calculate the most **fuel-efficient** route for a fleet of vans delivering packages. The goal is to minimize total fuel consumption by determining the optimal delivery assignments.   

### **Single Van Optimization**  
`find_optimal_route_for_single_van` – Computes the most fuel-efficient route for a single van.  

### **Multiple Van Optimization**  
`find_optimal_route_for_multiple_vans` – Finds the optimal assignment of deliveries among multiple vans using **exhaustive search with backtracking**.  

## Why Recursive Backtracking?  

I selected a **recursive backtracking (optimized exact permutation)** approach due to:  
**Problem Constraints:** The problem is constrained to a maximum of **5 packages** and **3 vans**, making an exhaustive search feasible.  
**Guaranteed Optimality:** Backtracking ensures all possible routes are explored, guaranteeing the most efficient solution.  

## Alternative Approach Considered  

I also considered using **Iterated Modified Simulated Annealing (IMSA)** but decided against it because:  

**IMSA is suited for large search spaces**, while this problem has strict constraints.  
**IMSA does not always guarantee the best solution**, whereas backtracking provides an exact optimal result.  

