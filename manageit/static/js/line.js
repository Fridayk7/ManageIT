google.charts.load('current', {'packages':['line']});
      google.charts.setOnLoadCallback(drawChart);

    function drawChart() {

      var data = new google.visualization.DataTable();
      data.addColumn('number', 'Day');
      data.addColumn('number', 'Tasks Remaining');
      data.addColumn('number', 'Tasks Completed');


      data.addRows([
        [1,  37.8, 80.8],
        [2,  30.9, 69.5],
        [3,  25.4,   57],
        [4,  11.7, 18.8],
        [5,  11.9, 17.6],
        [6,   8.8, 13.6],
        [7,   7.6, 12.3],
        [8,  12.3, 29.2],
        [9,  16.9, 42.9],
        [10, 12.8, 30.9],
        [11,  5.3,  7.9],
        [12,  6.6,  8.4],
        [13,  4.8,  6.3],
        [14,  4.2,  6.2]
      ]);

      var options = {
      animation: {
                duration: 1500,
                startup: true //This is the new option
            },
          title: 'Workload',
      chartArea: {
        backgroundColor: 'transparent'
      },
      backgroundColor: 'transparent'
      };

      var chart = new google.charts.Line(document.getElementById('line'));

      chart.draw(data, google.charts.Line.convertOptions(options));
    }