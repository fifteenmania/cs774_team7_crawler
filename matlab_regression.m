load('resnet101.mat')
price = log(double(price'));
acc5 = double(acc5');
conf = double(conf');
cent = -log(conf);

y = acc5;
x = price;
bin_cnt = 1;

[out, idx] = sort(x);
l = length(x) - rem(length(x), bin_cnt);
x = x(idx);
y = y(idx);
x = mean(reshape(x(1:l), [], bin_cnt), 2);
y = mean(reshape(y(1:l), [], bin_cnt), 2);
%%

X = [ones(length(x), 1), x];

plot(x, y, 'o', 'Displayname', 'Data')
hold on

[b, bint, r, rint, stats] = regress(y, X);
xfit = min(x):0.01:max(x);
yfit = b(1) + b(2)*xfit;
plot(xfit, yfit, '-k','Displayname', 'linear', 'linewidth', 5);

xlabel('log(Income) ($)');
ylabel('Top 5 Acc.');
hold off

lgd = legend('Location', 'southeast');
set(gca, 'FontSize', 20)
set(gcf, 'PaperUnits', 'inches');
set(gcf, 'PaperSize', [6.5 5]);

print('-f1', 'raw_scatter.png', '-dpng')
%print('-f1', 'raw_scatter.pdf', '-dpdf', '-fillpage');
