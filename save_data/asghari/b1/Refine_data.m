% load data
data=readdata('Bosch1.txt');

matrix_data=0;

activity={'Personal_Hygiene','Leave_Home','Enter_Home','Bathing','Meal_Preparation','Sleeping_Not_in_Bed',...
    'Take_Medicine','Eating','Housekeeping','Sleeping_in_Bed','Bed_Toilet_Transition'};
tic
for i=1:size(data,1)
    i
    delimiter='-';
    day=strsplit(data{i,1},delimiter);
    time=strsplit(data{i,2},':');
    sensor_type=data{i,3};
    sensor_status=data{i,4};
    activity_type=data{i,5};
    activity_status=data{i,6};
    
    matrix_data(i,1)=str2num(day{1,1}); 
    matrix_data(i,2)=str2num(day{1,2}); 
    matrix_data(i,3)=str2num(day{1,3}); 
    matrix_data(i,4)=str2num(time{1,1}); 
    matrix_data(i,5)=str2num(time{1,2}); 
    matrix_data(i,6)=round((str2num(time{1,3})),2,'significant');
    
    if sensor_type(1)=='M'
        matrix_data(i,7)=1;
        if strcmp(sensor_status,'ON')
            matrix_data(i,9)=1;
        else
            matrix_data(i,9)=2;
        end
    else
        matrix_data(i,7)=0;
        if strcmp(sensor_status,'OPEN')
            matrix_data(i,9)=3;
        else
            matrix_data(i,9)=4;
        end
        
    end
     matrix_data(i,8)=str2num(sensor_type(2:4));
     
     if strcmp(activity_type,'')
     matrix_data(i,10)=0;
     else
%         activity_type
%         pause(0.2);
       matrix_data(i,10)= find(strcmp(activity,activity_type)==1);
     end
     
     if strcmp(activity_status,'begin')
     matrix_data(i,11)=1;
     elseif strcmp(activity_status,'end')
       matrix_data(i,11)=2;
     elseif strcmp(activity_status,'')
         matrix_data(i,11)=0;
     end
     
end
toc