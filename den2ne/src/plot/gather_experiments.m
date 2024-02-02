%% Función para recolectar datos de todos los experimentos
%
%   [+] Autores: David Hernández Puerta <d.hernandezp@edu.uah.es>
%                Javier Díaz Fuentes <j.diazf@edu.uah.es>
%                David Carrascal <david.carrascal@uah.es> 
%
%   [+] Fecha: 22 Dic 2021


function data_out = gather_experiments(PATH_RESUTLS, TOPO_NAMES, TOPO_NUM_NODES, TOPO_DEGREES, TOPO_CRITERIONS, TOPO_BEHAVIORAL, TOPO_LOAD_LIMIT, TOPO_SEEDS, TOPO_RUNS)

    % Vars
    data_out = cell(length(TOPO_LOAD_LIMIT), length(TOPO_BEHAVIORAL));
    
    % Main loop 
    for limit_index=0:length(TOPO_LOAD_LIMIT)-1
        for behavioral_index=0:length(TOPO_BEHAVIORAL)-1

            % Build experiment path
            PATH_EXP = PATH_RESUTLS + "/exp_loadLimit_" + TOPO_LOAD_LIMIT(limit_index + 1) + "_behavioral_" + TOPO_BEHAVIORAL(behavioral_index + 1);

            % Let's parse all topos of the experiment_i
            data_out{limit_index + 1, behavioral_index + 1} = gather_topologies(PATH_EXP, TOPO_NAMES, TOPO_NUM_NODES, TOPO_DEGREES, TOPO_CRITERIONS, TOPO_SEEDS, TOPO_RUNS);
        end
    end
end