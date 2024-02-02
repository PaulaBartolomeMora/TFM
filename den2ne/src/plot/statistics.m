function [medias_modelo_grado_criterio_nodo, int_conf_modelo_grado_criterio_nodo] = statistics(datos,  TOPO_NAMES, TOPO_NUM_NODES, TOPO_DEGREES, TOPO_CRITERIONS, TOPO_SEEDS, PLOT_MEAS)   
    % media por semilla fijando criterio 
    
    media = zeros(length(TOPO_SEEDS),length(PLOT_MEAS));
    media_de_medias_por_nodo = zeros(length(TOPO_NUM_NODES),length(PLOT_MEAS));
    media_de_medias_por_nodo_y_criterio = cell(length(PLOT_MEAS),1);
    media_de_medias_por_nodo_criterio_y_grado = cell(length(TOPO_DEGREES),1);
    medias_modelo_grado_criterio_nodo = cell (length(TOPO_NAMES),1);
    int_conf_por_nodo = zeros(length(TOPO_NUM_NODES),length(PLOT_MEAS));
    int_conf_por_nodo_y_criterio = cell(length(PLOT_MEAS),1);
    int_conf_por_nodo_criterio_y_grado = cell(length(TOPO_DEGREES),1);
    int_conf_modelo_grado_criterio_nodo = cell(length(TOPO_NAMES),1);

    for model_index=0:length(TOPO_NAMES)-1
        for degree_index=0:length(TOPO_DEGREES)-1
            for criteria_index=0:length(TOPO_CRITERIONS)-1
                for node_index=0:length(TOPO_NUM_NODES)-1
                    for seed_index=0:length(TOPO_SEEDS)-1

                        %se realiza la media de cada archivo csv 
                        media(TOPO_SEEDS(seed_index+1),:,1) = mean(datos{model_index+1,node_index+1,degree_index+1} ...
                            {criteria_index+1,seed_index+1});
                    end
                    %se realiza la media de medias por cada nodo
                    media_de_medias_por_nodo(node_index+1,:) = mean(media); 
                    int_conf_por_nodo(node_index+1,:)= confidence_interval(length(TOPO_SEEDS),media);
                end
                %por cada criterio
                media_de_medias_por_nodo_y_criterio{criteria_index+1} = media_de_medias_por_nodo;
                int_conf_por_nodo_y_criterio{criteria_index+1} = int_conf_por_nodo;
            end
            %por cada grado de conectividad
            media_de_medias_por_nodo_criterio_y_grado{degree_index+1} = media_de_medias_por_nodo_y_criterio;
            int_conf_por_nodo_criterio_y_grado{degree_index+1} = int_conf_por_nodo_y_criterio;
        end
        %por modelo
        medias_modelo_grado_criterio_nodo{model_index+1} = media_de_medias_por_nodo_criterio_y_grado;
        int_conf_modelo_grado_criterio_nodo{model_index+1} = int_conf_por_nodo_criterio_y_grado;
    end
end