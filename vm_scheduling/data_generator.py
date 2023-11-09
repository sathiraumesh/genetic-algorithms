
import csv 
import random

def generate_tasks(size = 10000):
  with open('./vm_scheduling/tasks.csv', 'w', newline= '') as file :
    writer = csv.writer(file)
    writer.writerow(["id", "mips"])
    for i in range(size):
       mips_random = random.randint(1000, 10000)
       writer.writerow([i+1, mips_random])
    
def first_come_serve(): 
    task_list = []

    vm_list = [
        ("vm1", 1000, 30),
        ("vm2", 2000, 30),
        ("vm3", 3000, 45),
        ("vm4", 4000, 34),
        ("vm5", 5000, 55),
        ("vm6", 6000, 45)
    ]

    with open('./vm_scheduling/tasks.csv', 'r') as file :
          reader = csv.DictReader(file)
          for row in reader:
              task_list.append((f"task_{row['id']}", int(row['mips'])))


    return task_list


# def get_cost(vm_list, task_list):
#     makespan = 0.0
#     execution_time_of_vms = dict()
    
#     for vm in vm_list: 
#           execution_time_of_vms.update({vm[0]:0})

#     task_finish_times = []

#     for i in range(task_list):
#         task = task_list[i]
#         vm = vm_list[individual[i]]
#         execution_time = task[1]/vm[1] + execution_time_of_vms.get(vm[0])
#         task_finish_times.append(execution_time)
#         execution_time_of_vms.update({vm[0]: execution_time})

def read_data(): 
   with open('./vm_scheduling/tasks.csv', 'r') as file :
             reader = csv.reader(file)
            #  headers = next(reader)
             for row in reader:
                  print(row)
if __name__ == '__main__':
    generate_tasks()
  # read_data()

