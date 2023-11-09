import numpy as np
import random 
import statistics as sc
import csv

class VMSchedulingProblem:

    def __init__(self, vm_list):
            self.task_list = self.generate_tasks(number_of_tasks=1000)
            self.vm_list = vm_list
            self.vmp_size = len(self.task_list)

    def __len__(self):
        return self.vmp_size

    def print_items(self, solution):
        makespan = self.get_makespan(solution)
        cost = self.get_cost_fitness(solution)

        print("makespan = {}, cost = {}, solution = {}".format(makespan, cost, solution))

    def generate_tasks(self, number_of_tasks = 100):
        task_list = []
        with open('./vm_scheduling/tasks.csv', 'r') as file :
             reader = csv.DictReader(file)
             for row in reader:
                  task_list.append((f"task_{row['id']}", int(row['mips'])))
                  # task_list.append(("s",row["mips"]))
        # for i in range(number_of_tasks):
        #       mips_random = random.randint(10000, 50000)
        #       task_list.append((f"task{row}", mips_random))
        return task_list

    
    def get_makespan(self, individual):
      
        execution_time_of_vms = dict()
        
        for vm in self.vm_list: 
             execution_time_of_vms.update({vm[0]:0})
        task_finish_times = []

        for i in range(len(individual)):
            task = self.task_list[i]
            vm = self.vm_list[individual[i]]
            execution_time = task[1]/vm[1] +execution_time_of_vms.get(vm[0])
            task_finish_times.append(execution_time)
            execution_time_of_vms.update({vm[0]: execution_time})
        return max(task_finish_times) 
     
    def get_multiobjective(self, individual):

      execution_time_of_vms = dict()

      for vm in self.vm_list: 
            execution_time_of_vms.update({vm[0]:0})
      task_finish_times = []
     
      for i in range(len(individual)):
  
          task = self.task_list[i]
          vm = self.vm_list[individual[i]]
          execution_time = task[1]/vm[1] 
          task_finish_times.append(execution_time)
          execution_time_of_vms.update({vm[0]: execution_time})
      
      return 1/10*sum(task_finish_times) + self.get_cost(individual)
    
    def get_cost(self, individual): 
      cost = 0.0
      
      for i in range(len(individual)):
          task = self.task_list[i]
          vm = self.vm_list[individual[i]]
          
          task_finish_time = task[1]/vm[1]
          cost = cost + task_finish_time*vm[2]
      return cost

    def muti_objective_fitness(self, individual):
      makespan = 0.0
      cost = 0.0
      execution_time_of_vms = dict()

      #update all the vms execution times to 1
      for vm in self.vm_list: 
            execution_time_of_vms.update({vm[0]:0})
      task_finish_times = []
     
      for i in range(len(individual)):
          task = self.task_list[i]
          vm = self.vm_list[individual[i]]
          execution_time = task[1]/vm[1] + execution_time_of_vms.get(vm[0])
          task_finish_times.append(execution_time)
          execution_time_of_vms.update({vm[0]: execution_time})

      return sum(task_finish_times)

def main():

    vm_list = [
        ("vm1", 1000, 30),
        ("vm2", 1000, 30),
        ("vm3", 1000, 30),
        ("vm4", 1000, 30),
        ("vm5", 1000, 30),
        ("vm6", 2000, 30),
        ("vm7", 2000, 30),
        ("vm8", 2000, 30),
        ("vm9", 2000, 30),
        ("vm10", 2000, 30),
        ("vm11", 4000, 45),
        ("vm12", 4000, 45),
        ("vm13", 4000, 45),
        ("vm14", 4000, 45),
        ("vm15", 4000, 45),
        ("vm16", 3000, 45),
        ("vm17", 3000, 34),
        ("vm18", 3000, 34),
        ("vm19", 3000, 34),
        ("vm20", 3000, 34),
    ]

    vmp = VMSchedulingProblem(vm_list)

    random_solution = np.random.randint(len(vmp.vm_list), size=len(vmp.task_list))
 
    vmp.print_items(random_solution)
if __name__ == "__main__":
    main()