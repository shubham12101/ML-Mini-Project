clear
clc

% ========== CONSTANTS ===========
TRAIN_DATA_FILE = '../process_data/feature_train.csv';
TEST_DATA_FILE = '../process_data/feature_test.csv';

% ========= READ DATA ========
trainData = csvread(TRAIN_DATA_FILE);
testData = csvread(TEST_DATA_FILE);

trainLabels = trainData(:,6);
testLabels = testData(:,6);

trainData = trainData(:,1:5);
testData = testData(:,1:5);

% ======== TRAIN MODELS============
A = TreeBagger(10, trainData, trainLabels);

correct = 0;
incorrect = 0;
validCountVector = zeros(7,1);
classAccuracyMat = zeros(7,11);
k=1;

for i=1:292683
    ret = A.predict(testData(i,:));
    retClass = str2double(ret);
%         fprintf('retClass=%f, testLabelMat(i,1)=%f',retClass, testLabelMat(i,1));
%         fprintf('\n');
    if retClass == testLabels(i,1)
        validCountVector(testLabelMat(i,1),1) = validCountVector(testLabelMat(i,1),1) + 1;
        correct = correct + 1;
    else
        incorrect = incorrect + 1;
    end
end

for j=1:7
   classAccuracyMat(j,k) = validCountVector(j,1)/30; 
end

display(validCountVector);
display(classAccuracyMat);

accuracyMat(1,k) = correct/210;
k = k+1;

% bar(accuracyMat);
% bar(classAccuracyMat);
