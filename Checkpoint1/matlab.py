//-- ทดสอบการใช้ matlab ในการหาค่าเฉลี่ยและแก้ปัญหาค่า NAN


% Channel ID and API Keys
readChannelID = 2862155;  % Your Channel ID for reading data
readAPIKey = '2C2H8VFRWPVOC8CK'; % Your Read API Key
HALLID = 2;               % Field ID for the data you want to read
writeChannelID = 2862155; % Your Channel ID for writing data
writeAPIKey = 'IZ0IAKMRP61LNRX1'; % Your Write API Key

%% Read Data %%
data = thingSpeakRead(readChannelID, 'Fields', HALLID, 'NumPoints', 10, 'ReadKey', readAPIKey);

display(data);

%% Analyze Data %%
% Add code in this section to analyze data and store the result in the
% 'analyzedData' variable.
avgHall = mean(data); 
display(avgHall, 'Average Hall Data'); 

%% Write Data %%
thingSpeakWrite(writeChannelID, avgHall, 'Fields', 3, 'WriteKey', writeAPIKey);

//แก้ปัญหาค่า NAN

% Channel ID and API Keys
readChannelID = 2861838;  % Your Channel ID for reading data
readAPIKey = '2C2H8VFRWPVOC8CK'; % Your Read API Key
HALLID = 2;               % Field ID for the data you want to read
writeChannelID = 2861838; % Your Channel ID for writing data
writeAPIKey = 'IZ0IAKMRP61LNRX1'; % Your Write API Key

%% Read Data %%
data = thingSpeakRead(readChannelID, 'Fields', HALLID, 'NumPoints', 10, 'ReadKey', readAPIKey);

% Display the raw data
disp('Raw Data:');
disp(data);

% Filter out NaN values before analysis
data = data(~isnan(data)); 

% If the data is empty after filtering, you can set it to a default value
if isempty(data)
    disp('No valid data found!');
    data = 0;  % Set to 0 or another default value if needed
end

%% Analyze Data %%
% Calculate the average, ignoring NaN values
avgHall = mean(data); 
disp('Average Hall Data:');
disp(avgHall);

%% Write Data %%
thingSpeakWrite(writeChannelID, avgHall, 'Fields', 3, 'WriteKey', writeAPIKey);


