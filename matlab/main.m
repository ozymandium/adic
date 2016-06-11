%% main function for Allan Variance Tests
clear all;
close all;clc;
addpath('matlab_rosbag/')

gvlab = 0; span = 0; sim = 0;

runAllanVarSpan = 0; loadAllanVarSpan = 1;
runAllanVarSim = 0; loadAllanVarSim = 1;

%% Load Bag Data
if (gvlab)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%          Gavlab HG1700         %%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
HG_gvlab.filename = ['/Users/salmonc/devel/AllanVar_matlab/Data/'...
                        'HG_Static/HG1700_gvlab/2016-04-21-10-37-59.bag'];
HG_gvlab.bag = ros.Bag.load(HG_gvlab.filename);
HG_gvlab.bag.info()

HG_gvlab.idx = 1;
HG_gvlab.bag.resetView({'/HG1700Imu'});
HG_gvlab.Imu.Time = zeros(8716866,1);
HG_gvlab.Imu.Acc = zeros(8716866,3);
HG_gvlab.Imu.Gyro = zeros(8716866,3);
while HG_gvlab.bag.hasNext()
    [HG_gvlab.msg,HG_gvlab.meta] = HG_gvlab.bag.read();
    if (strcmp(HG_gvlab.meta.topic,'/HG1700Imu'))
        HG_gvlab.Imu.Time(HG_gvlab.idx,1) = cast(HG_gvlab.msg.header.stamp.sec,'double') +...
            cast(HG_gvlab.msg.header.stamp.nsec,'double') * 1e-9;
        HG_gvlab.Imu.Acc(HG_gvlab.idx,1:3) = HG_gvlab.msg.linear_acceleration;
        HG_gvlab.Imu.Gyro(HG_gvlab.idx,1:3) = HG_gvlab.msg.angular_velocity;
        
        HG_gvlab.idx = HG_gvlab.idx + 1;
    end
end

HG_GvLab_Imu_Acc = [HG_gvlab.Imu.Time, HG_gvlab.Imu.Acc];
HG_GvLab_Imu_Gyro = [HG_gvlab.Imu.Time, HG_gvlab.Imu.Gyro];

save HG_Gvlab_Acc.mat HG_GvLab_Imu_Acc -v7.3
save HG_Gvlab_Gyro.mat HG_GvLab_Imu_Gyro -v7.3

clear HG_gvlab HG_GvLab_Imu_Acc HG_GvLab_Imu_Gyro
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%          SPAN HG1700         %%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if (span)
HG_span.filename = ['/Users/salmonc/devel/AllanVar_matlab/Data/'...
                        'HG_Static/SPAN/24Hour_Static_AG58.bag'];
HG_span.bag = ros.Bag.load(HG_span.filename);
HG_span.bag.info()

HG_span.idx = 1;
HG_span.bag.resetView({'/novatel_node/imu'});
HG_span.Imu.Time = zeros(8789225,1);
HG_span.Imu.Acc = zeros(8789225,3);
HG_span.Imu.Gyro = zeros(8789225,3);
while HG_span.bag.hasNext()
    [HG_span.msg,HG_span.meta] = HG_span.bag.read();
    if (strcmp(HG_span.meta.topic,'/novatel_node/imu'))
        if HG_span.idx == 1
        spanTime1 = cast(HG_span.msg.header.stamp.sec,'double');
        end
        HG_span.Imu.Time(HG_span.idx,1) = cast(HG_span.msg.header.stamp.sec,'double') -...
            spanTime1 +...
            cast(HG_span.msg.header.stamp.nsec,'double') * 1e-9;
        HG_span.Imu.Acc(HG_span.idx,1:3) = HG_span.msg.linear_acceleration;
        HG_span.Imu.Gyro(HG_span.idx,1:3) = HG_span.msg.angular_velocity;
        
        HG_span.idx = HG_span.idx + 1;
    end
end
HG_Span_Imu_Acc = [HG_span.Imu.Time, HG_span.Imu.Acc];
HG_Span_Imu_Gyro = [HG_span.Imu.Time, HG_span.Imu.Gyro];

save HG_Span_Acc.mat HG_Span_Imu_Acc -v7.3
save HG_Span_Gyro.mat HG_Span_Imu_Gyro -v7.3

clear HG_span HG_Span_Imu_Acc HG_Span_Imu_Gyro
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%            IS4S SIM             %%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if (sim)
HG_sim.filename = ['/Users/salmonc/devel/Ros_Nav_ws/Bag_Data/'...
    'Tests/StaticSim/NavSimOut_Static_12Hr_100Hz.bag'];
HG_sim.bag = ros.Bag.load(HG_sim.filename);
HG_sim.bag.info()

HG_sim.idx = 1;
HG_sim.bag.resetView({'/SimImu/Imu'});

HG_sim.Imu.Time = zeros(4318761,1);
HG_sim.Imu.Acc = zeros(4318761,3);
HG_sim.Imu.Gyro = zeros(4318761,3);
while HG_sim.bag.hasNext()
    [HG_sim.msg,HG_sim.meta] = HG_sim.bag.read();
    if (strcmp(HG_sim.meta.topic,'/SimImu/Imu'))
        HG_sim.Imu.Time(HG_sim.idx,1) = cast(HG_sim.msg.header.stamp.sec,'double') +...
            cast(HG_sim.msg.header.stamp.nsec,'double') * 1e-9;
        HG_sim.Imu.Acc(HG_sim.idx,1:3) = HG_sim.msg.linear_acceleration;
        HG_sim.Imu.Gyro(HG_sim.idx,1:3) = HG_sim.msg.angular_velocity;
        
        HG_sim.idx = HG_sim.idx + 1;
    end
end
HG_Sim_Imu_Acc = [HG_sim.Imu.Time, HG_sim.Imu.Acc];
HG_Sim_Imu_Gyro = [HG_sim.Imu.Time, HG_sim.Imu.Gyro];

save HG_Sim_Acc.mat HG_Sim_Imu_Acc -v7.3
save HG_Sim_Gyro.mat HG_Sim_Imu_Gyro -v7.3

clear HG_sim HG_Sim_Imu_Acc HG_Sim_Imu_Gyro
end

%% Allan Variance Analysis
% load('HG_Gvlab_Acc.mat');
% load('HG_Gvlab_Gyro.mat');

if runAllanVarSpan
load('HG_Span_Acc.mat');
load('HG_Span_Gyro.mat');

[Tau_Span_Gyro,Sigma_Span_Gyro,Sigma2_Span_Gyro]=allan_2(HG_Span_Imu_Gyro(:,2:4),100, 10000);
save Tau_Span_Gyro.mat Tau_Span_Gyro -v7.3
save Sigma_Span_Gyro.mat Sigma_Span_Gyro -v7.3
[Tau_Span_Acc,Sigma_Span_Acc,Sigma2_Span_Acc]=allan_2(HG_Span_Imu_Acc(:,2:4),100, 10000);
save Tau_Span_Acc.mat Tau_Span_Acc -v7.3
save Sigma_Span_Acc.mat Sigma_Span_Acc -v7.3
elseif loadAllanVarSpan
load('Sigma_Span_Acc.mat');
load('Sigma_Span_Gyro.mat');
load('Tau_Span_Acc.mat');
load('Tau_Span_Gyro.mat');
end

if runAllanVarSim
load('HG_Sim_Acc.mat');
load('HG_Sim_Gyro.mat');

[Tau_Sim_Acc,Sigma_Sim_Acc,Sigma2_Sim_Acc]=allan_2(HG_Sim_Imu_Acc(:,2:4),100, 10000);
save Tau_Sim_Acc.mat Tau_Sim_Acc -v7.3
save Sigma_Sim_Acc.mat Sigma_Sim_Acc -v7.3
[Tau_Sim_Gyro,Sigma_Sim_Gyro,Sigma2_Sim_Gyr]=allan_2(HG_Sim_Imu_Gyro(:,2:4),100, 10000);
save Tau_Sim_Gyro.mat Tau_Sim_Gyro -v7.3
save Sigma_Sim_Gyro.mat Sigma_Sim_Gyro -v7.3
elseif loadAllanVarSim
load('Sigma_Sim_Acc.mat');
load('Sigma_Sim_Gyro.mat');
load('Tau_Sim_Acc.mat');
load('Tau_Sim_Gyro.mat');
end


%% Visualization
figure(1);
loglog(Tau_Span_Gyro,Sigma_Span_Gyro)
grid on;
title('SPAN Gyros')

figure(2);
loglog(Tau_Span_Acc,Sigma_Span_Acc)
grid on;
title('SPAN Accels')

figure(2);hold on;
loglog(Tau_Sim_Acc,Sigma_Sim_Acc)
grid on;
title('Accels')
legend('Span X','Span Y','Span Z','Sim X','Sim Y','Sim Z','location','northeast')

figure(1);hold on;
loglog(Tau_Sim_Gyro,Sigma_Sim_Gyro)
grid on;
title('Gyros')
legend('Span X','Span Y','Span Z','Sim X','Sim Y','Sim Z','location','northeast')


return;
%% Accel Plot
figure;subplot(3,1,1);
plot(HG_GvLab_Imu_Acc(:,1)-HG_GvLab_Imu_Acc(1,1),HG_GvLab_Imu_Acc(:,4),'.');
grid on;hold on;
plot(HG_Span_Imu_Acc(:,1)-HG_Span_Imu_Acc(1,1),HG_Span_Imu_Acc(:,2),'.');
plot(HG_Sim_Imu_Acc(:,1)-HG_Sim_Imu_Acc(1,1), HG_Sim_Imu_Acc(:,2),'.');
title('HG Accels');legend('Gavlab','SPAN','SIM','location','SouthEastOutside')
ylabel('X Accel (m/s2)')

subplot(3,1,2)
plot(HG_GvLab_Imu_Acc(:,1)-HG_GvLab_Imu_Acc(1,1),HG_GvLab_Imu_Acc(:,3),'.');
grid on;hold on
plot(HG_Span_Imu_Acc(:,1)-HG_Span_Imu_Acc(1,1),HG_Span_Imu_Acc(:,3),'.');
plot(HG_Sim_Imu_Acc(:,1)-HG_Sim_Imu_Acc(1,1), HG_Sim_Imu_Acc(:,3),'.');
ylabel('Y Accel (m/s2)')

subplot(3,1,3)
plot(HG_GvLab_Imu_Acc(:,1)-HG_GvLab_Imu_Acc(1,1),HG_GvLab_Imu_Acc(:,2),'.');
grid on;hold on;
plot(HG_Span_Imu_Acc(:,1)-HG_Span_Imu_Acc(1,1),HG_Span_Imu_Acc(:,4),'.');
plot(HG_Sim_Imu_Acc(:,1)-HG_Sim_Imu_Acc(1,1), HG_Sim_Imu_Acc(:,4),'.');
xlabel('Time (s)');ylabel('Z Accel (m/s2)')

%% Gyro Plot
figure;subplot(3,1,1);
plot(HG_GvLab_Imu_Gyro(:,1)-HG_GvLab_Imu_Gyro(1,1),HG_GvLab_Imu_Gyro(:,4),'.');
grid on;hold on;
plot(HG_Span_Imu_Gyro(:,1)-HG_Span_Imu_Gyro(1,1),HG_Span_Imu_Gyro(:,2),'.');
plot(HG_Sim_Imu_Gyro(:,1)-HG_Sim_Imu_Gyro(1,1), HG_Sim_Imu_Gyro(:,2),'.');
title('HG Gyros');legend('Gavlab','SPAN','SIM','location','SouthEastOutside')
ylabel('X Rot Rate (m/s2)')

subplot(3,1,2)
plot(HG_GvLab_Imu_Gyro(:,1)-HG_GvLab_Imu_Gyro(1,1),HG_GvLab_Imu_Gyro(:,3),'.');
grid on;hold on
plot(HG_Span_Imu_Gyro(:,1)-HG_Span_Imu_Gyro(1,1),HG_Span_Imu_Gyro(:,3),'.');
plot(HG_Sim_Imu_Gyro(:,1)-HG_Sim_Imu_Gyro(1,1), HG_Sim_Imu_Gyro(:,3),'.');
ylabel('Y Rot Rate (m/s2)')

subplot(3,1,3)
plot(HG_GvLab_Imu_Gyro(:,1)-HG_GvLab_Imu_Gyro(1,1),HG_GvLab_Imu_Gyro(:,2),'.');
grid on;hold on;
plot(HG_Span_Imu_Gyro(:,1)-HG_Span_Imu_Gyro(1,1),HG_Span_Imu_Gyro(:,4),'.');
plot(HG_Sim_Imu_Gyro(:,1)-HG_Sim_Imu_Gyro(1,1), HG_Sim_Imu_Gyro(:,4),'.');
xlabel('Time (s)');ylabel('Z Rot Rate (m/s2)')