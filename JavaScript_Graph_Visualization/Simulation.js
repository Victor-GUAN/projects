/* Created by Minghui GUAN on 4/06/2017.
 */
define([
    'jquery',
    "d3.js"
],function($,d3){
    var TSNE_simulation = function(json){

        d3.selectAll("button").remove();
        d3.selectAll(".tab_menu_el").remove();
        console.log("attention");
        console.log(json);
        var Button = d3.selectAll("body");
        Button.append("input")
            .attr("id","start_continue")
            .attr("class","simu_button")
            .attr("type","button")
            .attr("value","Start"+"\n"+"Continue")
            .classed("simu_button",true)
            .attr("style","top:80px")
            .on("click",start_continue);


        Button.append("input")
            .attr("id","stop")
            .attr("class","simu_button")
            .attr("type","button")
            .attr("value","Stop")
            .classed("simu_button",true)
            .attr("style","top:150px")
            .on("click",stop);

        Button.append("input")
            .attr("id","restart")
            .attr("class","simu_button")
            .attr("type","button")
            .attr("value","Restart")
            .classed("simu_button",true)
            .attr("style","top:220px")
            .on("click",restart);

        var width = window.innerWidth - 315;
        var height = window.innerHeight - 40;
        var image_width = 20;
        var image_height = 20;

        /*the function of zoom*/
        var zoom = d3.zoom()
            .scaleExtent([1, 10])
            .on("zoom", zoomed);

        /*input manipulate the data of json*/

        d3.selectAll(".node")
            .attr("opacity",0);
        d3.selectAll("div1").remove();
        d3.select("#simu_svg").remove();

        /*create a svg*/
        var svg = d3.select("body")
            .append("svg")
            .attr("id","simu_svg")
            .attr("width",window.innerWidth - 315)
            .attr("height",window.innerHeight - 40)
            .call(zoom);

        $("svg").css({left: 315,top: 40, position: 'absolute'});

        var extend_group = svg.append("g")
            .call(zoom);

        var padding ={left:30, right:30, top:20, bottom:20};

        var dataset=[];
        var dataFolder = json.graphs._ALL.dataFolder;
        var dict_keys = Object.keys(json.graphs._ALL.nodes);
        var iter_size = Object.keys(json.graphs).length - 1;
        console.log(dict_keys);

        /*construct the set of data with compatible structure*/
        for (var i = 0; i<dict_keys.length; i++) {

            dataset[i] = {};
            for (var j = 1; j<=iter_size; j++){
                dataset[i]["iter_"+(json.graphs._ALL.step)*j]
                    = [eval("json.graphs.iter" + (json.graphs._ALL.step)*j + ".nodes[dict_keys[i]].coord.tSNE[0]"),eval("json.graphs.iter" + (json.graphs._ALL.step)*j + ".nodes[dict_keys[i]].coord.tSNE[1]")]
            }
            dataset[i]["img"] = json.graphs._ALL.nodes[dict_keys[i]].img;
            dataset[i]['name'] = json.graphs._ALL.nodes[dict_keys[i]].name;

        }

        console.log(dataset);
        console.log([json.graphs._ALL.extreme[0],json.graphs._ALL.extreme[2]]);
        console.log([json.graphs._ALL.extreme[1],json.graphs._ALL.extreme[3]]);

        /*define the measuring scale of axis*/
        //to keep the same scale of axis x and axis y
        /* Height/Width = (axis_max_Y - axis_min_Y) / (axis_max_X - axis_min_X)
         axis_max_X / axis_min_X = max_X / min_X */


        var xScale = d3.scaleLinear()
            .domain([(json.graphs._ALL.extreme[3]-json.graphs._ALL.extreme[1])/(json.graphs._ALL.extreme[2]/json.graphs._ALL.extreme[0] - 1)*((window.innerWidth - 315)-padding.left-padding.right - 20 - 20)/(window.innerHeight-40-padding.top-padding.bottom - 20 - 20),
                (json.graphs._ALL.extreme[3]-json.graphs._ALL.extreme[1])/(json.graphs._ALL.extreme[2]/json.graphs._ALL.extreme[0] - 1)*((window.innerWidth - 315)-padding.left-padding.right - 20 - 20)/(window.innerHeight-40-padding.top-padding.bottom - 20 - 20) * (json.graphs._ALL.extreme[2]/json.graphs._ALL.extreme[0])])

            .range([0 + 20,(window.innerWidth - 315)-padding.left-padding.right - 20]);

        var yScale = d3.scaleLinear()
            .domain([json.graphs._ALL.extreme[1],json.graphs._ALL.extreme[3]])
            .range([window.innerHeight-40-padding.top-padding.bottom - 20, 0 + 20]);

        //define axis x
        var xAxis = d3.axisBottom(xScale);

        //define axis y
        var yAxis = d3.axisLeft(yScale);

        //add axis x
        extend_group.append("g")
            .attr("class","axis")
            .attr("transform","translate(" + (padding.left) + "," + (window.innerHeight - padding.bottom-10-(window.innerHeight-padding.top-padding.bottom-yScale(0))) + ")")
            .call(xAxis);

        //add axis y
        extend_group.append("g")
            .attr("class","axis")
            .attr("transform","translate(" + (padding.left+xScale(0)) +"," + (padding.top-10) + ")")
            .call(yAxis);

        //create a frame of explanatory note
        var tooltip = d3.select("body")
            .append("div")
            .attr("class", "tooltip")
            .style("display", "none");


        //create the objects of images, define their attributes, input the links of images and realize the display of frame with mouse move
        var images = extend_group.selectAll("image")
            .data(dataset);

        var images_move = images.enter()
            .append("svg:image")
            .attr("transform","translate(" + (padding.left) + ", " + (padding.top-10) +")")
            .attr("x",function(d,i){
                return xScale(eval("d.iter_" + json.graphs._ALL.step * 1 + "[0]"))-image_width/2;
            })
            .attr("y",function(d,i){
                return yScale(eval("d.iter_" + json.graphs._ALL.step * 1 + "[1]"))-image_height/2;
            })
            .attr("width",image_width)
            .attr("height",image_height)
            /*.attr("xlink:href","logo.png");*/
            .attr("xlink:href",function(d,i){
                return	d.img
            })
			.on("error",function(d){
				$(this).attr("href", "../../data/"+(dataFolder+"/"+d.img).split("/").slice(1).join("/"));	
			});

        $("image").one("error", function(d){
            $(this).attr("href", "logo.png");
        });


        var annotation = function(s){

            images
                .merge(images_move)
                .on("mouseover",function(d){
                    tooltip
                        .style("display", "inline")
                        .html(" &nbsp name: &nbsp " + d.name + "<br />" + " &nbsp tSNE-x: " + eval("d.iter_" + json.graphs._ALL.step * (s+2) + "[0]") + "&nbsp" + "<br />" + " &nbsp tSNE-y: " + eval("d.iter_" + json.graphs._ALL.step * (s+2) + "[1]") + "&nbsp")
                        .style("left", (d3.event.pageX) + "px")
                        .style("top", (d3.event.pageY + 20) + "px");

                })
                .on("mousemove", function(d){
                    tooltip.style("left", (d3.event.pageX) + "px")
                        .style("top", (d3.event.pageY + 20) + "px");
                })
                .on("mouseout", function(d){
                    tooltip.style("display", "none");
                })

        };

        annotation(-1);

        //create a container viewbox to add annotations
        var comment = d3.select("body")
            .append("div1")
            .attr("class","tooltip")
            .attr("id","comment")
            .style("opacity",1.0)
            .style("top",(window.innerHeight-padding.top-padding.bottom - 40 - 40) + "px")
            .style("left",(window.innerWidth-padding.left-padding.right - 80 - 80) + "px");

        comment
            .html("<span style='white-space:pre;'>" + "  ITER &nbsp;       " + json.graphs._ALL.step * iter_size + " &nbsp; " + "<br />" + "  NOW    &nbsp; iter " + json.graphs._ALL.step + " &nbsp; "+ " &nbsp; " + "</span>");

        console.log(document.getElementsByTagName("span")[0].innerHTML.split(" "));

        //define the time intervalle between each step
        var time_step = 650;
        var a = [];
        var b = [];
        var now = 0;

        //realize the continuous move of images in a series of steps
        //use the assignment operator "let" instead of "var" to avoid the problem of the value of dynamic variables

        //define the start_continue function to continue or start the move of images
        function start_continue(){

            now = parseInt(document.getElementsByTagName("span")[0].innerHTML.split(" ")[20])/json.graphs._ALL.step-1;
            for(let m = parseInt(document.getElementsByTagName("span")[0].innerHTML.split(" ")[20])/json.graphs._ALL.step-1 ; m < iter_size -1 ; m++) {
                //redefine the function for position translate with the matching of new steps
                a[m] = function(){

                    simulation(m);

                };

                //the delay of time for different steps
                clearTimeout(b[m]);
                b[now] = setTimeout(a[m], time_step*(m-(parseInt(document.getElementsByTagName("span")[0].innerHTML.split(" ")[20])/json.graphs._ALL.step-1)));
                now += 1;
            }
        }

        //define the stop function to control the move of images for visualisation
        function stop(){

            for(let q = parseInt(document.getElementsByTagName("span")[0].innerHTML.split(" ")[20])/json.graphs._ALL.step-1 ; q < iter_size -1 ; q++){

                clearTimeout(b[q]);
            }
        }

        //define the restart function to initialize the iteration
        function restart(){

            stop();
            simulation(-1);

        }

        // add the final annotations for the images
        var annotation_num = 0;
        var final_anno = function() {
            var l = setInterval(function() {
                annotation_num++;
                if ( parseInt(document.getElementsByTagName("span")[0].innerHTML.split(" ")[20]) == json.graphs._ALL.step * iter_size )
                    annotation(iter_size-2);
                if (annotation_num > 60)
                    clearInterval(l);
            }, 1000);
        };
        setTimeout(final_anno, iter_size * time_step);

        //define the function of simulation
        var simulation = function(n){

            //$(".tooltip").opacity = 0.0;

            annotation(n);

            images
                .merge(images_move)
                .transition()
                .duration(time_step)
                .ease(d3.easeLinear)
                .attr("x", function (d) {
                    return xScale(eval("d.iter_" + json.graphs._ALL.step * (n+2) + "[0]")) - image_width / 2;
                })
                .attr("y", function (d) {
                    return yScale(eval("d.iter_" + json.graphs._ALL.step * (n+2) + "[1]")) - image_height / 2;
                });


            comment
                .html("<span style='white-space:pre;'>" + "  ITER &nbsp;       " + json.graphs._ALL.step * iter_size + " &nbsp; " + "<br />" + "  NOW    &nbsp; iter " + json.graphs._ALL.step * (n+2) + " &nbsp; "+ " &nbsp; " + "</span>");

        };

//define the function of zoom
        function zoomed(){
            d3.select(this).attr(
                "transform",'translate(' + d3.event.transform.x + ',' + d3.event.transform.y + ') scale(' + d3.event.transform.k + ')');
        }




    };
    return{
        TSNE_simulation: TSNE_simulation
    }
});


