clc; clear; close all;

robot = importrobot("DoF2.slx")

init_angle = [1 0.5 0 0];
show(robot,init_angle);
showdetails(robot)
xlim([-0.5 0.5]); ylim([-0.5 0.5]); zlim([0 0.75]);
title("Quanser-Qarm")
hold on;