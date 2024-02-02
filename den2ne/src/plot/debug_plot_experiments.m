%% Función para pintar datos de un experimento
%
%   [+] Autores: David Hernández Puerta <d.hernandezp@edu.uah.es>
%                Javier Díaz Fuentes <j.diazf@edu.uah.es>
%                David Carrascal <david.carrascal@uah.es> 
%
%   [+] Fecha: 22 Dic 2021

function plot_experiments(data_exp, title_in, PATH_OUTPUT_FIG_PDF, PLOT_MEAS, TOPO_NAMES, TOPO_NUM_NODES, TOPO_DEGREES, TOPO_CRITERIONS, TOPO_SEEDS) 
        
    for plot_meas_index=0:length(PLOT_MEAS)-1
        % Init subplot
        subplot = @(m,n,p) subtightplot (m, n, p, [0.075 0.075], [0.32 0.02], [0.07 0.04]); 
        
        % Opciones para las graficas
        line_size = 1.0;

        % Cat title
        title_names =  ["Seed", "Global balance", "Abs flux", "IDs time","Global balance time", "Number of iterations"];
        title_str = strcat(title_in, " - ", title_names(PLOT_MEAS(plot_meas_index+1)+1));
        
        % Labels
        criterio = ["Number Hops", "Distance" ,"Power Balance", "Power Balance with Losses", "Link Losses", "Power Balance Weighted"]; 
        marker = ["-o", "--^", ":*", "-.d","-x", "--v"];
        topos_str = ["Barabasi", "Waxman"];
        
        % Colors for datapoints and error bars 
        colors = ["#0072BD","#D95319","#EDB120","#7E2F8E","#77AC30","#4DBEEE"];

        % Y axis
        y_min= -25;
        y_max= 25;
        y_jumps = 5;
        
        % X axis
        num_ticks_x = (100:10:200);
        %num_ticks_x = (120:1:150);
        name_ticks_x = {'100','110','120','130','140','150','160','170','180','190','200'};
        %name_ticks_x = {'10','20','30','40','50','60','70','80','90','100','110','120','130','140','150','160','170','180','190','200'};
        %name_ticks_x = 120:1:150;
        
        % Data range we want to plot from the data array
        % For example for normal plot, we represent nodes from 100 to 200,
        % which in data array uses the position 10 to 20, then
        %data_range = 10:20;
        data_range = (10:20);
        
        % Error bar size
        Marker_Size = 6;
                
        % PDF specs
        size_legends = 7;
        paper_size = [18 20];
        paper_position = [0.25 0 14-0.25 15.99];
        pos_legend = [0.53 0.11 0 0]; 
        
        % Generate PDF file
        fig=figure('Name', sprintf('plot_%s.pdf', title_str));
        fig.PaperOrientation='landscape';
        fig.PaperSize=paper_size;
        fig.Units = 'centimeters';
        fig.PaperPosition = paper_position;
        
        % Get stats 
        [mean_model_grade_criterion_node, conf_int_model_grade_criterion_node] = statistics(data_exp,  TOPO_NAMES, TOPO_NUM_NODES, ...
                                                                                            TOPO_DEGREES, TOPO_CRITERIONS, TOPO_SEEDS, PLOT_MEAS);

        % Get rid of the current subplot
        number_subplot = 1;
    
    
        for degree_index=0:length(TOPO_DEGREES)-1
            for model_index=0:length(TOPO_NAMES)-1
               
                % Subplot init 
                subplot(3,1,number_subplot);
                hold on;
                
                % Plot all criteria 
%                 for criteria_index=0:length(TOPO_CRITERIONS)-1
%                     plot (num_ticks_x, mean_model_grade_criterion_node{model_index+1}{degree_index+1}{criteria_index+1}(data_range,PLOT_MEAS(plot_meas_index+1)+1),marker(criteria_index+1),...
%                         'LineWidth',line_size, 'MarkerSize', Marker_Size, 'Color',colors(criteria_index+1));
%                     errorbar(num_ticks_x, mean_model_grade_criterion_node{model_index+1}{degree_index+1}{criteria_index+1}(data_range,PLOT_MEAS(plot_meas_index+1)+1),...
%                         conf_int_model_grade_criterion_node{model_index+1}{degree_index +1}{criteria_index+1}(data_range,PLOT_MEAS(plot_meas_index+1)+1)',".",'LineWidth',...
%                         1, 'MarkerSize', Marker_Size,'Color',colors(criteria_index+1));
%                 end
                aux_bars = zeros(length(data_range),length(TOPO_CRITERIONS));
                aux_error = zeros(length(data_range),length(TOPO_CRITERIONS));
                for i=0:length(TOPO_CRITERIONS)-1
                    aux_bars(:,i+1) = mean_model_grade_criterion_node{model_index+1}{degree_index+1}{i+1}(data_range, PLOT_MEAS(plot_meas_index+1)+1);
                    aux_error(:,i+1) = conf_int_model_grade_criterion_node{model_index+1}{degree_index+1}{i+1}(data_range, PLOT_MEAS(plot_meas_index+1)+1);
                end

                pt=bar(aux_bars,'FaceColor','Flat');
                for ib=1:length(TOPO_CRITERIONS)
                    pt(ib).CData=ib;
                end

                for ib = 1:numel(pt)
                    xData = pt(ib).XData+pt(ib).XOffset;
                    e=errorbar(xData,pt(ib).YData,aux_error(:,ib).','k.','LineWidth',line_size);
                    e.CapSize=3;
                end

                % Adjust the curr subplot
                %xticks(num_ticks_x);
                xticklabels(name_ticks_x);
                
                if (PLOT_MEAS(plot_meas_index+1) == 1) 
                    ylim([y_min y_max]);
                    yticks(y_min:y_jumps:y_max)
                end
    
                % Set grid
                grid on;
                box on;
                
                if (number_subplot == 1 || number_subplot == 2 || number_subplot == 3)
                    if PLOT_MEAS(plot_meas_index+1) == 0
                        ylabel(sprintf("Degree %d\n Seed",(degree_index +1)*2));
                    elseif (PLOT_MEAS(plot_meas_index+1) == 1 || PLOT_MEAS(plot_meas_index+1) == 2) 
                        ylabel(sprintf("Degree %d\n Power (kW)",(degree_index +1)*2));
                    elseif (PLOT_MEAS(plot_meas_index+1) == 3 || PLOT_MEAS(plot_meas_index+1) == 4)
                        ylabel(sprintf("Degree %d\n Time (ms)",(degree_index +1)*2));
                    else
                        ylabel(sprintf("Degree %d\n Number of iterations",(degree_index +1)*2));
                    end
    
                end
                
                %if (number_subplot == 1 || number_subplot == 2)
                if (number_subplot == 1)
                    title(topos_str(model_index+1));
                end
    
                %if(number_subplot == 5 || number_subplot == 6)
                if(number_subplot == 3)
                    xlabel ("Number of nodes");
                end
                
                hold off
                number_subplot = number_subplot+1;
            end
        end
    
        % Set legend
        h_legend=legend(criterio, 'location','best');
        set(h_legend,'FontSize',size_legends);
        set(h_legend,'position',pos_legend);
        
        % Save the file
        if PLOT_MEAS(plot_meas_index+1) == 0
            format='%s/seed_%s.pdf';
            print(fig,sprintf(format, PATH_OUTPUT_FIG_PDF, title_in),'-dpdf','-fillpage');
        elseif PLOT_MEAS(plot_meas_index+1) == 1
            format='%s/balance_%s.pdf';
            print(fig,sprintf(format, PATH_OUTPUT_FIG_PDF, title_in),'-dpdf','-fillpage');
        elseif PLOT_MEAS(plot_meas_index+1) == 2
            format='%s/absFlux_%s.pdf';
            print(fig,sprintf(format, PATH_OUTPUT_FIG_PDF, title_in),'-dpdf','-fillpage');
        elseif PLOT_MEAS(plot_meas_index+1) == 3
            format='%s/time_ID_%s.pdf';
            print(fig,sprintf(format, PATH_OUTPUT_FIG_PDF, title_in),'-dpdf','-fillpage');
        elseif PLOT_MEAS(plot_meas_index+1) == 4
            format='%s/time_balance_%s.pdf';
            print(fig,sprintf(format, PATH_OUTPUT_FIG_PDF, title_in),'-dpdf','-fillpage');
        else
            format='%s/number_iterations_%s.pdf';
            print(fig,sprintf(format, PATH_OUTPUT_FIG_PDF, title_in),'-dpdf','-fillpage');
        end
    end
end


