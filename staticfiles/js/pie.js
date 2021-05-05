google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {

        var data = google.visualization.arrayToDataTable([
          ['Task', 'Hours per Day'],
          ['No state', nostate],
          ['To-do',     todo],
          ['In Progress', inprogress],
          ['Completed',  completed],
        ]);

        var options = {
          'backgroundColor': 'transparent',
          legendTextStyle: { color: '#FFF' },
          legend: 'top',
          width: 300,
          height: 300,
        };

        var chart = new google.visualization.PieChart(document.getElementById('piechart'));

        chart.draw(data, options);
      }