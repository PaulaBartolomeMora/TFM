%% Entregable 1 - Transformación de una Señal de Audio
%
%   [+] Autor: David Carrascal <david.carrascal@uah.es> 
%
%   [+] Fecha: 18 Feb 2021
clc;
close all;
clear variables;

%% Main

% Definimos los limites de la funcion de densidad de probabilidad uniforme 
a=-4;
b=4;

% Pillamos la PDF
pd2 = makedist('Uniform','lower',-4,'upper',4); % Uniform distribution with a = -2 and b = 2


% Sacamos los puntos de la PDF
x = -6:.01:6;
pdf2 = pdf(pd2,x);

% Plot bueno bueno 
% paper_size = [18 20];
% paper_position = [0.25 0 14-0.25 15.99];
set(groot,'defaultAxesTickLabelInterpreter','latex'); 
fig = figure();
% fig.PaperOrientation='landscape';
% fig.PaperSize=paper_size;
% fig.Units = 'centimeters';
% fig.PaperPosition = paper_position;

plot(x,pdf2,'-','Color','#D95319','LineWidth',1.5);
grid minor;
xlim([-6 6]);
ylim([0 ((1/(b-a)) + 0.1 )]);
yticks([0 0.05 0.1 0.1250 0.15 0.2])
yticklabels({'0','0.05','0.1','$\frac{1}{b-a}$','0.15','0.2'})
title('Probability density function for Load generation ','Interpreter','latex')
legend({'$a = -4, b = 4$'},'Interpreter','latex','Location','northwest');
xlabel('Observation')
ylabel('Probability Density')
%print(fig,sprintf('fig.pdf', '', 'fig'),'-dpdf','-fillpage');
