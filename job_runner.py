import os
from datetime import date
import itertools

os.system('clear')
build_path = '/Users/klstengel/Projects/CU_research_Brown/libCEED/examples/solids/elasticity'

out_dir = '/Users/klstengel/Projects/CU_research_Brown/gradResearchData/libCEED/strain_plot/'

clopt_string = ""

#mesh options
mesh_opt = { '-dm_plex_box_faces': '4,4,4',
             '-bc_clamp': '1,2,3,4,5,6',
             '-bc_clamp_1_rotate': '0,0,1,0,.3',
             '-bc_clamp_2_rotate': '0,0,1,0,.3',
             '-bc_clamp_3_rotate': '0,0,1,0,.3',
             '-bc_clamp_4_rotate': '0,0,1,0,.3',
             '-bc_clamp_5_rotate': '0,0,1,0,.3',
             '-bc_clamp_6_rotate': '0,0,1,0,.3'
            }
for opt, val in mesh_opt.items():
    clopt_string = clopt_string + ' ' + opt + ' ' + str(val)

#cloptions for things that don't change between runs
cloptions = {'-outer_ksp_converged_reason': '',
             '-outer_ksp_max_it': 50,
             '-outer_ksp_monitor_true_residual': '',
             '-outer_ksp_norm_type': 'preconditioned',
             '-outer_ksp_type': 'gmres',
             '-outer_pc_type': 'lu',
             '-print_strain_every_increment': '',
             '-snes_fd': '',
             '-snes_linesearch_atol': 1e-30,
             '-snes_linesearch_monitor': '',
             '-snes_linesearch_type': 'cp',
             '-snes_monitor': '',
             '-snes_view': '',
             '-view_soln': '',
             '-log_view': ''
            }

for opt, val in cloptions.items():
    if val != '':
        clopt_string = clopt_string + ' ' + opt + ' ' + str(val)
    else:
        clopt_string = clopt_string + ' ' + opt

# print(clopt_string)
nu = [0.4]
mu1 = [1]
mu2 = [0]
K = [round((2*1+ 2*1*nu[0])/(3- 6*nu[0]), 3)]
E = [round(3*K[0] - 6*K[0]*nu[0], 3)]
# print(K, E)
#material properties, etc
run_opts = {'-degree': [1],
            '-E': E,
            '-nu': nu,
            '-K': K,
            '-mu_1': mu1,
            '-mu_2': mu2,
            '-num_steps': [40],
            '-problem': ['FSInitial-NH1', 'FSInitial-MR1']
           }
# print(*[v for v in run_opts.values()])
opt_combos = list(itertools.product(*[v for v in run_opts.values()]))
# print(opt_combos)

for combo in opt_combos:
    combo_string = ''
    for k, key in enumerate(run_opts.keys()):
        combo_string = combo_string + ' ' + key + ' ' + str(combo[k])

    print('Running elasticity with: ' + combo_string)
    out_loc = out_dir + date.today().strftime("%Y%m%d") + '_' + combo[-1] + '/'
    if not os.path.exists(out_loc):
        os.makedirs(out_loc)
    # print(build_path + ' ' + clopt_string + combo_string + ' -output_dir ' + out_loc + ' > ' + out_loc + 'log.txt')
    os.system(build_path + ' ' + clopt_string + combo_string + ' -output_dir ' + out_loc + ' > ' + out_loc + 'log.txt')
