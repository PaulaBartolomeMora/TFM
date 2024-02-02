%% Función para recolectar datos de todas las semillas de una topología
%
%   [+] Autores: David Hernández Puerta <d.hernandezp@edu.uah.es>
%                Javier Díaz Fuentes <j.diazf@edu.uah.es>
%                David Carrascal <david.carrascal@uah.es> 
%
%   [+] Fecha: 22 Dic 2021

function data_out_csv = gather_csv(PATH_TOPO, TOPO_CRITERIONS, TOPO_SEEDS, TOPO_RUNS)

    % Start topo out data structure
    data_out_csv = cell(length(TOPO_CRITERIONS),length(TOPO_SEEDS));

    % Main loop
    for criteria_index=0:length(TOPO_CRITERIONS)-1
        for seed_index=0:length(TOPO_SEEDS)-1
            data_out_csv{criteria_index + 1, seed_index +1} = importdata(PATH_TOPO + "outdata_seed_" + TOPO_SEEDS(seed_index + 1)+ "_c_" + TOPO_CRITERIONS(criteria_index + 1) + ".csv");
        end
    end
end 
