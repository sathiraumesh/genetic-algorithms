import numpy as np
import random 
import csv

class VMSchedulingProblem:

    def __init__(self, vm_list):
            self.task_list = self.generate_tasks(number_of_tasks=10000)
            self.vm_list = vm_list
            self.vmp_size = len(self.task_list)

    def __len__(self):
        return self.vmp_size

    def print_items(self, solution):
        makespan = self.get_makespan(solution)
        print("makespan = {}, solution = {}".format(makespan, solution))

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
        makespan = 0.0
        execution_time_of_vms = dict()
        for vm in self.vm_list: 
             execution_time_of_vms.update({vm[0]:0})
        task_finish_times = []

        for i in range(len(individual)):
            task = self.task_list[i]
            vm = self.vm_list[individual[i]]
            execution_time = task[1]/vm[1] + execution_time_of_vms.get(vm[0])
            task_finish_times.append(execution_time)
            execution_time_of_vms.update({vm[0]: execution_time})
        return max(task_finish_times)

def main():

    vm_list = [
        ("vm1", 1000, 30),
        ("vm2", 2000, 30),
        ("vm3", 4000, 45),
        ("vm4", 3000, 34),
        ("vm5", 4000, 55),
        ("vm6", 1000, 45)
    ]

    vmp = VMSchedulingProblem(vm_list)

    random_solution = np.random.randint(len(vmp.vm_list), size=len(vmp.task_list))
 
    vmp.print_items(random_solution)
if __name__ == "__main__":
    main()