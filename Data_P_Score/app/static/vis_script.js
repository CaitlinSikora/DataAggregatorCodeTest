console.log("starting js");
function InitChart(barData) {

            var mean = 0
            for (i=0;i<barData.length;i++){
            	mean+=barData[i].y;
            }
            mean = Math.round(mean / barData.length*100)/100;
            $('#final').html(mean);
            console.log(mean);
            console.log(barData.length);
            var vis = d3.select('#visualisation'),
                WIDTH = 1000,
                HEIGHT = 360,
                MARGINS = {
                    top: 10,
                    right: 60,
                    bottom: 40,
                    left: 50
                },
                xRange = d3.scale.ordinal().rangeRoundBands([MARGINS.left, WIDTH - MARGINS.right], 0.1).domain(barData.map(function(d) {
                    return d.x;
                })),


                yRange = d3.scale.linear().range([HEIGHT-MARGINS.top, MARGINS.bottom]).domain([0,
                    d3.max(barData, function(d) {
                        return 1.0;
                    })
                ]),

                xAxis = d3.svg.axis()
                .tickFormat(function(d) {
                    return d
                })
                .scale(xRange)
                .tickSize(3)
                .tickSubdivide(true)
                .ticks(10),

                yAxis = d3.svg.axis()
                .scale(yRange)
                .tickSize(3)
                .orient("left")
                .tickSubdivide(true);

            vis.append('svg:g')
                .attr('class', 'x axis')
                .attr('transform', 'translate(0,' + (HEIGHT - MARGINS.bottom) + ')')
                .call(xAxis);

            vis.append('svg:g')
                .attr('class', 'y axis')
                .attr('transform', 'translate(' + (MARGINS.left) + ',-30)')
                .call(yAxis);

            vis.append("line")          
			    .attr("class", "mean")  
			    .attr("x1", MARGINS.left)     
			    .attr("y1", yRange(mean)-30)      
			    .attr("x2", WIDTH-MARGINS.right-20)     
			    .attr("y2", yRange(mean)-30);

			vis.append("text")
				.attr("x", WIDTH-MARGINS.right)
         		.attr("y", yRange(mean)-20)
         		.attr("style", "font-size:30px;")
                .text(mean)    

            vis.selectAll('rect')
                .data(barData)
                .enter()
                .append('rect')
                .attr('x', function(d) {
                    return xRange(d.x);
                })
                .attr('y', function(d) {
                    return yRange(d.y)-30;
                })
                .attr('width', xRange.rangeBand())
                .attr('height', function(d) {
                    return ((HEIGHT - MARGINS.bottom) - yRange(d.y)+30);
                })
                .attr({
                    ry: '5',
                    rx: '5'
                })
                .attr('fill', '#5caaf2')
                .style("opacity", .65)
                .on('mouseover', function(d) {
                    d3.select(this)
                        .attr('fill', '#1474cd');
                    console.log(d);
                    p_messages='';
                    for (i=0;i<d.z.length;i++){
                    	p_messages+='<p>'+d.z[i]+'</p>';
                    }
                    $('.messages').html(p_messages);
                })
                .on('mouseout', function(d) {
                    d3.select(this)
                        .attr('fill', '#5caaf2');
                });

        }
