
for ( var wbs in wbs_progress) {
    var total = parseInt(wbs_progress[wbs]["total_progress"])
    if (total == 0){
        total=100
    }
    var value = parseInt(wbs_progress[wbs]["completed_progress"]) / total
    var text = Math.round(value * 100) + '%'
    var data = [value, 1 - value]

    // Settings
    var width = 130
    var height = 100
    var anglesRange = 0.5 * Math.PI
    var radius = Math.min(width, 2 * height) / 2
    var thickness = 20
    // Utility
//     var colors = d3.scale.category10();
    var colors = ["#5EBBF8", "#F5F5F5"]

    var pies = d3.pie()
    	.value( d => d)
    	.sort(null)
    	.startAngle( anglesRange * -1)
    	.endAngle( anglesRange)

		var arc = d3.arc()
    	.outerRadius(radius)
    	.innerRadius(radius - thickness)

    var translation = (x, y) => `translate(${x}, ${y})`

    // Feel free to change or delete any of the code you see in this editor!
    var svg = d3.select("#wbs_progress"+wbs.toString()).append("svg")
      .attr("width", width)
      .attr("height", height)
      .attr("class", "half-donut")
      .append("g")
      .attr("transform", translation(width / 2, height))


    svg.selectAll("path")
    	.data(pies(data))
    	.enter()
    	.append("path")
    	.attr("fill", (d, i) => colors[i])
    	.attr("d", arc)

    svg.append("text")
    .text( d => text)
    .attr("dy", "-1rem")
    .attr("class", "label")
    .attr("text-anchor", "middle")

    svg.append("text")
    .text(wbs_progress[wbs]["name"])
    .attr("dy", "-5rem")
    .attr("class", "label")
    .attr("text-anchor", "middle")
    	}