import pygad
import numpy as np

def run_optimizer(h_us, num_sprints, limite_custo):

    gene_space = [list(range(num_sprints + 1))] * len(h_us)

    fitness_history = []

    def corrigir_solucao(solution):
        sprint_map = {i: [] for i in range(1, num_sprints + 1)}
        for idx, sprint in enumerate(solution):
            if sprint > 0:
                sprint_map[sprint].append(idx)

        for sprint_id, indices in sprint_map.items():
            custo_total = sum(h_us[i]["custo"] for i in indices)
            while custo_total > limite_custo and indices:
                pior = min(indices, key=lambda i: h_us[i]["importancia"] / h_us[i]["custo"])
                solution[pior] = 0
                indices.remove(pior)
                custo_total = sum(h_us[i]["custo"] for i in indices)
        return solution

    def fitness_func(ga_instance, solution, solution_idx):
        sprint_map = {i: [] for i in range(1, num_sprints + 1)}
        for idx, sprint in enumerate(solution):
            if sprint > 0:
                sprint_map[sprint].append(h_us[idx])
        fitness = 0
        for hu_list in sprint_map.values():
            for hu in hu_list:
                fitness += 1.0 * hu["importancia"] - 0.5 * hu["criticidade"] - 0.3 * hu["impacto"]
        return fitness


    def on_generation(instance):
        for i in range(instance.population.shape[0]):
            instance.population[i] = corrigir_solucao(instance.population[i])
        best = instance.best_solution()[1]
        fitness_history.append(best)

    ga = pygad.GA(
        num_generations=50,
        num_parents_mating=10,
        fitness_func=fitness_func,
        sol_per_pop=40,
        num_genes=len(h_us),
        gene_space=gene_space,
        parent_selection_type="tournament",
        crossover_type="single_point",
        mutation_type="random",
        mutation_percent_genes=20,
        on_generation=on_generation
    )

    ga.run()

    solution, solution_fitness, _ = ga.best_solution()

    # Organizar saída
    sprint_allocations = {i: [] for i in range(1, num_sprints + 1)}
    unallocated = []

    for idx, sprint_id in enumerate(solution):
        hu = h_us[idx]
        if sprint_id > 0:
            sprint_allocations[sprint_id].append(hu)
        else:
            unallocated.append(hu)

    sprints_info = []
    for sprint_id, hu_list in sprint_allocations.items():
        custo = sum(hu["custo"] for hu in hu_list)
        fit = sum(1.0 * hu["importancia"] - 0.5 * hu["criticidade"] - 0.3 * hu["impacto"] for hu in hu_list)
        sprints_info.append({
            "sprint": sprint_id,
            "custo_total": custo,
            "fitness": round(fit, 2),
            "requisitos": hu_list
        })

    return {
        "melhor_fitness_total": round(solution_fitness, 2),
        "sprints": sprints_info,
        "nao_alocados": unallocated
    }
