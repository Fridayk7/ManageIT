google.charts.load('current', {'packages':['bar']});

      function drawChart() {
        viz_table = [['Employee', 'to-do', 'in-progress', 'completed']]
        for (var user in users_tasks) {
            viz_table.push([user, parseInt(users_tasks[user][0]), parseInt(users_tasks[user][1]), parseInt(users_tasks[user][2]) ])
        }
        var data = google.visualization.arrayToDataTable(viz_table);

        var options = {
            chartArea: {
                backgroundColor: {
                  fill: 'transparent'
                },
              },
            backgroundColor: 'transparent',
            hAxis: {
                textStyle:{color: '#FFF'}
            },
            legendTextStyle: { color: '#FFF' },
        };

        var chart = new google.charts.Bar(document.getElementById('workload'));

        chart.draw(data, google.charts.Bar.convertOptions(options));
      }
            google.charts.setOnLoadCallback(drawChart);
