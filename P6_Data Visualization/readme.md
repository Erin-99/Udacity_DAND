总结：本次使用D3.js与dimple.js技术进行可视化，优势在于可视化的每个细节都可以代码级别调整，可以动态交互，同时可方便的在网页端展示。劣势在于本次项目遇到的问题
数据集较大绘制点过多时，执行效率差，数据处理能力弱。比不上现成的可视化工具，诸如teabluea、甚至Excel这样的工具。
设计：本次设计根据美国政府网站上提供的洛杉矶2010年至今的犯罪数据，观察不同犯罪类型犯罪时间的特征。此数据集有超过150万条数据，为了可视化的效果，已将数据提前聚合，并只取了犯罪记录最多的5种类型近三年（2014年，2015年和2016年）的数据。在数据展示上，x轴为犯罪年份，y轴为一天24小时，将犯罪类型作为筛选项，用气泡的大小表示此类犯罪在特定年份特定时间发生的次数。点击右侧列表可以查看这一类型犯罪的数据显示。鼠标悬停可以显示此数据点的具体信息，如犯罪类型，年份，犯罪时间及次数。
反馈：由于数据量大，动态交互有一定的延迟现象。
资源：此次数据可视化参考了dimple官网的数据展示http://dimplejs.org/advanced_examples_viewer.html?id=advanced_storyboard_control；
网页内容格式参考了jasonbai同学的样板http://localhost:8088/workspace/movie.html#two