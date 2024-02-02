%% Función para pasar los timepos a ms

function tiempos_ms = seg2mseg(matriz)
    matriz(:,end-1:end) = matriz(:,end-1:end) .* 1000;
    tiempos_ms = matriz;
end