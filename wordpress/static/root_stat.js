function sites () {
	$("#sites-container").toggle();
}

function site_bubble() {
	$("#site-bubble").toggle();
}

function site_trends () {
	$("#site-trends").toggle();
}

function bubble_visual (root, container) {
	
	container.selectAll("svg").remove();

	var margin = 20,
	    diameter = 1000;

   //var tooltip = d3.select("#site-bubble").append("div").attr("id", "tooltip").style("opacity", 0);
   var tooltip = container.append("div").attr("id", "tooltip").style("opacity", 0);

	var color = d3.scale.linear()
	    .domain([-1, 5])
	    .range(["hsl(209,80%,80%)", "hsl(228,30%,40%)"])
	    .interpolate(d3.interpolateHcl);

	var pack = d3.layout.pack()
	    .padding(2)
	    .size([diameter - margin, diameter - margin])
	    .value(function(d) { return 1; });

	// var svg = d3.select("#site-bubble").append("svg")
	var svg = container.append("svg")
	    .attr("width", diameter)
	    .attr("height", diameter)
	  .append("g")
	    .attr("transform", "translate(" + diameter / 2 + "," + diameter / 2 + ")");


	var focus = root,
	  nodes = pack.nodes(root),
	  view;

	var circle = svg.selectAll("circle")
	  .data(nodes)
	.enter().append("circle")
	  .attr("class", function(d) { return d.parent ? d.children ? "node" : "node node--leaf" : "node node--root"; })
	  .style("fill", function(d) { return d.children ? color(d.depth) : null; })
	  .on("click", function(d) { if (focus !== d) zoom(d), d3.event.stopPropagation(); })
	  .on("mouseover", function(d) {
			tooltip.transition()
				.duration(100)
				.style("opacity", 0.9);
			tooltip.html(d.title+".<br/>"+d.subtitle+".<br/>Published : "+d.published.slice(0, 10))
				.style("left", d3.event.pageX+"px")
				.style("top", d3.event.pageY+"px");
		})
		.on("mouseout", function(d) {
			tooltip.transition()
				.duration(100)
				.style("opacity", 0);
		})
		.on("dblclick", function(d){
			window.location.href="/wordpress/stats?url="+d.url+"&level="+d.level;
		});

	var text = svg.selectAll("text")
	  .data(nodes)
	.enter().append("text")
	  .attr("class", "label")
	  .style("fill-opacity", function(d) { return d.parent === root ? 1 : 0; })
	  .style("display", function(d) { return d.parent === root ? null : "none"; })
	  .text(function(d) { return d.level === "page" ? d.title : ""; });

	var node = svg.selectAll("circle,text");

	  // d3.select("#site-bubble")
	  container
	      .style("background", color(-1))
	      .on("click", function() { zoom(root); });

	  zoomTo([root.x, root.y, root.r * 2 + margin]);

	  function zoom(d) {
	    var focus0 = focus; focus = d;

	    var transition = d3.transition()
	        .duration(d3.event.altKey ? 7500 : 750)
	        .tween("zoom", function(d) {
	          var i = d3.interpolateZoom(view, [focus.x, focus.y, focus.r * 2 + margin]);
	          return function(t) { zoomTo(i(t)); };
	        });

	    transition.selectAll("text")
	      .filter(function(d) { return d.parent === focus || this.style.display === "inline"; })
	        .style("fill-opacity", function(d) { return d.parent === focus ? 1 : 0; })
	        .each("start", function(d) { if (d.parent === focus) this.style.display = "inline"; })
	        .each("end", function(d) { if (d.parent !== focus) this.style.display = "none"; });
	  }

	  function zoomTo(v) {
	    var k = diameter / v[2]; view = v;
	    node.attr("transform", function(d) { return "translate(" + (d.x - v[0]) * k + "," + (d.y - v[1]) * k + ")"; });
	    circle.attr("r", function(d) { return d.r * k; });
	  }

	d3.select(self.frameElement).style("height", diameter + "px");
}

function trends_visual () {
	$(function() {
	    $( "#from" ).datepicker({
	      defaultDate: "-2m",
	      changeMonth: true,
	      numberOfMonths: 3,
	      onClose: function( selectedDate ) {
	        $( "#to" ).datepicker( "option", "minDate", selectedDate );
	      }
	    });
	    $( "#to" ).datepicker({
	      defaultDate: "0",
	      changeMonth: true,
	      numberOfMonths: 3,
	      onClose: function( selectedDate ) {
	        $( "#from" ).datepicker( "option", "maxDate", selectedDate );
	      }
	    });
	  });
}

function analyze () {
	// Sends a GET request to the server with the date range, receives the data and visualizes it in several ways!
	var from = $("#from").datepicker("getDate");
	var to = $("#to").datepicker("getDate");
	var flag = true
	if (from === null){
		$("#from").val("!?!?!");
		flag = false;
	}
	if(to === null){
		$("#to").val("!?!?!");
		flag = false;
	}
	if (flag){
		$("#trend-word-cloud").empty();
		$("#trend-bar-graph").empty();
		$("#trend-summary").empty();
		$("#word-list")
		$.ajaxSetup({
		    beforeSend:function(){
		        $("#ajax-loader").show();
		    },
		    complete:function(){
		        $("#ajax-loader").hide();
		    }
		});
		var temp = $.get("api", {from : from , to : to}, function (data) {
			trend_summary(data);	//Print summary
			if (data['page_count'] > 0){
				trend_word_cloud(data['word_count'], d3.select("#trend-word-cloud")); //Word Cloud Visual
				bar_graph(data['word_bags'], d3.select("#trend-bar-graph")); //Word Count Bar graph
			}
		}, "json");
	}
}

function trend_summary (data) {
	// Prints the stats of the results to #trend-summary div
	var summary = $("#trend-summary");
	summary.empty();
	summary.append( "Number of posts (pages) published : "+data['page_count']);
	summary.append("<br> Number of sites with activity : "+data['site_count']);
}

function trend_word_cloud(data, container) {
	container.selectAll("svg").remove();
	
	data =data.slice(0, 50);
	var fill = d3.scale.category20();
	var x = $("#site-trends").innerWidth()*0.9;
	var y = 500;
	var scale = 100/data[0]['count'];

	d3.layout.cloud().size([x, y])
	  .words(data.map(function(d) {
	    return {text: d['text'], size: d['count'] * scale};
	  }))
	  .rotate(function() { return ~~(Math.random() * 2) * 90; })
	  .font("Impact")
	  .fontSize(function(d) { return d.size; })
	  .on("end", draw)
	  .start();

	function draw(words) {
	container.append("svg")
	    .attr("width", x)
	    .attr("height", y)
	  .append("g")
	    .attr("transform", "translate("+x/2+","+y/2+")")
	  .selectAll("text")
	    .data(words)
	  .enter().append("text")
	    .style("font-size", function(d) { return d.size + "px"; })
	    .style("font-family", "Impact")
	    .style("fill", function(d, i) { return fill(i); })
	    .attr("text-anchor", "middle")
	    .attr("transform", function(d) {
	      return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
	    })
	    .text(function(d) { return d.text; });
	}
}

function bar_graph(data, container) {
	container.selectAll("svg").remove();

	container.style("background", "white");

	var margin = {top: 50, right: 30, bottom: 50, left: 30},
	    width = parseInt(container.style("width")) - margin.left - margin.right,
	    height = 500 - margin.top - margin.bottom;

	var x = d3.scale.ordinal()
	    .rangeRoundBands([0, width], .1, .3);

	var y = d3.scale.linear()
	    .range([height, 0]);

	var xAxis = d3.svg.axis()
	    .scale(x)
	    .orient("bottom");

	var yAxis = d3.svg.axis()
	    .scale(y)
	    .orient("left");
	    //.ticks(8, "%");

	var svg = container.append("svg")
	    .attr("width", width + margin.left + margin.right)
	    .attr("height", height + margin.top + margin.bottom)
	  .append("g")
	    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
	
	x.domain(data.map(function(d) { return d.count; }));
	y.domain([0, d3.max(data, function(d) { return d.count; })]);

	svg.append("text")
      .attr("class", "title")
      .attr("x", x(data[0].count))
      .attr("y", -26)
      .text("Word Frequencies");

    svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

    svg.append("g")
      .attr("class", "y axis")
      .call(yAxis);

    svg.selectAll(".bar")
      .data(data)
    .enter().append("rect")
      .attr("class", "bar")
      .attr("x", function(d) { return x(d.count); })
      .attr("width", x.rangeBand())
      .attr("y", function(d) { return y(d.count); })
      .attr("height", function(d) { return height - y(d.count); })
      .on("mouseover", function(d) { d3.select(this).style("cursor", "pointer");})
      .on("click", function(d) {
      	$("#word-list").empty();
      	var words = document.getElementById("word-list");
      	for (var i = 0; i < d.words.length; i++) {
      	 	words.innerHTML += d.words[i] + ". ";
      	 }; });


    d3.select("#site-trends").append("div")
      .attr("id", "word-list")
      .style("margin-top", "10px");
}