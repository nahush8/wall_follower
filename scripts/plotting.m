b = load('gpq_epoch_20');
a = load('q_reward_epoch_20');


[n1,p1] = size(a);
[n2,p2] = size(b);
t1 = 1:n1;
t2 = 1:n2;


plot(t1,a);
hold on
plot(t2,b);
hold on

