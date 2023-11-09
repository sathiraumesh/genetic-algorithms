import unittest

import vm_scheduling_problem as vmp

class TestVMSchedulingProblem(unittest.TestCase):

    def test_makespan(self):
        vm_list =  vm_list = [ 
            ("vm1", 1000, 10),
            ("vm2", 2000, 20),
            ("vm3", 3000, 30),
        ]

        vp = vmp.VMSchedulingProblem(vm_list)
        individual = [0, 1, 2, 0, 1]
        vp.task_list = [('task_1', 5000), ('task_2', 1000), ('task_3', 2000), ('task_4', 3000), ('task_5', 4000)]
        make_span = vp.get_makespan(individual)
        self.assertEqual(make_span, 8)

    def test_cost(self):
        vm_list =  vm_list = [ 
            ("vm1", 1000, 10),
            ("vm2", 2000, 20),
            ("vm3", 3000, 30),
        ]

        vp = vmp.VMSchedulingProblem(vm_list)
        individual = [0, 1, 2, 0, 1]
        vp.task_list = [('task_1', 5000), ('task_2', 1000), ('task_3', 2000), ('task_4', 3000), ('task_5', 4000)]
        make_span = vp.get_cost_fitness(individual)
        self.assertEqual(make_span, 150)

if __name__ == '__main__': 
    unittest.main()