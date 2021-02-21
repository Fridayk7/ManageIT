google.charts.load('current', {packages: ['corechart']});
function drawChart() {
            // Define the chart to be drawn.

            viz_table = [['Day', 'Tasks Remaining', 'Tasks Completed']]
            for (var date in journey) {
                viz_table.push([date, parseInt(journey[date][0]), parseInt(journey[date][1])])
            }
            var data = google.visualization.arrayToDataTable(viz_table);

            var options = {title: 'Task Burndown',
            isStacked:true,
            'backgroundColor': 'transparent',
            animation: {
                duration: 1500,
                startup: true //This is the new option
            },
            hAxis: {
                textStyle:{color: '#FFF'}
            },
            legendTextStyle: { color: '#FFF' },
            };

            // Instantiate and draw the chart.
            var chart = new google.visualization.ColumnChart(document.getElementById('burndown'));
            chart.draw(data, options);
         }
         google.charts.setOnLoadCallback(drawChart);