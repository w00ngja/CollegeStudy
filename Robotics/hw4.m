% 초기값
dt = 0.1;
d = 0.5;
theta = 0;
X = [0; 0];
path = X;

% 노이즈 초기값
theta_noisy = 0;
X_noisy = X;
path_noisy = X_noisy;

% 선속도
Vl = [ones(1, 100),  ones(1, 8), ones(1, 120),ones(1, 8), ones(1, 100)];
Vr = [ones(1, 100), zeros(1, 8), ones(1, 120),zeros(1, 8), ones(1, 100)];

% 총 동작 횟수만큼 반복
for t = 1:length(Vl)
    V = (Vr(t) + Vl(t)) / 2;
    w = (Vr(t) - Vl(t)) / d;

    % 상태 갱신
    X = X + dt*[V*cos(theta); V*sin(theta)];
    theta = theta + dt*w;

    % 노이즈 추가
    V_noisy = V + 0.3*randn;
    w_noisy = w + 0.3*randn;
    X_noisy = X_noisy + dt*[V_noisy*cos(theta_noisy); V_noisy*sin(theta_noisy)];
    theta_noisy = theta_noisy + dt*w_noisy;

    path = [path, X];
    path_noisy = [path_noisy, X_noisy];
end

% GPS 센서 임의 데이터
sensor_noise_std = 0.4;
num_sensor_points_per_path_point = 5;

sensor_points = [];


for i = 1:size(path, 2)
    for j = 1:num_sensor_points_per_path_point
        sensor_point = path(:, i) + sensor_noise_std*randn(2, 1);

        sensor_points = [sensor_points, sensor_point];
    end
end

% 자코비안
syms x y theta V dt
g1 = x + dt*V*cos(theta);
g2 = y + dt*V*sin(theta);
g3 = theta;

G = jacobian([g1; g2; g3], [x, y, theta]);

% 그래프
plot(path(1,:), path(2,:), 'b', 'LineWidth', 4);
hold on;
plot(path_noisy(1,:), path_noisy(2,:), 'r', 'LineWidth', 2);
plot(sensor_points(1,:), sensor_points(2,:), 'g.', 'MarkerSize', 5);
hold off;

xlabel('X');
ylabel('Y');
title('Robot Trajectory');
legend('Ground Truth', 'Just Predict', 'GPS');
