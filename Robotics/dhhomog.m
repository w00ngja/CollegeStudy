clc;clear;close all;
theta_z = zeros(1,7);
distance_z = [340 0 400 0 400 0 126];
theta_x = [-pi/2 pi/2 pi/2 -pi/2 -pi/2 pi/2 0];
distance_x = zeros(1,7);

% theta_z(1) = pi/3;
% theta_z(2) = pi/4;
% theta_z(3) = 0;
% theta_z(4) = pi/4;
% theta_z(5) = pi/3;
% theta_z(6) = pi/4;
% theta_z(7) = 0;

theta_z(1) = 0;
theta_z(2) = 0;
theta_z(3) = 0;
theta_z(4) = -90;
theta_z(5) = 0;
theta_z(6) = 0;
theta_z(7) = 0;

A = zeros(4,4,7);
for i=1:7
    t = theta_z(i);
    d = distance_z(i);
    a = theta_x(i);
    l = distance_x(i);

    Ct = cos(t);
    St = sin(t);
    Ca = cos(a);
    Sa = sin(a);

    A(:,:,i) = [Ct -St*Ca St*Sa l*Ct;
        St Ct*Ca -Ct*Sa l*St;
        0 Sa Ca d;
        0 0 0 1];

end

A_1 = A(:,:,1);
A_2 = A(:,:,2);
A_3 = A(:,:,3);
A_4 = A(:,:,4);
A_5 = A(:,:,5);
A_6 = A(:,:,6);
A_7 = A(:,:,7);

T_0 = eye(4);
T_1 = A_1;
T_2 = A_1*A_2;
T_3 = A_1*A_2*A_3;
T_4 = A_1*A_2*A_3*A_4;
T_5 = A_1*A_2*A_3*A_4*A_5;
T_6 = A_1*A_2*A_3*A_4*A_5*A_6;
T_7 = A_1*A_2*A_3*A_4*A_5*A_6*A_7;


[P_0,R_0] = TransToState(T_0);
[P_1,R_1] = TransToState(T_1);
[P_2,R_2] = TransToState(T_2);
[P_3,R_3] = TransToState(T_3);
[P_4,R_4] = TransToState(T_4);
[P_5,R_5] = TransToState(T_5);
[P_6,R_6] = TransToState(T_6);
[P_7,R_7] = TransToState(T_7);

Position=[P_0,P_1,P_2,P_3,P_4,P_5,P_6,P_7];
figure(10);
plot3(Position(1,:),Position(2,:),Position(3,:),'Color','k','LineWidth',3)
hold on;

p0 = plot3(P_0(1),P_0(2),P_0(3),'-o','Color','b','MarkerSize',15,'MarkerFaceColor','r');
p1 = plot3(P_1(1),P_1(2),P_1(3),'-o','Color','b','MarkerSize',15,'MarkerFaceColor','m');
p2 = plot3(P_2(1),P_2(2),P_2(3),'-o','Color','b','MarkerSize',15,'MarkerFaceColor','c');
p3 = plot3(P_3(1),P_3(2),P_3(3),'-o','Color','b','MarkerSize',15,'MarkerFaceColor','b');
p4 = plot3(P_4(1),P_4(2),P_4(3),'-o','Color','b','MarkerSize',15,'MarkerFaceColor','y');
p5 = plot3(P_5(1),P_5(2),P_5(3),'-o','Color','b','MarkerSize',15,'MarkerFaceColor','g');
p6 = plot3(P_6(1),P_6(2),P_6(3),'-o','Color','b','MarkerSize',15,'MarkerFaceColor','w');
p7 = plot3(P_7(1),P_7(2),P_7(3),'-o','Color','b','MarkerSize',15,'MarkerFaceColor','k');

legend([p0 p1 p2 p3 p4 p5 p6 p7],['X_0','X_1','X_2','X_3','X_4','X_5','X_6','X_7'])
grid on;
title('FK');
xlabel('X[mm]')
ylabel('Y[mm]')
zlabel('Z[mm]')
view(135,20);
set(gca,'FontSize',20);
axis equal
xlim([-950 950]);
ylim([-950 950]);
zlim([0 1300])

Target_T7 = T_7;
Target_T4 = T_4;
save 'target.mat' Target_T7
save 'target0.mat' Target_T7


function [P, R] = TransToState(T)
    P = T(1:3, 4);
    R = T(1:3, 1:3);
end