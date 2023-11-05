%%  Give the number of features, and how far ahead we are predicting
numFilesUsed = 5;
PredictAheadBy = 4;


%%
tb_india = readtable('tb_dataset_india.csv');
tb_uttar = readtable('tb_dataset_uttar_pradesh.csv');
tb_gujarat =  readtable('tb_dataset_gujarat.csv');
tb_maharashtra = readtable('tb_dataset_maharashtra.csv')
tb_trend  = readtable('Interest in TB India.csv')
%%
tb_uttar(:,"Var1") = []
tb_uttar(:,"Var2") = []
tb_uttar(1,:) = []
tb_maharashtra(:,"Var1") = []
tb_maharashtra(:,"Var2") = []
tb_maharashtra(1,:) = []
tb_gujarat(:,"Var1") = []
tb_gujarat(:,"Var2") = []
tb_gujarat(1,:) = []
tb_trend(:,"Dates") = []
tb_india(:,"Var1") = []
tb_india(:,"Dates") = []


%%


data = [tb_india{:,:},tb_uttar{:,:}',tb_gujarat{:,:}',tb_maharashtra{:,:}',tb_trend{:,:}];
data (isnan(final_data ))=0; %replace NaN values with 0

%%standardized Data
final_data = zscore(data);

%%Get Training and Test data
numTimeStepsTrain = floor(0.75*size(final_data, 1));
trainData = final_data(1:numTimeStepsTrain+1, :);
testData = final_data(numTimeStepsTrain:end, :);

%%Prep predictors
XTrain = trainData(1:end-PredictAheadBy,:)';
YTrain = trainData((PredictAheadBy+1):end,1)';

%%
 
%%LSTM Network training
numFeatures = numFilesUsed;
numResponses = 1;
numHiddenUnits = 327;
layers = [...
    sequenceInputLayer(numFeatures)
    lstmLayer(numHiddenUnits)
    fullyConnectedLayer(numResponses)
    regressionLayer];

options = trainingOptions('adam', ...
    'MaxEpochs', 200, ...
    'GradientThreshold', 1, ...
    'InitialLearnRate', 0.005, ...
    'LearnRateSchedule', 'piecewise', ...
    'LearnRateDropPeriod', 125, ...
    'LearnRateDropFactor', 0.1, ...
    'Verbose', 0, ...
    'Plots','training-progress');

net = trainNetwork(XTrain, YTrain, layers, options);
%% Opperations on Trained Network

%%Prepare test data
XTest = testData(1:end-PredictAheadBy,:);
YTest = testData((PredictAheadBy+1):end,1);

YPred = predict(net, XTest')';

figure
hold on
plot(YTest)
plot(YPred)
xlabel('Weeks')
ylabel('Z-score of Influenza Positive Viruses')
legend('actual ', 'predicted')
hold off
%%
tbRes = (YPred * std(final_data(:,1))) + mean(final_data(:,1));
tbAct = data(numTimeStepsTrain+PredictAheadBy:end,1);

err = sqrt(immse(double(tbRes), tbAct));
%%
% figure
% hold on
% plot(iliAct)
% plot(iliRes, 'r')
% plot(iliRes+err, 'r--')
% plot(iliRes-err, 'r--')
% xlabel('Weeks')
% ylabel('ILI Cases')
% legend({'actual ', 'predicted', 'confidence intervals'}, 'Location', 'northwest')
% hold off

mapeSum = 0;
sum2 = 0;

for yRow = 1: length(YPred)

    mapeSum = mapeSum + abs(tbRes(yRow) - tbAct(yRow));
    sum2 = sum2 + (tbRes(yRow) + tbAct(yRow));

end
mapeSum/sum2


