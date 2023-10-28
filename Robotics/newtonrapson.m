% 로봇 팔의 길이
L = [1 1];

% 목표 위치
target = [1.5; 0.5; 0];

% 초기 관절 각도
theta = [0; 0; 0];

% 반복 횟수
iteration = 1000;

% 학습률
alpha = 0.1;

for i = 1:iteration
    % 현재 위치 계산
    pos = [L(1)*cos(theta(1)) + L(2)*cos(theta(1)+theta(2));
           L(1)*sin(theta(1)) + L(2)*sin(theta(1)+theta(2));
           0];

    % 에러 계산
    e = target - pos;

    % Jacobian 행렬 계산
    J = [-L(1)*sin(theta(1)) - L(2)*sin(theta(1)+theta(2)), -L(2)*sin(theta(1)+theta(2)), 0;
          L(1)*cos(theta(1)) + L(2)*cos(theta(1)+theta(2)),  L(2)*cos(theta(1)+theta(2)), 0;
          0, 0, 1];

    % 업데이트
    theta = theta + alpha * (pinv(J) * e);
    
    % 시각화
    clf;
    plot3([0, L(1)*cos(theta(1)), pos(1)], [0, L(1)*sin(theta(1)), pos(2)], [0, 0, pos(3)], '-o');
    hold on;
    plot3(target(1), target(2), target(3), 'r*');
    xlim([-2 2]);
    ylim([-2 2]);
    zlim([-2 2]);
    drawnow;
end
