%% Función para calcular el intervalo de confianza
%
%   [+] Autor: Joaquin Alvarez <j.alvarez@uah.es> 
%
%   [+] Fecha: 22 Dic 2021

function [intervalo] = confidence_interval(num_repeticiones, medias)
    grados_libertad=(num_repeticiones-1);
    tstudent=(tinv([0.025 0.975],grados_libertad));
    intervalo = (tstudent(2).* std(medias))./sqrt(grados_libertad);    
end

