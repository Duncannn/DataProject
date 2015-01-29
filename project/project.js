// Json data
var optionsJSON;

// Global vars
var k = 0,
    GBM = false,
    investButton = false,
    activeStock = [0,0,0,0,0,0,0,0],
    thisAmount = [0,0,0,0,0,0,0,0],
    shareAmount = 0,                                     
    thisAmountOpt = [0,0,0,0,0,0,0,0],
    newPrice = [0,0,0,0,0,0,0,0],
    checked_boxes = [-1,-1,-1,-1,-1,-1,-1,-1],
    payoffData,
    GBMPrice,
    thisPrice = [],
    lastPrice = [],
    stockData = 0,
    numtour = 0,
    numAbout = 0,
    numInfo = 0,
    totalInvestment = 10000,
    strUser = "",
    remember,
    fullData,
    profit,
    allData = [{},{},{},{},{},{},{},{}],
    optionInfo = 0,
    eps = d3.random.normal();

// Margins   
var margin = {top: 20, right: 525, bottom: 400, left: 130},
    marginXBrush = {top: 330, right: 525, bottom: 320, left: 130},
    marginPayoff = {top: 450, right: 525, bottom: 55, left: 50},
    marginYBrush = {top: 20, right: 1185, bottom: 400, left: 30},
    marginBar = {top:380, right: 20, bottom: 120, left:950};

// Width and heights
var width = 1280 - margin.left - margin.right,
    widthPayoff = 1280 - marginPayoff.left - marginPayoff.right,
    widthYBrush = 1280 - marginYBrush.left - marginYBrush.right,
    widthBar = 1280 - marginBar.left - marginBar.right,

    height = 700 - margin.top - margin.bottom,
    heightXBrush = 700 - marginXBrush.top - marginXBrush.bottom,
    heightPayoff = 700 - marginPayoff.top - marginPayoff.bottom,
    heightYBrush = 700 - marginYBrush.top - marginYBrush.bottom,
    heightBar = (700 - marginBar.top - marginBar.bottom)/2;

// Date and money elements
var parseDate = d3.time.format("%d-%m-%Y").parse,
    bisectDate = d3.bisector(function(d) { return d.date; }).left,
    bisectNum = d3.bisector(function(d) {return d.price;}).left,
    formatValue = d3.format(",.2f"),
    formatCurrency = function(d) { return "$" + formatValue(d); };

// Colors
var color = d3.scale.category10();

// Scaling
var x = d3.time.scale().range([0, width]),
    x2 = d3.time.scale().range([0, width]),
    x3 = d3.scale.linear().range([0,widthPayoff]),
    x4 = d3.time.scale().range([0, widthYBrush]),
    xbar = d3.scale.linear().range([0, widthBar]),

    y = d3.scale.linear().range([height, 0]),
    y2 = d3.scale.linear().range([heightXBrush, 0]),
    y3 = d3.scale.linear().range([heightPayoff, 0]),
    y4 = d3.scale.linear().range([heightYBrush, 0]),
    ybar1 = d3.scale.ordinal().rangeRoundBands([0, heightBar], .2),
    ybar2 = d3.scale.ordinal().rangeRoundBands([0, heightBar], .2);

// Axes
var xAxis = d3.svg.axis().scale(x).orient("bottom"),
    xAxis2 = d3.svg.axis().scale(x2).orient("bottom"),
    xAxis3 = d3.svg.axis().scale(x3).orient("bottom"),
    xAxis4 = d3.svg.axis().scale(x4).orient("bottom"),
    xAxisbar = d3.svg.axis().scale(xbar).orient("bottom").ticks(8),

    yAxis = d3.svg.axis().scale(y).orient("left"),
    yAxis3 = d3.svg.axis().scale(y3).orient("left"),
    yAxis4 = d3.svg.axis().scale(y4).orient("left"),
    yAxisbar1 = d3.svg.axis().scale(ybar1).orient("left"),
    yAxisbar2 = d3.svg.axis().scale(ybar2).orient("left");

// Horizontal and vertical brushes
var brushx = d3.svg.brush()
    .x(x2)
    .on("brush", brushedx);

var brushy = d3.svg.brush()
    .y(y4)
    .on("brush", brushedy);

// 4 Lines I'm using
var line1 = d3.svg.line()
    .interpolate("basis")
    .x(function(d) { return x(d.date); })
    .y(function(d) { return y(d.price); });

var line2 = d3.svg.line()
    .interpolate("basis")
    .x(function(d) { return x2(d.date); })
    .y(function(d) { return y2(d.price); });

var line3 = d3.svg.line()
    .interpolate("basis")
    .x(function(d) { return x3(d.key); })
    .y(function(d) { return y3(d.price); });

var line4 = d3.svg.line()
    .interpolate("basis")
    .x(function(d) { return x4(d.date); })
    .y(function(d) { return y4(d.price); });

// Appending the SVG element
var svg = d3.select("body").append("svg")
    .attr("id","svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom);

// Clip path for when using the brush
svg.append("defs").append("clipPath")
    .attr("id", "clip")
    .append("rect")
    .attr("width", width)
    .attr("height", height);

// Main element where the stock charts are in
var main = svg.append("g")
    .attr("class", "main")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// Two brush elements
var xBrush = svg.append("g")
    .attr("class", "xBrush")
    .attr("transform", "translate(" + marginXBrush.left + "," 
                                    + marginXBrush.top + ")");

var yBrush = svg.append("g")
    .attr("class", "yBrush")
    .attr("transform", "translate(" + marginYBrush.left + "," + 
                                      marginYBrush.top + ")");

// Payoff element
var payoff = svg.append("g")
    .attr("class", "payoff")
    .attr("transform", "translate(" + marginPayoff.left + "," + 
                                      marginPayoff.top + ")");

// Tooltip main graph
var toolTip1 = svg.append("g")
    .attr("transform", "translate(" + margin.left + "," + 
                                      margin.top + ")")
    .style("display", "none");

// Tooltip payoff graph
var toolTip2 = svg.append("g")
    .attr("transform","translate(" + marginPayoff.left + "," + 
                                     marginPayoff.top + ")");

// Bar charts
var chart1 = svg.append("g")
    .attr("class", "chart1")
    .attr("transform", "translate(" + marginBar.left +"," +marginBar.top +")");

var bar2 = marginBar.top +heightBar+40;

var chart2 = svg.append("g")
    .attr("class", "chart2")
    .attr("transform", "translate(" + marginBar.left +"," +bar2 +")");

// Set the initial money
document.getElementById("money").innerHTML = "Money left: $" + 
                                              formatValue(totalInvestment);

// Load option data
d3.json("optionsData.json", function(data) {optionsJSON = data;})

// Main data
d3.json("finalData.json", function(error, data) {
  // save full data and crop data to 2nd jan.
  fullData = data;
  data = data.slice(14,data.length-1);

  // Color domain are all names in the data except the date
  color.domain(d3.keys(data[0]).filter(function(key) {return key !== "date";}));

  // Parse the date
  data.forEach(function(d) {
    d.date = parseDate(d.date);
  });

  // Sort the date
  data.sort(function(a, b) {
    return a.date - b.date;
  });

  // Assign the stocks a color and map the values 
  stockData = color.domain().map(function(name) {
    return {
      name: name,
      values: data.map(function(d) {
        return {date: d.date, price: +d[name]};
      })
    };
  });

  // Last known price for all stocks in one array
  for (var i = 0; i < stockData.length; i++) {
    thisPrice.push(stockData[i].values[(stockData[i].values).length-1].price);
    lastPrice.push(fullData[0][stockData[i].name]);
  }
// ------------------------------------------------------------------
// Domains
// ------------------------------------------------------------------
  // x,x2,x4 and y,y2,y4 domains
  x.domain(d3.extent(data, function(d) { return d.date; }));

  y.domain([0, d3.max(stockData, function(c) 
       {return d3.max(c.values, function(v) {return v.price; }); 
    })
  ]);

  x2.domain(x.domain());
  y2.domain(y.domain());
  x4.domain(x.domain());
  y4.domain(y.domain());

// ------------------------------------------------------------------
// Main graph
// ------------------------------------------------------------------
  // Place the x axis
  main.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

  // Place the y axis
  main.append("g")
      .attr("class", "y axis")
      .call(yAxis)
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("price ($)");

  // Place all the stocks
  var stock1 = main.selectAll(".stock1")
      .data(stockData)
    .enter().append("g")
      .attr("class", "stock1");

  stock1.append("path")
      .attr("id", function(d,i) {;return d.name})
      .attr("d", function(d) { return line1(d.values); })
      .style("stroke", function(d) { return color(d.name); })
      .style("fill", "none")
      .style("stroke-width", "1.5px");

// ------------------------------------------------------------------
// Legend
// ------------------------------------------------------------------

  // Spacing between legend
  var space = height/stockData.length;

  // Add the main legend class
  var legend = svg.append("g")
    .attr("class", "legend");
      
  // Add all the names with appropriate spacing  
  legend.selectAll('text')
    .data(stockData)
  .enter().append("text")
    .attr("id", function(d,i) {return d.name})
    .attr("x", width+ margin.left +10)
    .attr("y", function(d, i){ return (i+0.5) * space + margin.top;})
    .style("fill", function(d) {return color(d.name)})
    .text(function(d) { return d.name;})
    .on("click", function(d, i){
      // Set variable to active or inactive and denote the current stock index
      var active  = d.active ? false : true;
      d.active = active;
      k = i;

      // Contiuing the tour
      if (active == true) {
        activeStock[k] = 1;
      } else {activeStock[k] = 0}
      if (numtour == 3) {
        tour2();
      }

      // Call functions that depent on activation of stock
      payoffResult();
      payoffLegendName();
      optionbars();
      editSlider();
      unCheckBoxes();
      sliderText();

      document.getElementById("shareHeader").style.visibility = "visible";
      if (checked_boxes[k] !== -1) {checkBoxes();}
      // uncheck all boxes
      document.getElementById("strats").style.visibility = "visible";
      // Edit the information on thfe page
      document.getElementById("money").innerHTML = 
      "Money left: $" + formatValue(totalInvestment);
      document.getElementById("stock").innerHTML = 
      "Investing in " +stockData[k].name;
      document.getElementById("stockPrice").innerHTML = 
      "Current price  " +thisPrice[k];
      if (strUser == "shares") {
        document.getElementById("amount").value = thisAmount[k];
      }

      // When  active
      if (active == true) {
        d3.select("#navbar")
          .transition().duration(1000)
          .style("background-color",color(d.name));
        // Values for the line, and change the line
        var onOpacity = 5,
            offOpacity = 2;
        legend.select("#"+d.name)
              .transition().duration(1000)
              .style("font-size","15px")
              .style("font-weight","bold");
        d3.select("#"+d.name.replace(/\s+/g, ''))
            .transition().duration(1000) 
            .style("stroke-width", onOpacity)
            .style("opacity", 1);

        // Put all stocks except this one to false
        for (var j = 0; j < stockData.length; j++) {
          if (j != i) {
            d3.select("#"+stockData[j].name)
              .transition().duration(1000) 
              .style("stroke-width", offOpacity)
              .style("opacity", 0.5);

            legend.select("#"+stockData[j].name)
              .transition().duration(1000)
              .style("font-size","10px")
              .style("font-weight","normal");
              stockData[j].active = false;
              activeStock[j] = 0;
          };
        };

      // Change all the lines and to normal if none are active
      } else {

        d3.select("#navbar")
          .transition().duration(1000)
          .style("background-color","maroon");

        for (var j = 0; j < stockData.length; j++) {
          d3.select("#"+stockData[j].name)
            .transition().duration(1000) 
            .style("stroke-width", 2)
            .style("opacity", 1);

          legend.select("#"+stockData[j].name)
                .transition().duration(1000)
                .style("font-size","10px")
                .style("font-weight","normal");
        }
      }
    });
// ------------------------------------------------------------------
// Brush X Section
// ------------------------------------------------------------------
  
  // Place the x axis for the horizontal brush
  xBrush.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + heightXBrush + ")")
      .call(xAxis2);  

  // Place all the stocks
  var stock2 = xBrush.selectAll(".stock2")
      .data(stockData)
    .enter().append("g")
      .attr("class", "stock2");

  stock2.append("path")
      .attr("class", "line")
      .attr("d", function(d) { return line2(d.values); })
      .style("stroke", function(d) { return color(d.name); });

  // Call the brush element in a rectangle
  xBrush.append("g")
      .attr("class", "x brush")
      .call(brushx)
    .selectAll("rect")
      .attr("y", -6)
      .attr("height", heightXBrush + 7);  

// ------------------------------------------------------------------
// Brush Y Section
// ------------------------------------------------------------------
  
  // Place the y axis for the vertical brush
  yBrush.append("g")
      .attr("class", "y axis")
      .call(yAxis4)
    .append("text")
      .attr("transform", "rotate(-90)");

  // Place all the stocks
  var stock3 = yBrush.selectAll(".stock3")
      .data(stockData)
    .enter().append("g")
      .attr("class", "stock3");

  stock3.append("path")
      .attr("class", "line")
      .attr("d", function(d) {return line4(d.values); })
      .style("stroke", function(d) { return color(d.name); });

  // Call the brush element in a rectangle
  yBrush.append("g")
      .attr("class", "y brush")
      .call(brushy)
    .selectAll("rect")
      .attr("x", 0)
      .attr("width", widthYBrush);

// ------------------------------------------------------------------
// Tooltip Main Graph
// ------------------------------------------------------------------

  // Add a circle for the tooltip
  toolTip1.append("circle")                                 
      .attr("class", "y")                                
      .style("fill", "none")                             
      .style("stroke", "black")                           
      .attr("r", 4);

  // Add the text for the tooltip
  toolTip1.append("text")
      .attr("class", "y2")
      .attr("dx", -2)
      .attr("dy", -10)
      .style("font-size", "15px");

  // Rectangle for when the tooltip shows if the mouse is on it
  main.append("rect")                                     
      .attr("width", width)                              
      .attr("height", height+margin.bottom/3)                            
      .style("fill", "none")                             
      .style("pointer-events", "all")                    
      .on("mouseover", function() { toolTip1.style("display", null); })
      .on("mouseout", function() { toolTip1.style("display", "none"); })
      .on("mousemove", mousemove); 

  // Function for when the mouse moves on the rectangle
  function mousemove() {
    // Get the date, its index, values left/right of date and the intrapolation
    var mouseDate = x.invert(d3.mouse(this)[0]),              
        i = bisectDate(stockData[k].values, mouseDate, 1),                   
        d0 = stockData[k].values[i - 1],                              
        d1 = stockData[k].values[i],                            
        d = mouseDate - d0.date > d1.date - mouseDate ? d1 : d0;
    
    // Move the circle on the graph where the mouse is
    toolTip1.select("circle.y")                           
        .attr("transform",                             
              "translate(" + x(d.date) + "," +         
                             y(d.price) + ")");

    // Place the price above of the circle
    toolTip1.select("text.y2")
        .attr("transform",
              "translate(" + x(d.date) + "," +
                             y(d.price) + ")")
        .text(formatCurrency(d.price));   
    }

// ------------------------------------------------------------------
// Tooltip Payoff Graph
// ------------------------------------------------------------------

  // Add circle to the tooltip
  toolTip2.append("circle")                                 
      .attr("class", "y")                                
      .style("fill", "none")                             
      .style("stroke", "black")                         
      .attr("r", 4);

  // Add the text for the tooltip (profit)
  toolTip2.append("text")
      .attr("class", "y2")
      .attr("dx", -2)
      .attr("dy", -30)
      .style("font-size", "15px");

  // Add second text to tooltip (price)
  toolTip2.append("text")
      .attr("class", "y3")
      .attr("dx", -2)
      .attr("dy", -10)
      .style("font-size", "15px");

  // Rectangle for when the tooltip shows if the mouse is on it
  payoff.append("rect")                                     
      .attr("width", widthPayoff)                              
      .attr("height", heightPayoff)                            
      .style("fill", "none")                             
      .style("pointer-events", "all")                    
      .on("mouseover", function() { toolTip2.style("display", null); })
      .on("mouseout", function() { toolTip2.style("display", "none"); })
      .on("mousemove", mousemovepayoff); 

  // Function for when the mouse moves on the rectangle
  function mousemovepayoff() {
    // Get the number and the index of that number
    var mouseNum = x3.invert(d3.mouse(this)[0]),
        i2 = Math.round(mouseNum+30-thisPrice[k]);

    // Only show tooltip if there is a line
    if (payoffData[k].length !== 0) {

      // Only one line, so profit doesn't get calculated
      if (payoffData[k].length === 1) {
        var d = payoffData[k][payoffData[k].length-1][i2];}
      // More lines, there is a profit variable
      else { var d = profit[i2]}

      // move the circle
      toolTip2.select("circle.y")                           
          .attr("transform",                             
                "translate(" + x3(d.key) + "," +         
                               y3(d.price) + ")");

      // Place the profit and price above of the circle
      toolTip2.select("text.y2")
          .attr("transform",
                "translate(" + x3(d.key) + "," +
                               y3(d.price) + ")")
          .text("Profit: "+formatCurrency(d.price)); 

      toolTip2.select("text.y3")
          .attr("transform",
                "translate(" + x3(d.key) + "," +
                               y3(d.price) + ")")
          .text("Price: "+formatCurrency(Math.round(d.key)));
    // No tooltip if there is no investment in the stock
    } else {toolTip2.style("display", "none");}
  }

// ------------------------------------------------------------------
// Payoff graph
// ------------------------------------------------------------------ 

  // Initial empty graph
  x3.domain([0,0]);
  y3.domain([0,0]);
  payoffData = [[],[],[],[],[],[],[],[]];

  // Place the x axis
  payoff.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + heightPayoff/2 + ")")
      .call(xAxis3)
      .append("text")
      .attr("y", 35)
      .attr("x", widthPayoff-30)
      .text("price ($)");

  // place the y axis
  payoff.append("g")
      .attr("class", "y axis")
      .call(yAxis3)
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("profit ($)");

  // Graph after update
  window.payoffResult = function() {
    // Initialise variables and remove all the old graphs
    payoffData[k] = [];
    payoff.selectAll(".stock3").remove();

    // Count how many options there are and remove ones with no numbers 
    var optionAmount = 0
    for (var m = 0; m < Object.keys(allData[k]).length; m++){
      optionAmount += Math.abs(allData[k][Object.keys(allData[k])[m]][0]);
      if (allData[k][Object.keys(allData[k])[m]][0] === "0") {
        delete allData[k][Object.keys(allData[k])[m]];
      }
    }

    // Create lines if there are line elements
    if (optionAmount !== 0) {

      // Loop over the dictionary
      for (var i = 0; i < Object.keys(allData[k]).length; i++ ){
        var lineInfo =[];

        // Loop over the range of possible prices
        for (var j = thisPrice[k]-30; j <= thisPrice[k] +30; j++){

          // if it does contain c then its a call
          if (Object.keys(allData[k])[i].indexOf("c") !== -1 ){
            // replace the c
            var thisStrike = Object.keys(allData[k])[i].replace("c","");
            lineInfo.push({
              key: j,
              price: allData[k][Object.keys(allData[k])[i]][0]
                      *(100 * d3.max([j - thisStrike,0]) 
                      - allData[k][Object.keys(allData[k])[i]][1])
            });

          // if it does contain p then its a put
          } else if (Object.keys(allData[k])[i].indexOf("p") !== -1) {
            var thisStrike = Object.keys(allData[k])[i].replace("p","");
            lineInfo.push({
              key: j,
              price: allData[k][Object.keys(allData[k])[i]][0]
                      *(100 * d3.max([thisStrike - j,0]) 
                      - allData[k][Object.keys(allData[k])[i]][1])
            });

          // otherwise they are shares
          } else {
            lineInfo.push({
              key: j,
              price: (j-thisPrice[k])* allData[k][Object.keys(allData[k])[i]][0]
            });             
          }
        }
        payoffData[k].push(lineInfo);
      }

      // Create the profit line by adding all the elements
      profit = [];
      for (var j = 0; j < 61; j++) {
        var profitKey = 0;
        for (var i = 0; i < payoffData[k].length; i++) {
          profitKey += payoffData[k][i][j].price;
        }
        profit.push({
          key: payoffData[k][0][j].key,
          price: profitKey
        });
      }

      // Add the profit line to the payoff data
      if (payoffData[k].length >=2) {payoffData[k].push(profit)}

      // Find the highest and lowest values
      var yMax = 0,
          yMin = 0,
          dom = [];

      // Loop over all elements and find the maximum and minimum values
      for (var i = 0; i<payoffData[k].length; i++) {
        for (var j = 0; j < payoffData[k][i].length; j++) {
          if (payoffData[k][i][j].price < yMin) 
            {yMin = payoffData[k][i][j].price;}
          else if (payoffData[k][i][j].price > yMax) 
            {yMax=payoffData[k][i][j].price;}
        } 
      };

      // This is your y-domain
      var dom = [yMin, yMax];

      // Set the domains
      x3.domain(d3.extent(payoffData[k][0], function(d) { return d.key; }));
      y3.domain(dom);

      // Set the intersection point to 1/2 of the graph if there are no lines
      if (payoffData[k].length == 0){
        var intersection = 0.5;
      } else{
        var intersection =  Math.abs(dom[1])/(Math.abs(dom[1])+Math.abs(dom[0]));
      } 

      // Plot a max of 5 graphs
      if (payoffData[k].length > 5) {
        var len = payoffData[k].length,
            dataPlot = payoffData[k].slice(len-4, len);
      } else {
        var dataPlot = payoffData[k];
      }

      // Plot all the lines
      var stock3 = payoff.selectAll(".stock3")
          .data(dataPlot)
        .enter().append("g")
          .attr("class", "stock3");

      stock3.append("path")
          .attr("id", function(d,i) {return stockData[k].name;})
          .attr("d", function(d) { return line3(d); })
          .style("stroke", function(d,i) {
              if (i == dataPlot.length-1) {
                  return color(stockData[k].name);
              } else {return "maroon";}    
          })
          .style("stroke-width", function(d,i) {
              if (i == dataPlot.length-1) {
                  return 3;
              } else {return 1;}
          })
          .style("opacity", 0)
          .transition().duration(1500)
          .style("opacity", 1)
          .style("fill", "none")
          .style("stroke-dasharray", function(d,i){
              if (i == dataPlot.length-1) {
                  return 0,0;}
              else {return 5,5;}
          })
    
    // Transition the x and y axis
      payoff.select(".x.axis").transition().duration(1000)
            .call(xAxis3)
            .attr("transform", "translate(0," + heightPayoff*intersection+ ")");
      payoff.select(".y.axis").transition().duration(1000).call(yAxis3);

    // Reset the domains if there are no lines
    } else {
      x3.domain([thisPrice[k]-30,thisPrice[k]+30]);
      y3.domain([0,0]);
      payoff.select(".x.axis").transition().duration(1000)
            .call(xAxis3)
            .attr("transform", "translate(0," + heightPayoff*0.5+ ")");
      payoff.select(".y.axis").transition().duration(1000).call(yAxis3);
    }

    // Section for the results following results() or GBM()
    // Remove the old lines and text
    payoff.select("#resultsLine").remove();
    payoff.select("#resultsText").remove();

    // Only after results is clicked
    if (investButton === true) {
      // Find out if it was the simulated price or market price
      if (GBM === true) {
        var linePrice = GBMPrice;
      } else {
        var linePrice = lastPrice;
      }

      // Append the lines and text to the payoff section
      payoff.append("line")
            .attr("id", "resultsLine")
            .attr("x1", x3(linePrice[k]))
            .attr("y1", 0)
            .attr("x2", x3(linePrice[k]))
            .attr("y2", heightPayoff)
            .attr("stroke-width", 2)
            .attr("stroke", "maroon")
            .attr("opacity" , 0)
            .transition().duration(1000)
            .attr("opacity" , 1);

      // Add the date on top
      payoff.append("text")
            .attr("id", "resultsText")
            .attr("y", -10)
            .attr("x", x3(linePrice[k])-35)
            .attr("font-weight", "bold")
            .text("Price at 23rd Jan");
    }
  }

// ------------------------------------------------------------------
// Payoff Legend
// ------------------------------------------------------------------
  
  // Main element
  var payoffLegend = svg.append("g")
    .attr("class", "payoffLegend");
    
  // Name and color stock
  payoffLegend.append("text")
      .attr("x", widthPayoff +marginPayoff.left +10)
      .attr("y", 450)
      .style("fill", color(stockData[k].name))
      .text(stockData[k].name);

  // Amount of stocks
  payoffLegend.append("text")
      .attr("x", widthPayoff +marginPayoff.left +10)
      .attr("y", 470)
      .text(thisAmount[k] +" stocks");

  // Amount of options
  payoffLegend.append("text")
      .attr("x", widthPayoff +marginPayoff.left +10)
      .attr("y", 490)
      .text(thisAmount[k] +" options");

  // Dynamically change the color and amounts
  window.payoffLegendName = function() {
    payoffLegend.select("text:nth-child(1)")
                .style("fill", color(stockData[k].name))
                .text(stockData[k].name);

    // Shares is 0 if he is not in the dictionary
    if (allData[k]["shares"] === undefined) {
      shareAmount = 0;
    // Or the first element in the dict 
    } else{
      shareAmount = allData[k]["shares"][0];
    }
    // Set the amount of stocks
    payoffLegend.select("text:nth-child(2)")
                .text(shareAmount +" stocks");

    // Count the amount of options
    var num = 0;
    for (var i = 0;i < Object.keys(allData[k]).length; i++){
      if (Object.keys(allData[k])[i] != "shares"){
        num += Math.abs(allData[k][Object.keys(allData[k])[i]][0]);
      }
    }
    // Add the amount to hte html page
    num = parseInt(num);
    if (num == 1) {
      payoffLegend.select("text:nth-child(3)")
                  .text(num +" option");
    } else {
      payoffLegend.select("text:nth-child(3)")
                  .text(num +" options");
    }
  }

// ------------------------------------------------------------------
// Bar Chart
// ------------------------------------------------------------------ 

  window.optionbars = function(){
    // Every stock has a different amount of put/call options, so
    // we have to recalculate both the domains again.
    document.getElementById("optCounterPut").style.visibility = "hidden";
    document.getElementById("optCounterCall").style.visibility = "hidden";

    // Initialise variables
    var strikesCall = [],
        pricesCall = [],
        strikesPut = [],
        pricesPut = [];
    // Append all the prices and strikes for the calls and the puts
    for (var i = 0; i<optionsJSON[stockData[k].name].call.length; i++){
      strikesCall.push(optionsJSON[stockData[k].name].call[i].strike);
      pricesCall.push(optionsJSON[stockData[k].name].call[i].price*100);
    }
    for (var i = 0; i<optionsJSON[stockData[k].name].put.length; i++){
      strikesPut.push(optionsJSON[stockData[k].name].put[i].strike);
      pricesPut.push(optionsJSON[stockData[k].name].put[i].price*100);
    }
    // Join the put and call prices in one array
    var prices = pricesCall.concat(pricesPut),
        strikes = strikesCall.concat(strikesPut);

    // Find the domains of this data
    xbar.domain([0, d3.max(prices)]);
    ybar1.domain(strikesCall);
    ybar2.domain(strikesPut);

    // Remove old bars and axes
    chart1.selectAll(".bar").remove();
    chart2.selectAll(".bar2").remove();
    chart1.select(".y.axis").remove();
    chart2.select(".y.axis").remove();
    chart1.select(".x.axis").remove();
    chart2.select(".x.axis").remove();
    chart1.select("text").remove();
    chart2.select("text").remove();

    // Create the call bar charts
    chart1.selectAll(".bar")
        .data(optionsJSON[stockData[k].name].call)
      .enter().append("rect")
        .attr("class", "bar")
        .attr("y", function(d) {return ybar1(d.strike); })
        .attr("height", ybar1.rangeBand())
        .attr("x", 1)
        .attr("width", function(d) {return xbar(d.price*100); })
        .on("click", function(d,i) {
          // Edit the visibility of the inputs and the text beside them
          document.getElementById("optCounterPut").style.visibility = "hidden";
          document.getElementById("optCounterCall").style.visibility = "visible";
          document.getElementById("optTypeCall").innerHTML = 
          "Buy or sell call option with strike $" +d.strike +" for a price of $" 
          +formatValue(d.price*100);

          // Amount of options is zero if the option is not in the dict
          if (allData[k][d.strike+"c"] === undefined) {
              document.getElementById("numCall").value = 0;
          // Amount of options = the first element of the array in the dict
           } else {
            document.getElementById("numCall").value=allData[k][d.strike+"c"][0];
           }
           // Set this option info to the variable 
          optionInfo = d;
        })
        .style("opacity", 0)
        .transition().duration(1000)
        .style("opacity", 1);

    // Create the put bar charts
    chart2.selectAll(".bar2")
        .data(optionsJSON[stockData[k].name].put)
      .enter().append("rect")
        .attr("class", "bar2")
        .attr("y", function(d) {return ybar2(d.strike); })
        .attr("height", ybar2.rangeBand())
        .attr("x", 1)
        .attr("width", function(d) {return xbar(d.price*100); })
        .on("click", function(d,i) {

          // Edit the visibility of the inputs and the text beside them
          document.getElementById("optCounterCall").style.visibility = "hidden";
          document.getElementById("optCounterPut").style.visibility = "visible";
          document.getElementById("optTypePut").innerHTML = 
          "Buy or sell put option with strike $" +d.strike +" for a price of $" 
          +formatValue(d.price*100);

          // Amount of options is zero if the option is not in the dict (undef)
          if (allData[k][d.strike+"p"] === undefined) {
            document.getElementById("numPut").value = 0;
          // Amount of options: the first element of the array in the dict
          } else {
            document.getElementById("numPut").value = allData[k][d.strike+"p"][0];
          }

          // Set this option info to the variable
          optionInfo = d;
        })
        .style("opacity", 0)
        .transition().duration(1000)
        .style("opacity", 1);

      // y axis call options
    chart1.append("g")
          .attr("class", "y axis")
          .call(yAxisbar1)
          .style("opacity", 0)
          .transition().duration(1000)
          .style("opacity", 1);

    // Text above bar chart
    chart1.append("text")
        .attr("x", -30)
        .attr("y", -15)
        .attr("dy", ".71em")
        .text("Strike price of Call options")
        .style("opacity", 0)
        .transition().duration(1000)
        .style("opacity", 1);

    // y axis put options
    chart2.append("g")
          .attr("class", "y axis")
          .call(yAxisbar2)
          .style("opacity", 0)
          .transition().duration(1000)
          .style("opacity", 1);

    // Text above bar charts
    chart2.append("text")
          .attr("x", -30)
          .attr("y", -15)
          .attr("dy", ".71em")
          .text("Strike price of Put options")
          .style("opacity", 0)
          .transition().duration(1000)
          .style("opacity", 1);

    // x axis call options
    chart1.append("g")
          .attr("class", "x axis")
          .attr("transform", "translate(0," + heightBar + ")")
          .call(xAxisbar)
          .style("opacity", 0)
          .transition().duration(1000)
          .style("opacity", 1);

    // x axis put options
    chart2.append("g")
          .attr("class", "x axis")
          .attr("transform", "translate(0," + heightBar + ")")
          .call(xAxisbar)
          .style("opacity", 0)
          .transition().duration(1000)
          .style("opacity", 1);
  }

// ------------------------------------------------------------------
// END OF D3.JSON(){}
// ------------------------------------------------------------------
});
  // Remove old slider and append a new slider with the 
  // amount of shares are invested
  function editSlider(){
    d3.select("#slider").remove();
    d3.select("body").append("input")
    .attr("id", "slider")
    .attr("type", "range")
    .attr("min", -5)
    .attr("max", 5)
    .attr("value", function() {
      if (allData[k]["shares"] !== undefined) {
        return allData[k]["shares"][0]/5;
      } else {return 0;}
    }) 
    .style("visibility", "visible")
    .on("change", function() {
      // Set the share data and call the functions
      allData[k]["shares"] = [this.value*5, ""];
      investButton = false;
      payoffLegendName();
      payoffResult();
      moneyLeft();
      // Set the amount of shares beside the slider
      if (allData[k]["shares"] !== undefined) {
        document.getElementById("shareSlider").innerHTML=this.value*5 +" shares";
      }
    });
  }

// ------------------------------------------------------------------
// Brush function
// ------------------------------------------------------------------

  // Horizontal brush
  function brushedx() {
    // Set the main x domain to the brushed domain
    x.domain(brushx.empty() ? x2.domain() : brushx.extent());

    // Transition back to normal if the brush is empty
    if (brushx.empty()) {
      main.select(".x.axis")
          .transition().duration(1000)
          .call(xAxis);
      for (var i = 0; i<stockData.length; i++) {
        main.select("#"+stockData[i].name)
            .transition().duration(1000)
            .attr("d", function(d){return line1(d.values);});
      }
    //Edit the main graph to the extent of the brush
    } else {
        main.select(".x.axis").call(xAxis);
        for (var i = 0; i<stockData.length; i++) {
          main.select("#"+stockData[i].name)
              .attr("d", function(d){return line1(d.values);});
        }
    }
  }

  // Vertical brush
  function brushedy() {
    // Set the main y domain to the brushed domain
    y.domain(brushy.empty() ? y4.domain() : brushy.extent());
    // Transition back to normal if the brush is empty
    if (brushy.empty()) {
      main.select(".y.axis")
          .transition().duration(1000)
          .call(yAxis);
      for (var i = 0; i<stockData.length; i++) {
        main.select("#"+stockData[i].name)
            .transition().duration(1000)
            .attr("d", function(d){return line1(d.values);});
      };
    // Edit the main graph to the extent of the brush
    } else {
      main.select(".y.axis").call(yAxis);
      for (var i = 0; i<stockData.length; i++) {
        main.select("#"+stockData[i].name).attr("d", function(d){
                                                  return line1(d.values);});
      }
    }
  }

// ------------------------------------------------------------------
// Strategies
// ------------------------------------------------------------------
    
    function bullSpread() {
      // clear all previous inputs and set variables
      clearInput();
      investButton = false;
      checked_boxes[k] = 0;
      allData[k] = {};

      // Get the index for the ATM option
      var index = getIndexCall();

      // Set the prices and strikes for the options in the spread
      var lengthCall = optionsJSON[stockData[k].name].call.length,
          longStrike = optionsJSON[stockData[k].name].call[index].strike,
          longPrice = optionsJSON[stockData[k].name].call[index].price,
          shortStrike = optionsJSON[stockData[k].name].call[lengthCall-1].strike,
          shortPrice = optionsJSON[stockData[k].name].call[lengthCall-1].price;

      // Add the options to the data variable
      allData[k][longStrike+"c"] = [1, longPrice*100];
      allData[k][shortStrike+"c"] = [-1, shortPrice*100];

      // Edit the slider, payoff legend, results, money and slider text
      callFunctions()
    }

//------------------------------------------------------------------------------

    function bearSpread() {
      // clear all previous inputs and set variables
      clearInput();
      investButton = false;
      checked_boxes[k] = 1;
      allData[k] = {};
      
      // Get the index for the ATM option
      var index = getIndexCall();

      // Set the prices and strikes for the options in the spread
      var shortStrike = optionsJSON[stockData[k].name].call[0].strike,
          shortPrice = optionsJSON[stockData[k].name].call[0].price,
          longStrike = optionsJSON[stockData[k].name].call[index].strike,
          longPrice = optionsJSON[stockData[k].name].call[index].price;

      // Add the options to the data variable
      allData[k][shortStrike+"c"] = [-1, shortPrice*100];
      allData[k][longStrike+"c"] = [1, longPrice*100];

      // Edit the slider, payoff legend, results, money and slider text
      callFunctions()
    }
//------------------------------------------------------------------------------
    function backSpread() {
      // clear all previous inputs and set variables
      clearInput();
      investButton = false;
      checked_boxes[k] = 2;
      allData[k] = {};

      // Get the index for the ATM option
      var index = getIndexCall();
      // Amazon different
      if (k == 0) {index += 1;}

      // Set the prices and strikes for the options in the spread
      var shortStrike = optionsJSON[stockData[k].name].call[index-1].strike,
          shortPrice = optionsJSON[stockData[k].name].call[index-1].price,
          longPrice1 = optionsJSON[stockData[k].name].call[index+1].price,
          longStrike1 = optionsJSON[stockData[k].name].call[index+1].strike;

      // Add the options to the data variable
      allData[k][shortStrike+"c"] = [-1, shortPrice*100];
      allData[k][longStrike1+"c"] = [2, longPrice1*100];

      // Edit the slider, payoff legend, results, money and slider text
      callFunctions()
    }
//------------------------------------------------------------------------------
    function strangleSpread() {
      // clear all previous inputs and set variables
      clearInput();
      investButton = false;
      checked_boxes[k] = 4;
      allData[k] = {};

      // Get the index for the ATM call and put option
      var indexCall = getIndexCall();
      var indexPut = getIndexPut();

      // Set the prices and strikes for the options in the spread
      var longStrikeCall = optionsJSON[stockData[k].name].call[indexCall].strike,
          longPriceCall = optionsJSON[stockData[k].name].call[indexCall].price,
          longStrikePut = optionsJSON[stockData[k].name].put[indexPut].strike,
          longPricePut = optionsJSON[stockData[k].name].put[indexPut].price;

      // Add the options to the data variable
      allData[k][longStrikeCall+"c"] = [1, longPriceCall*100];
      allData[k][longStrikePut+"p"] = [1, longPricePut*100];

      // Edit the slider, payoff legend, results, money and slider text
      callFunctions()
    }
//------------------------------------------------------------------------------
    function ironSpread() {
      // clear all previous inputs and set variables
      clearInput();
      investButton = false;
      checked_boxes[k] = 3;
      allData[k] = {};

       // Get the index for the ATM call and put option
      var callIndex = getIndexCall(),
          putIndex = getIndexPut();

      // Costco different
      if (k == 3) {
        callIndex -=1;
        putIndex -=1;
      }

      // Set the prices and strikes for the options in the spread
      var callPrice1 = optionsJSON[stockData[k].name].call[callIndex].price,
          callStrike1 = optionsJSON[stockData[k].name].call[callIndex].strike,
          callPrice2 = optionsJSON[stockData[k].name].call[callIndex+2].price,
          callStrike2 = optionsJSON[stockData[k].name].call[callIndex+2].strike;

      var putPrice1 = optionsJSON[stockData[k].name].put[putIndex].price,
          putStrike1 = optionsJSON[stockData[k].name].put[putIndex].strike,
          putPrice2 = optionsJSON[stockData[k].name].put[putIndex-2].price,
          putStrike2 = optionsJSON[stockData[k].name].put[putIndex-2].strike;

      // Add the options to the data variable
      allData[k][callStrike1+"c"] = [-1, callPrice1*100];
      allData[k][callStrike2+"c"] = [1, callPrice2*100];
      allData[k][putStrike1+"p"] = [-1, putPrice1*100];
      allData[k][putStrike2+"p"] = [1, putPrice2*100];

      // Edit the slider, payoff legend, results, money and slider text
      callFunctions()
    }

    function getIndexCall() {
      // Find the smallest difference between stock and strike prices
      var difference = 10000;
      for (var i = 0; i < optionsJSON[stockData[k].name].call.length; i++){
        var thisDifference = Math.abs(thisPrice[k] - 
                                optionsJSON[stockData[k].name].call[i].strike);
        // If difference is smaller, this is the new index
        if (thisDifference < difference) {
          difference = thisDifference;
          var index = i;
        }
      }
      // return the index
      return index;
    }

    function getIndexPut() {
      // Find the smallest difference between stock and strike prices
      var difference = 10000;
      for (var i = 0; i < optionsJSON[stockData[k].name].put.length; i++){
        var thisDifference = Math.abs(thisPrice[k] - 
                                  optionsJSON[stockData[k].name].put[i].strike);
        // If difference is smaller, this is the new index
        if (thisDifference < difference) {
          difference = thisDifference;
          var index = i;
        }
      }
      // return the index
      return index;
    }

// ------------------------------------------------------------------
// Money left
// ------------------------------------------------------------------
  
  function moneyLeft() {
    // Recalculate the total investment starting at 10K
    totalInvestment = 10000;

    // Loop over all stocks and all elements in the stock
    for (var i = 0; i < allData.length; i++) {
      for (var j = 0; j < Object.keys(allData[i]).length; j++) {
        // Add something different if they are shares
        if (Object.keys(allData[i])[j] == "shares") {
          totalInvestment -= allData[i][Object.keys(allData[i])[j]][0]*
                             thisPrice[i];
        } else {
          totalInvestment -=allData[i][Object.keys(allData[i])[j]][0]*
                            allData[i][Object.keys(allData[i])[j]][1];
        }
      }
    }
    // Set the amout of money left on the HTML page
    document.getElementById("money").innerHTML = 
                                "Money left: $" + formatValue(totalInvestment);
  }

// ------------------------------------------------------------------
// Investment results
// ------------------------------------------------------------------

  function results() {
    // Calculates the profits given an end date. Only if we have money
    if (totalInvestment > 0) {
      // Set variables
      var prof = 0,
          resultTest = "";

      // Loop through all stocks
      for (var i = 0; i < stockData.length; i++) {
        var stockName = stockData[i].name;

        // Check if we invested in the stock
        if (payoffData[i].length !== 0) {
          // Find the key for associated with the new price
          if (GBM === true) {
            var finalKey = Math.round(GBMPrice[i] - thisPrice[i]+30);
          } else {
            var finalKey = Math.round(lastPrice[i] - thisPrice[i]+30);
          }
          // Get the profit associated with the new price via the key
          var stockResult = payoffData[i][payoffData[i].length-1][finalKey].price;
          prof += stockResult;
          resultTest += stockName +": " +formatCurrency(stockResult) + "\n";

        // No investments, so no profits
        } else {
          resultTest += stockName +": $ 0.00 \n";
        }
      }
      // Different outputs for for profit or loss
      if (prof >= 0) {
        resultTest += "You made a PROFIT of " +formatCurrency(prof);
        alert(resultTest);
      } else {
        prof = -prof;
        resultTest += "You made a LOSS of " +formatCurrency(prof);
        alert(resultTest);
      }
      // Boolean variable for the investment line in the payoff graph, plot it
      investButton = true;
      payoffResult();
      // Go-to results are the market prices, not the simulated prices
      GBM = false;
    }
  }

  // Simulates stock prices according to a Geometric Brownian Motion (GBM)
  function GBMresults() {
    // Calculates the profits given an end date. Only if we have money
    if (totalInvestment > 0) {
      // Set the variables (market variables so same for all stocks)
      GBMPrice = [];
      var sigma = 0.5*Math.random(),
          mu = 0.5*Math.random();

      // Simulate paths for each stock
      for (var l = 0; l<stockData.length; l++) {
        var So = thisPrice[l],
            dt = (14/252)/1000;
        for (var i = 0; i < 1000; i++) {
          So *= Math.exp((mu - 0.5*sigma*sigma)*dt + sigma*eps()*Math.sqrt(dt));
        }
        // Must lie between -30 +S0 <ST< 30 + S0 
        So = d3.max([So,thisPrice[l]-30]);
        So = d3.min([So,thisPrice[l]+30]);
        // Add the simuation result to the array
        GBMPrice.push(So);
      }
      // Go-to results are market prices, set them to GBM prices. Call results
      GBM = true;
      results();
    }
  }

  // Funtion which gets called when puts are changed
  function optGraphPut() {
    //Get the amount of options for the selected put and add it to the data dict
    var amountOpts = document.getElementById("numPut").value;
    allData[k][optionInfo.strike+"p"] = [amountOpts, optionInfo.price*100];

    // Remove the result line in the payoff graph and call functions
    investButton = false;
    payoffResult();
    payoffLegendName();
    moneyLeft();
  }

  // Funtion which gets called when calls are changed
  function optGraphCall() {
    //Get the amount of options for the selected put and add it to the data dict
    var amountOpts = document.getElementById("numCall").value;
    allData[k][optionInfo.strike+"c"] = [amountOpts, optionInfo.price*100];

    // Remove the result line in the payoff graph and call functions
    investButton = false;
    payoffResult();
    payoffLegendName();
    moneyLeft();
  }

  // Function that removes all the information
  function clearAll() {
    // Set the input type value to zero, set the data to empty dicts
    clearInput();
    allData = [{},{},{},{},{},{},{},{}];
    payoffData = [[],[],[],[],[],[],[],[]];
    // All radio buttons for each stock must have no value
    // If this isn't done it will light up the previous checked radio button
    checked_boxes = [-1,-1,-1,-1,-1,-1,-1,-1];

    // Uncheck radio buttons and call all relevant functions
    unCheckBoxes();
    investButton = false;
    callFunctions()

    // Set the amount of shares to zero
    document.getElementById("shareSlider").innerHTML =  0 +" shares";
  }

  function clearStock() {
    // Set the input type value to zero and call all relevant functions
    investButton = false;
    clearInput();
    allData[k] = {};
    checked_boxes[k] = -1;
    unCheckBoxes();
    callFunctions()

    // Set the amount of shares to zero
    document.getElementById("shareSlider").innerHTML =  0 +" shares";
  }

  function clearInput() {
    // Set the values to zero for when we clear a stock 
    document.getElementById("numPut").value = 0;
    document.getElementById("numCall").value = 0;
  }

// ------------------------------------------------------------------
// Tour of visualisation
// ------------------------------------------------------------------  

  function tour() {
    // Set the About, term and information boxes to hidden;
    document.getElementById("terms").style.visibility = "hidden"
    if (numAbout !== 0) {
      document.getElementById("about_"+(numAbout-1)).style.visibility = "hidden";
    }
    if (numInfo !== 0 ) {
      document.getElementById("info_"+(numInfo-1)).style.visibility = "hidden";
    }
    // Remember the data we are using, then set the data to zero for examples
    remember = allData;
    allData = [{},{},{},{},{},{},{},{}];

    // Dim the screen, set the number of the tour to zero
    d3.select("svg").style("opacity", 0.6);
    numtour = 0;

    // If somebody presses the tour when there is already a tour in progress
    for (var i = 0; i<10; i++){
      document.getElementById("help_"+i).style.visibility = "hidden";
    }

    // Call the next section of the tour
    tour2();
  }

  function tour2() {
    // Tour ends if we are at number 10
    if (numtour == 10) {
      tour3();
    // We have to remove the prevous tours, but only if it isn't the first
    } else {
      if (numtour != 0) {
        document.getElementById("help_"+(numtour-1)).style.visibility = "hidden";
      }
      // If the tour is at 3 we want the user to click a stock if he hasn't yet
      if (numtour == 3) {
        // Set the name of the stock we have selected
        var tourStockName = stockData[k].name;
        if (tourStockName === "RalphLauren") {
          tourStockName = "Ralph Lauren";
        } else if (tourStockName === "MasterCard") {
          tourStockName = "Master Card";
        }
        document.getElementById("tourName").innerHTML = tourStockName;
        // If no stock is active you cannot press the next button
        var tester = 0;
        for (var i = 0; i < activeStock.length; i++){
          tester += activeStock[i];
        }
        if (tester == 0 ){
          numtour -= 1;
        }
      }
      // Set the current box to visible
      document.getElementById("help_"+numtour).style.visibility = "visible";

      // Share example, with relevant functions
      if (numtour == 7) {
        thisAmount[k] = 4;
        editSlider();
        allData[k]["shares"] = [thisAmount[k]*5, ""];
        payoffResult();
        payoffLegendName();
        moneyLeft();
      }

      // Spread example, with relevant functions
      if (numtour == 8) {
        document.getElementById("bull").checked = true;
        bullSpread();
        payoffLegendName();
      }

      // Single option example, with relevant functions
      if (numtour == 9) {
        document.getElementById("bull").checked = false;
        document.getElementById("optCounterCall").style.visibility = "visible";
        allData[k] = {};
        var tourStrike = optionsJSON[stockData[k].name].call[0].strike,
            tourPrice = optionsJSON[stockData[k].name].call[0].price;
        allData[k][tourStrike +"c"] = [2, tourPrice*100];
        payoffResult();
        payoffLegendName();
      }

      // Next tour box
      numtour += 1;
      }
  }
  
  function tour3(){
    // Function to end the tour
    // Set the svg and previous data back to normal
    d3.select("svg").style("opacity", 1);
    allData = remember;

    // Last tour box must go away, and also the option input
    document.getElementById("help_"+(numtour-1)).style.visibility = "hidden";
    document.getElementById("optCounterCall").style.visibility = "hidden";

    // Set the tour to zero and call all relevant functiona
    numtour = 0;
    payoffResult();
    payoffLegendName();
    editSlider();
  }

// ------------------------------------------------------------------
// Information about the visualisation
// ------------------------------------------------------------------ 

  function about() {
    // Set the tour, term and information boxes to hidden
    document.getElementById("terms").style.visibility = "hidden";
    if (numtour !== 0) {
      document.getElementById("help_"+(numtour-1)).style.visibility = "hidden";
    }
    if (numInfo !==0 ) {
      document.getElementById("info_"+(numInfo-1)).style.visibility = "hidden";
    }

    // Dim the svg
    d3.select("svg").style("opacity", 0.6);
    numAbout = 1;

    // If somebody presses about when it is allready in progress
    for (var i = 1; i<3; i++){
      document.getElementById("about_"+i).style.visibility = "hidden";
    }

    // Call the next function
    about2();
  }

  function about2() {
    // End if the number is 4
    if (numAbout === 4) {
      about3();
    // We have to remove the prevous abouts, but only if it isn't the first
    } else {
      if (numAbout != 1) {
        document.getElementById("about_"+(numAbout-1)).style.visibility = 
                                                                      "hidden";
      }
      document.getElementById("about_"+numAbout).style.visibility = "visible";
      numAbout += 1;
      }
  }

  function about3() {
    // Hide the last box and set the svg to normal
    document.getElementById("about_"+(numAbout-1)).style.visibility = "hidden";
    d3.select("svg").style("opacity", 1);
  }

// ------------------------------------------------------------------
// Information about options
// ------------------------------------------------------------------ 

  function info() {
    // Set the tour, term and about boxes to hidden
    document.getElementById("terms").style.visibility = "hidden";
    document.getElementById("strats").style.visibility = "visible";
    if (numtour !== 0) {
      document.getElementById("help_"+(numtour-1)).style.visibility = "hidden";
    }
    if (numAbout !== 0) {
      document.getElementById("about_"+(numAbout-1)).style.visibility = "hidden";
    }
    // Dim the svg call the next part of the info
    d3.select("svg").style("opacity", 0.6);
    numInfo = 1;
    info2();
  }

  function info2() {
    // End if info is at number 7
    if (numInfo === 7) {
      info3();
    // We have to remove the prevous infos, but only if it isn't the first
    } else {
      if (numInfo != 1) {
        document.getElementById("info_"+(numInfo-1)).style.visibility = "hidden";
      }
      document.getElementById("info_"+numInfo).style.visibility = "visible";
      numInfo += 1
      }
  }

  function info3() {
    // End the information, set the last box to hidden and svg to normal
    document.getElementById("info_"+(numInfo-1)).style.visibility = "hidden";
    d3.select("svg").style("opacity", 1);
  }

// ------------------------------------------------------------------
// Term information
// ------------------------------------------------------------------ 

  function termFun() {
    // Dim svg and make the term box visible
    d3.select("svg").style("opacity", 0.6);
    document.getElementById('terms').style.visibility = 'visible';

    // Set all irrelevant boxes to hidden
    if (numtour !== 0) {
      document.getElementById("help_"+(numtour-1)).style.visibility = "hidden";
    }
    if (numAbout !== 0) {
      document.getElementById("about_"+(numAbout-1)).style.visibility = "hidden";
    }
    if (numInfo !==0 ) {
      document.getElementById("info_"+(numInfo-1)).style.visibility = "hidden";
    }
  }

  function termEnd() {
    // End the terms, set the last box to hidden and svg to normal
    document.getElementById('terms').style.visibility = 'hidden';
    d3.select("svg").style("opacity", 1);
  }

// ------------------------------------------------------------------
// Text behind the slider
// ------------------------------------------------------------------ 

  function sliderText() {
    // Set text behind the slider to the amount if the entry in the dict exists
    if (allData[k]["shares"] !== undefined) {
      document.getElementById("shareSlider").innerHTML = 
      allData[k]["shares"][0] +" shares";
    // Set it to zero if there is no entry in the dict
    } else {
      document.getElementById("shareSlider").innerHTML = 
      0 +" shares";
    }
  }

// ------------------------------------------------------------------
// Section regarding checking and unchecking the boxes
// ------------------------------------------------------------------ 

  function unCheckBoxes() {
    // Uncheck all the radio buttons
    var boxes = document.getElementsByName("strategy");
    for (var l=0; l<boxes.length; l++){
        boxes[l].checked = false;
    }

  window.checkBoxes = function() {
    // Check the radio button
    var boxes = document.getElementsByName("strategy");
    boxes[checked_boxes[k]].checked = true;
  }

  window.callFunctions = function() {
    // Highly used functions
    editSlider();
    payoffLegendName();
    payoffResult();
    moneyLeft();
    sliderText();
  }

// ------------------------------------------------------------------
// END OF JAVASCRIOT
// ------------------------------------------------------------------
}