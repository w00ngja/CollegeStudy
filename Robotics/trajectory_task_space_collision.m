clc; clear; close all;

robot = loadrobot('quanserQArm',DataFormat="row")

init_angle = [1 0.5 0 0];
show(robot,init_angle);
showdetails(robot)
xlim([-0.5 0.5]); ylim([-0.5 0.5]); zlim([0 0.75]);
title("Quanser-Qarm")
hold on;

%% ik
ik = inverseKinematics('RigidBodyTree',robot);
ikWeights = [0 0 0 1 1 1];
ikInitGuess = robot.homeConfiguration;

ikInitGuess(ikInitGuess > pi) = ikInitGuess(ikInitGuess > pi) - 2*pi;
ikInitGuess(ikInitGuess < -pi) = ikInitGuess(ikInitGuess < -pi) + 2*pi;


%% 상태공간 및 유효성 검사
ss = manipulatorStateSpace(robot);
sv = manipulatorCollisionBodyValidator(ss,SkippedSelfCollisions="parent")

sv.ValidationDistance = 1
sv.IgnoreSelfCollision = true

importenv()