function [ total , accuracy ] = class_accuracy( test_labels , output_labels)
%CLASS_ACCURACY Summary of this function goes here
%   Detailed explanation goes here

len = size(unique(test_labels) , 1);

incorrect = zeros(len,1);
correct = zeros(len,1);
for i=1:size(test_labels)
    class = test_labels(i);
    if test_labels(i) == output_labels(i)
       correct(class) = correct(class) + 1;
    else      
       incorrect(class) = incorrect(class) + 1;
    end
end

accuracy = zeros(len,1);
total = zeros(len,1);
for i=1:size(correct)
    accuracy(i) = correct(i) / (correct(i) + incorrect(i));
    total(i) = correct(i) + incorrect(i);
end

end

