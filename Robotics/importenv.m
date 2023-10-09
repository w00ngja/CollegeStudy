function importenv()

box1 = collisionBox(0.1,0.1,0.2);
box1.Pose= trvec2tform([0.2 0.2 0.1])

box2 = collisionBox(0.2,0.2,0.2);
box2.Pose= trvec2tform([0 -0.3 0.1])

box3 = collisionBox(0.1,0.1,0.4);
box3.Pose= trvec2tform([0.35 0 0.2])

env = {box1 box2 box3};
sv.Enviornment = env;

for i=1:length(env)
    show(env{i}); hold on;
end
end