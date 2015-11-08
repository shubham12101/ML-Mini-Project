clear
clc

% ========== CONSTANTS ===========
TRAIN_DATA_FILE = '../process_data/train_features.csv';
TEST_DATA_FILE = '../process_data/test_final_features.csv';

% ========= READ DATA ========
trainData = csvread(TRAIN_DATA_FILE);
testData = csvread(TEST_DATA_FILE);

trainLabels = trainData(:,6);
testLabels = testData(:,6);

trainData = trainData(:,1:5);
testData = testData(:,1:5);

lenTrain = size(trainData,1);
lenTest = size(testData,1);
numUnique = size(unique(trainLabels),1);

nnTrainLabels = zeros(lenTrain, numUnique);
nnTestLabels = zeros(lenTest, numUnique);

for i=1:lenTrain
    nnTrainLabels(i, trainLabels(i)) = 1;
end

for i=1:lenTest
    nnTestLabels(i, testLabels(i)) = 1;
end

% nnstart();

trainInputs = trainData.';
trainTargets = nnTrainLabels.';
testInputs = testData.';
testTargets = nnTestLabels.';

% Create a Pattern Recognition Network
hiddenLayerSize = [50,10];
net = patternnet(hiddenLayerSize);
net.trainParam.epochs = 100;


% % Set up Division of Data for Training, Validation, Testing
net.divideParam.trainRatio = 90/100;
net.divideParam.valRatio = 5/100;
net.divideParam.testRatio = 5/100;

% Train the Network
[net,tr] = train(net,trainInputs,trainTargets);

% Test the Network
outputs = net(trainInputs);
% display(outputs);
errors = gsubtract(trainTargets,outputs);
performance = perform(net,trainTargets,outputs);

% View the Network
view(net)

% Plots
% Uncomment these lines to enable various plots.
% figure, plotperform(tr)
% figure, plottrainstate(tr)
% figure, plotconfusion(targets,outputs)
% figure, ploterrhist(errors)

