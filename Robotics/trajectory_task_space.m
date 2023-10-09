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

%% waypoint
waypoints = [ 0.2  0.2 0.3;
              0.35 0.1 0.1;
              0.35 0 0.2;
              0.35 -0.2   0.3  ;
              -0.1 -0.2   0.3  ]

%% time
waypointTimes = 0:4:16;
ts = 0.5;
trajTimes = 0:ts:waypointTimes(end);

waypointsVels = 0.1 * [0 1 0;
                      -1 0 0;
                      0 -1 0;
                      1 0 0;
                      0 1 0]';

numWaypoints = size(waypoints,1);
numJoints = numel(robot.homeConfiguration);
jointWaypoints = zeros(numJoints,numWaypoints);

%% spline
[q,qd,qdd] = cubicpolytraj(waypoints',waypointTimes,trajTimes, ...
    "VelocityBoundaryCondition",waypointsVels);

for idx = 1:size(q,2)

    tgtPose = trvec2tform(q(:,idx)');

    [config,info] = ik("END-EFFECTOR",tgtPose,ikWeights,ikInitGuess);
    taskWaypoints(:,idx) = config';
    ikInitGuess = config;
end

for idx = 1:numel(trajTimes)
    config = taskWaypoints(:,idx)';

    eeTform = getTransform(robot, config,"END-EFFECTOR");

    plotTransforms(tform2trvec(eeTform),tform2quat(eeTform),"FrameSize",0.05);

        % show robot
    show(robot,config,'Frames','on','PreservePlot',false);
    plot3(waypoints(:,1),waypoints(:,2),waypoints(:,3),'o',MarkerSize=7,MarkerFaceColor='b', ...
        ColorMode='auto');
    title(['t = ' num2str(trajTimes(idx))])
    drawnow
end