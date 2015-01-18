// Margins
// Set the dimensions of the canvas / graph
var margin = {top: 20, right: 50, bottom: 30, left: 50},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

var parseDate = d3.time.format("%d-%b-%y").parse,
    bisectDate = d3.bisector(function(d) { return d.date; }).left,
    formatValue = d3.format(",.2f"),
    formatCurrency = function(d) { return "$" + formatValue(d); };

var color = d3.scale.category10();

var x = d3.time.scale()
    .range([0, width]);

var y = d3.scale.linear()
    .range([height, 0]);

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left");

var line = d3.svg.line()
    .x(function(d) { return x(d.label); })
    .y(function(d) { return y(d.value); });

var svg = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

d3.csv("test.csv", function(data) {
  data.forEach(function(d) {
    d.date = parseDate(d.date);
    d.close1 = +d.close1;
    d.close2 = +d.close2;
    d.close3 = +d.close3;
  });

  data.sort(function(a, b) {
    return a.date - b.date;
  });

  var labelVar = 'date'; //A
  var varNames = d3.keys(data[0])
      .filter(function (key) { return key !== labelVar;});
  color.domain(varNames); //C

  var seriesData = varNames.map(function (name) { //D
    return {
      name: name,
      values: data.map(function (d) {
        return {name: name, label: d[labelVar], value: +d[name]};
      })
    };
  });
  console.log("seriesData", seriesData);

  x.domain(d3.extent(data, function(d) { return d.date; }));
  y.domain([0,
    d3.max(seriesData, function (c) { 
      return d3.max(c.values, function (d) { return d.value; });
    })
  ]);

  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("Price ($)");

  var series = svg.selectAll(".series")
      .data(seriesData)
    .enter().append("g")
      .attr("class", "series");

  series.append("path")
      .attr("class", "line")
      .attr("d", function(d) { return line(d.values); })
      .style("stroke", function(d) { return color(d.name); })
      .style("stroke-width", "4px")
  	  .style("fill", "none");


  var focus = svg.append("g")
      .attr("class", "focus")
      .style("display", "none");

  focus.append("line")
        .attr("class", "x")
        .style("stroke", "blue")
        .style("stroke-dasharray", "3,3")
        .style("opacity", 0.5)
        .attr("y1", 0)
        .attr("y2", height);

  focus.append("circle")
      .attr("r", 4.5);

  focus.append("text")
      .attr("x", 9)
      .attr("dy", ".35em");

  svg.append("rect")
      .attr("class", "overlay")
      .attr("width", width)
      .attr("height", height)
      .on("mouseover", function() { focus.style("display", null); })
      .on("mouseout", function() { focus.style("display", "none"); })
      .on("mousemove", mousemove);

  function mousemove() {
  	// x0 are the dates 
    var x0 = x.invert(d3.mouse(this)[0]),
    	// Get the date index
        i = bisectDate(data, x0, 1),
        // Get data between dates
        d0 = data[i - 1],
        d1 = data[i],
        d = x0 - d0.date > d1.date - x0 ? d1 : d0;
    focus.attr("transform", "translate(" + x(d.date) + "," + y(d.close1) + ")");
    focus.select("text").text(formatCurrency(d.close1));
  }
});
