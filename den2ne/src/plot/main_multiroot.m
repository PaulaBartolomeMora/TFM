%% Fichero Main para dibijar todos los resultados para la ejecución multiroot
%
%   [+] Autor: David Carrascal <david.carrascal@uah.es> 
%   [+]        Javier Díaz <j.diazf@uah.es>
%
%   [+] Fecha: 22 Marzo 2022
clc
close all
clear variables

%% Global Vars

% Paths
PATH_RESUTLS_DIR = './';
PATH_RESUTLS_MAT_DATA = './';
PATH_OUTPUT_FIG_PDF = './figMultiroot';

% Name 
NAME_RESUTLS = 'results-MultiRoot';

% Script flags
SAVE_FIG = true;

% Experiments vars
TOPO_NAMES = ["barabasi" , "waxman"];
TOPO_NUM_NODES = 10:10:200;
TOPO_DEGREES = 2:2:6;
TOPO_CRITERIONS = 0:1:5;
%TOPO_BEHAVIORAL = 0:1:3;
TOPO_BEHAVIORAL = 0;
%TOPO_LOAD_LIMIT = 0:1:1;
TOPO_LOAD_LIMIT = 0;
TOPO_SEEDS = 1:1:10;
TOPO_RUNS = 1:1:10;

% Plot vars
PLOT_MEAS = [0 1 2 3 4 5];  % Seed(0)
                            % Global balance (1)
                            % Abs flux(2)
                            % IDs time (3)
                            % Global balance time(4)
                            % Number of iterations for multiroot (5)


%% Main block

% First of all, we have to check if we have already parse the data into a
% *.mat file..
if isfile(strcat(PATH_RESUTLS_MAT_DATA, NAME_RESUTLS,'.mat'))
    % File exist.
    load(strcat(PATH_RESUTLS_MAT_DATA, NAME_RESUTLS,'.mat'));
else
    % File does not exist, then we have to generate it
    data = gather_experiments(strcat(PATH_RESUTLS_DIR, NAME_RESUTLS), TOPO_NAMES, TOPO_NUM_NODES, TOPO_DEGREES, TOPO_CRITERIONS, TOPO_BEHAVIORAL, TOPO_LOAD_LIMIT, TOPO_SEEDS, TOPO_RUNS);

    % And, we are going to save it in order to speed up future plots
    save(strcat(PATH_RESUTLS_MAT_DATA, NAME_RESUTLS,'.mat'), "data");
end



% Second, post-processing data
for limit_index=0:length(TOPO_LOAD_LIMIT)-1
    for behavioral_index=0:length(TOPO_BEHAVIORAL)-1
        for model_index=0:length(TOPO_NAMES)-1
            for node_index=0:length(TOPO_NUM_NODES)-1
                for degree_index=0:length(TOPO_DEGREES)-1
                    for criteria_index=0:length(TOPO_CRITERIONS)-1
                        for seed_index=0:length(TOPO_SEEDS)-1
                            data{limit_index + 1, behavioral_index + 1}{model_index + 1, node_index + 1, degree_index + 1}{criteria_index + 1, seed_index +1} = seg2mseg_Multiroot(data{limit_index + 1, behavioral_index + 1}{model_index + 1, node_index + 1, degree_index + 1}{criteria_index + 1, seed_index +1});
                        end
                    end
                end
            end
        end
    end
end

% Third, we are going to plot all the results
for limit_index=0:length(TOPO_LOAD_LIMIT)-1
    for behavioral_index=0:length(TOPO_BEHAVIORAL)-1
        title = "exp_loadLimit_" + TOPO_LOAD_LIMIT(limit_index + 1) + "_behavioral_" + TOPO_BEHAVIORAL(behavioral_index + 1);
        plot_experiments(data{limit_index +1,behavioral_index+1}, title, PATH_OUTPUT_FIG_PDF, PLOT_MEAS, TOPO_NAMES, TOPO_NUM_NODES, TOPO_DEGREES, TOPO_CRITERIONS, TOPO_SEEDS);
    end
end
