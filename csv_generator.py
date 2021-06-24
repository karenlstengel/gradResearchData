import os
import csv

static_str = './elasticity  -dm_plex_box_faces 4,4,4 -bc_clamp 1,2,3,4,5,6 -bc_clamp_1_rotate 0,0,1,0,.3 -bc_clamp_2_rotate 0,0,1,0,.3 -bc_clamp_3_rotate 0,0,1,0,.3 -bc_clamp_4_rotate 0,0,1,0,.3 -bc_clamp_5_rotate 0,0,1,0,.3 -bc_clamp_6_rotate 0,0,1,0,.3 -outer_ksp_converged_reason -outer_ksp_max_it 50 -outer_ksp_norm_type preconditioned -outer_ksp_type gmres -outer_pc_type lu -print_strain_every_increment -snes_fd -snes_linesearch_atol 1e-30 -snes_linesearch_monitor -snes_linesearch_type cp'

degree = 1

problem_dict = {'problem': ['FSInitial-MR1', 'FSInitial-MR1', 'FSInitial-NH1'],
            'mu_1': [1.0, 0.5, 1.0],
            'mu_2': [0.0, 0.5, 0.0],
            'K': [4.667, 4.667, 4.667],
            'E': [2.8, 2.8, 2.8],
            'nu': [0.4, 0.4, 0.4]
            }

load = [0,1,2] #np.arange(40)
strain = {}

# os.system( static_str + ' -degree ' + str(degree) +' -E ' + (str) + ' -nu ' + str(problem_dict['nu'][i]) + ' -K ' + str(problem_dict['K'][i]) + ' -mu_1 ' + str(problem_dict['mu_1'][i]) + '-mu_2' + str(problem_dict['mu_2'][i]) + ' -num_steps 40 -problem' +  FSInitial-MR1 ' > ' + problem_dict['problem'][i] + + '_' + str(i) + '_log.txt')

for i in range(len(problem_dict['problem'])):
    os.system(static_str + ' -degree ' + str(degree) +' -E ' + str(problem_dict['E'][i]) + ' -nu ' + str(problem_dict['nu'][i]) + ' -K ' + str(problem_dict['K'][i]) + ' -mu_1 ' + str(problem_dict['mu_1'][i]) + '-mu_2' + str(problem_dict['mu_2'][i]) + ' -num_steps 2 -problem' + problem_dict['problem'][i] + ' > ' + problem_dict['problem'][i] + '_' + str(i) + '_log.txt')

    with open(problem_dict['problem'][i] + '_' + str(i) + '_log.txt', 'r') as logfile:
        Lines = logfile.readlines()
        for line in Lines:
            line_arr = line.strip().split(' ')

            if 'Strain' in line_arr:
                if problem_dict['problem'][i]  + ' ' + str(i) in strain.keys():
                    strain[problem_dict['problem'][i] + ' ' + str(i)].append(float(line_arr[-1]) )
                else:
                    strain[problem_dict['problem'][i] + ' ' + str(i)] = [float(line_arr[-1])]


with open('strainEnergy_vs_loadIncrement_data.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',')

    header = ['Load Increment']
    for key in strain.keys():
        header.append(key)
    spamwriter.writerow(header)

    print(load, strain)
    for i in range(len(strain[strain.keys()[0]][:-1])):
        line = [load[i]]
        for key in strain.keys():
            line.append(strain[key][i])

        spamwriter.writerow(line)

with open('strainEnergy_vs_loadIncrement_params.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',') 

    header = ['Parameter']
    for key in strain.keys():
        header.append(key)
    spamwriter.writerow(header)

    for p in problem_dict.keys():
        if p != 'problem':
            line = [p]
            for num, key in enumerate(strain.keys()):
                line.append(problem_dict[p][num])

            spamwriter.writerow(line)
