google.charts.load('current', {'packages':['bar']});
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {
        viz_table = [['Employee', 'to-do', 'in-progress', 'completed']]
        for (var user in users_tasks) {
            viz_table.push([user, parseInt(users_tasks[user][0]), parseInt(users_tasks[user][1]), parseInt(users_tasks[user][2]) ])
        }
        var data = google.visualization.arrayToDataTable(viz_table);

        var options = {
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

        var chart = new google.charts.Bar(document.getElementById('workload'));

        chart.draw(data, google.charts.Bar.convertOptions(options));
      }