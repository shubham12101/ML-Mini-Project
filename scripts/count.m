function [ output_args ] = count( test_labels , output_labels )
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
correct = 0;
incorrect = 0;
for i=1:size(test_labels)
    if output_labels(i) == test_labels(i)
        correct = correct + 1;
    else
        incorrect = incorrect + 1;
    end
end
accuracy = correct / (correct + incorrect);
output_args = accuracy;
