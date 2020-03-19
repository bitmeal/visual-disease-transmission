python viz.py "{'population_size': 400, 'sim_time': 50, 'init_infections': 2, 'fps': 4, 'filename': 'docs/assets/img/free-for-all', 'random_seed': 1}"


python viz.py "{'init_mask_surgical': 100, 'population_size': 400, 'sim_time': 50, 'init_infections': 2, 'fps': 4, 'filename': 'docs/assets/img/1of4-surgical', 'random_seed': 1}"

python viz.py "{'init_mask_n95v': 100, 'population_size': 400, 'sim_time': 50, 'init_infections': 2, 'fps': 4, 'filename': 'docs/assets/img/1of4-n95', 'random_seed': 1}"


python viz.py "{'person_properties':{'mask_on_symptoms': True, 'default_mask': protection.Surgical}, 'population_size': 400, 'sim_time': 50, 'init_infections': 2, 'fps': 4, 'filename': 'docs/assets/img/surgical-on-symptoms', 'random_seed': 1}"

python viz.py "{'person_properties':{'isolate_on_symptoms': True}, 'population_size': 400, 'sim_time': 50, 'init_infections': 2, 'fps': 4, 'filename': 'docs/assets/img/isolate-on-symptoms', 'random_seed': 1}"


python viz.py "{'init_home_office': 100, 'force_public_infections': True, 'person_properties':{'interact_necessary_while_disabled': True}, 'second_population': True, 'population_size': 400, 'sim_time': 50, 'init_infections': 2, 'fps': 4, 'filename': 'docs/assets/img/1of4-home-office', 'random_seed': 1}"

python viz.py "{'init_home_office': 200, 'force_public_infections': True, 'person_properties':{'interact_necessary_while_disabled': True}, 'second_population': True, 'population_size': 400, 'sim_time': 50, 'init_infections': 2, 'fps': 4, 'filename': 'docs/assets/img/1of2-home-office', 'random_seed': 1}"


python viz.py "{'init_home_office': 200, 'force_public_infections': True, 'person_properties':{'interact_necessary_while_disabled': True, 'isolate_on_symptoms': True}, 'second_population': True, 'population_size': 400, 'sim_time': 50, 'init_infections': 2, 'fps': 4, 'filename': 'docs/assets/img/1of2-home-office-isolation', 'random_seed': 1}"


python viz.py "{'init_home_office': 200, 'person_properties':{'interact_necessary_while_disabled': True, 'isolate_on_symptoms': True}, 'second_population': True, 'population_size': 400, 'sim_time': 50, 'init_infections': 2, 'fps': 4, 'filename': 'docs/assets/img/1of2-home-office-isolation-best-case', 'random_seed': 5}"
