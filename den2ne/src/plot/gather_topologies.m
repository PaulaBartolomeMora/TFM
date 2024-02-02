%% Función para recolectar datos de todas las topologias de un experimento
%
%   [+] Autores: David Hernández Puerta <d.hernandezp@edu.uah.es>
%                Javier Díaz Fuentes <j.diazf@edu.uah.es>
%                David Carrascal <david.carrascal@uah.es> 
%
%   [+] Fecha: 22 Dic 2021

function data_out_experiment = gather_topologies(PATH_EXP, TOPO_NAMES, TOPO_NUM_NODES, TOPO_DEGREES, TOPO_CRITERIONS, TOPO_SEEDS, TOPO_RUNS)

    % Start the data structure for the experiment
    data_out_experiment = cell(length(TOPO_NAMES), length(TOPO_NUM_NODES), length(TOPO_DEGREES));
    
    % Main loop 
    for model_index=0:length(TOPO_NAMES)-1
        for node_index=0:length(TOPO_NUM_NODES)-1
            for degree_index=0:length(TOPO_DEGREES)-1

                % Let's build topo dir path
                PATH_TOPO = PATH_EXP + "/" + TOPO_NAMES(model_index + 1) + "-" + TOPO_NUM_NODES(node_index + 1) + "-" + TOPO_DEGREES(degree_index + 1) + "/";

                % Let's gather topo data
                data_out_experiment{model_index + 1, node_index + 1, degree_index + 1} = gather_csv(PATH_TOPO, TOPO_CRITERIONS, TOPO_SEEDS, TOPO_RUNS);
            end
        end
    end
end