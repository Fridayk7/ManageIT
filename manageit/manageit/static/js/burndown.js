google.charts.load('current', {packages: ['corechart']});
function drawChart() {
            // Define the chart to be drawn.
            var data = google.visualization.arrayToDataTable([
               ['Year', 'Asia', 'Europe'],
               ['2012',  900,      390],
               ['2013',  1000,      400],
               ['2014',  1170,      440],
               ['2015',  1250,       480],
               ['2016',  1530,      540]
            ]);
            var options = {title: 'Task Burndown',
            isStacked:true,
            'backgroundColor': 'transparent',
            animation: {
                duration: 1500,
                startup: true //This is the new option
            }
            };

            // Instantiate and draw the chart.
            var chart = new google.visualization.ColumnChart(document.getElementById('burndown'));
            chart.draw(data, options);
         }
         google.charts.setOnLoadCallback(drawChart);