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

best_accuracy = 0;
best_forest_size = 0;
for i= 10:10:50
  forest = TreeBagger(i, trainData, trainLabels);
  output = predict(forest, testData);
  output_labels = str2double(output);
  accuracy = count(testLabels, output_labels);
  if accuracy > best_accuracy
      best_accuracy = accuracy;
      best_forest_size = i;
  end
end

