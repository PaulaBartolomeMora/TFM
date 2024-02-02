%% Función para pasar los timepos a ms

function tiempos_ms = seg2mseg_Multiroot(matriz)
    matriz(:,end-2:end-1) = matriz(:,end-2:end-1) .* 1000;
    tiempos_ms = matriz;
end
