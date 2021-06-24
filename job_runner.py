import os
import numpy as np
from datetime import datetime
import itertools

os.system('clear')
def getMaterialParameters(nu, E, mu1, mu2, K, mu_div = None):
    mus = []
    mu = []
    if len(mu1) != 0:
        mus.append(mu1[0])
    if len(mu2) != 0:
        mus.append(mu2[0])
    if len(mus) != 0:
        mu.append(np.sum(mus))

    if len(nu) != 0 and len(E) != 0:
        if len(mu) == 0:
            mu.append( E[0]/(2 + 2*nu[0]) )
            print(mu)
        if len(K) == 0:
            K.append( E[0]/(3 - 6*nu[0]) )

    if len(nu) != 0 and len(K) != 0:
        if len(mu)== 0:
            mu.append( (3*K[0] - 6*K[0]*nu[0])/(2 - 2*nu[0]) )
        if len(E)== 0:
            E.append( 3*K[0] - 6*K[0]*nu[0] )

    if len(nu) != 0 and len(mu) != 0:
        if len(K)== 0:
            K.append( (2*mu[0] + 2*mu[0]*nu[0])/(3 - 6*nu[0]) )
        if len(E)== 0:
            E.append( 2*mu[0] + 2*mu[0]*nu[0] )

    if len(mu) != 0 and len(K) != 0:
        if len(nu)== 0:
            nu.append( (3*K[0] - 2*mu[0])/(6*K[0] + 2*mu[0]) )
        if len(E)== 0:
            E.append( (9*K[0]*mu[0])/(3*K[0] + mu[0]) )

    if len(mu) != 0 and len(E) != 0:
        if len(nu)== 0:
            nu.append( E[0]/(2*mu[0]) - 1 )
        if len(K)== 0:
            K.append( (E[0]*mu[0])/(9*mu[0] - 3*E[0]) )

    # split up the mu values into mu1 and mu2
    if mu_div is None:
        mu_div = 0.5

    if len(mu1) == 0 and len(mu2) == 0:
        mu1.append(mu[0]*mu_div)
        mu2.append(mu[0] - mu1[0])

    return nu, E, mu1, mu2, K


to_print = False
build_path = '/Users/klstengel/Projects/CU_research_Brown/libCEED/examples/solids/elasticity'

out_dir = '/Users/klstengel/Projects/CU_research_Brown/gradResearchData/libCEED/altair_plot/'

clopt_string = ""

id = '_logJ_' # TO DO: RERUN ENERGY W/ LOG(J)
#mesh options
# mesh_opt = { '-dm_plex_box_faces': '3,3,3',
#              '-bc_clamp': '1,2,3,4,5,6',
#              '-bc_clamp_1_rotate': '0,0,1,0,.3',
#              '-bc_clamp_2_rotate': '0,0,1,0,.3',
#              '-bc_clamp_3_rotate': '0,0,1,0,.3',
#              '-bc_clamp_4_rotate': '0,0,1,0,.3',
#              '-bc_clamp_5_rotate': '0,0,1,0,.3',
#              '-bc_clamp_6_rotate': '0,0,1,0,.3'
#             }

# mesh_opt = { '-dm_plex_box_faces': '3,3,3',
#              '-bc_clamp': '1,2,3,4,5,6',
#              '-bc_clamp_1_translate': '0,0,1,0,.3',
#              '-bc_clamp_2_translate': '0,0,1,0,.3',
#              '-bc_clamp_3_translate': '0,0,1,0,.3',
#              '-bc_clamp_4_translate': '0,0,1,0,.3',
#              '-bc_clamp_5_translate': '0,0,1,0,.3',
#              '-bc_clamp_6_translate': '0,0,1,0,.3'
#             }

mesh_opt = { '-dm_plex_box_faces': '3,3,3',
             '-bc_clamp': '1',
             '-bc_traction': '2',
             '-bc_traction_2': '0,0.1,0'
            }

# mesh_opt ={'-forcing':'mms'}
for opt, val in mesh_opt.items():
    clopt_string = clopt_string + ' ' + opt + ' ' + str(val)

#cloptions for things that don't change between runs
cloptions = {'-outer_ksp_converged_reason': '',
             # '-outer_ksp_max_it': 50,
             '-outer_ksp_monitor_true_residual': '',
             '-outer_ksp_norm_type': 'preconditioned',
             '-outer_ksp_type': 'gmres',
             '-ksp_monitor_singular_value': '',
             '-outer_pc_type': 'lu',
             # '-print_strain_every_increment': '',
             '-snes_fd': '',
             '-snes_linesearch_atol': 1e-30,
             '-snes_linesearch_monitor': '',
             '-snes_linesearch_type': 'cp',
             '-snes_monitor': '',
             # '-snes_view': '',
             '-view_soln': '',
             '-log_view': ''
            }

for opt, val in cloptions.items():
    if val != '':
        clopt_string = clopt_string + ' ' + opt + ' ' + str(val)
    else:
        clopt_string = clopt_string + ' ' + opt


nu = []
E = []
mu2 = [3.846153846153846]
mu1 = [0.0]
K = [20]
nu, E, mu1, mu2, K = (getMaterialParameters(nu, E, mu1, mu2, K, 1.0))
print('nu:', nu[0], ', E:',E[0], ', mu1:', mu1[0], ', mu2:', mu2[0], ', K:', K[0])

id = '_NH_equiv_test'

#material properties, etc
run_opts = {'-degree': [1],
            '-E': E,
            '-nu': nu,
            '-K': K,
            '-mu_1': mu1,
            '-mu_2': mu2,
            '-num_steps': [20],
            '-problem': ['FSInitial-MR1', 'FSInitial-NH1']
           }
# print(*[v for v in run_opts.values()])
opt_combos = list(itertools.product(*[v for v in run_opts.values()]))
# print(opt_combos)

#make elasticity
#os.system('make PETSC_DIR=/Users/klstengel/Projects/CU_research_Brown/petsc PETSC_ARCH=libceed')

for combo in opt_combos:
    combo_string = ''
    for k, key in enumerate(run_opts.keys()):
        combo_string = combo_string + ' ' + key + ' ' + str(combo[k])

    print('Running elasticity with: ' + combo_string)
    out_loc = out_dir + combo[-1] + id + '/' #out_dir + datetime.now().strftime("%Y%m%d%H%M%S") + '_' + combo[-1] + id + '/'
    if not os.path.exists(out_loc):
        print('Making directory: ' + out_loc)
        os.makedirs(out_loc)
    if to_print:
        print(build_path + ' ' + clopt_string + combo_string + ' -output_dir ' + out_loc + ' > ' + out_loc + 'log.txt')
    # os.system(build_path + ' ' + clopt_string + combo_string + ' -output_dir ' + out_loc + ' > ' + out_loc + 'log.txt')
