clear;
load('resnet101.mat')
price = log(double(price'));
acc5 = double(acc5');
category = double(category');

cat_num = length(unique(category));
means = zeros(cat_num, 1);
counts = zeros(cat_num, 1);
stds = zeros(cat_num, 1);
for i=1:cat_num
    vec = acc5(category == (i-1));
    means(i) = mean(vec);
    counts(i) = length(vec);
    stds(i) = sqrt(means(i)*(1-means(i))/length(vec));
end

norm_acc = zeros(size(acc5));
for i=1:length(acc5)
    cat = category(i)+1;
    norm_acc(i) = (acc5(i) - means(cat))/stds(cat);
end

x = price;
y = norm_acc;
X = [ones(length(x), 1), x];

plot(x, y, 'o', 'Displayname', 'Data')
hold on

[b, bint, r, rint, stats] = regress(y, X);
xfit = min(x):0.01:max(x);
yfit = b(1) + b(2)*xfit;
plot(xfit, yfit, '-k', 'Displayname', 'linear', 'linewidth', 5);

xlabel('log(Income) ($)');
ylabel('Norm Acc.');
hold off

lgd = legend('Location', 'southeast');
set(gca, 'FontSize', 20)
set(gcf, 'PaperUnits', 'inches');
set(gcf, 'PaperSize', [6.5 5]);

print('-f1', 'norm_scatter.png', '-dpng')
%print('-f1', 'norm_scatter.pdf', '-dpdf', '-fillpage');


