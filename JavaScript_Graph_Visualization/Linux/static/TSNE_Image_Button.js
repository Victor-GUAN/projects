/**
 * Created by MGN11 on 3/29/2017.
 */

'use strict';

var width = window.innerWidth - 160;
var height = window.innerHeight;
var image_width = 30;
var image_height = 30;

/*the function of zoom*/
var zoom = d3.zoom()
    .scaleExtent([1, 10])
    .on("zoom", zoomed);

/*input manipulate the data of json*/

document.getElementById('import').onclick = function(){

    d3.selectAll("svg").remove();
    d3.selectAll("div1").remove();

    d3.selectAll("div").remove();

    /*create a svg*/
    var svg = d3.select("body")
        .append("svg")
        .attr("width",window.innerWidth - 125)
        .attr("height",window.innerHeight)
        .call(zoom);

    $("svg").css({left: 160,top: 10, position: 'absolute'});

    var extend_group = svg.append("g")
        .call(zoom);

    var files = document.getElementById('selectFiles').files;
    /*console.log(files);*/
    if (files.length <= 0) {
        return false;
    }

    var fr = new FileReader();

    fr.onload = function(event) {

        console.log(event.target.result);
        var json = JSON.parse(event.target.result);

        var datafolder = json.graphs._ALL.dataFolder;
        var dict_keys = Object.keys(json.graphs._ALL.nodes);

        var mydata = {};

        /*construct the set of data with compatible structure*/
        for (var i = 0; i < dict_keys.length; i++) {

            mydata["img" + i] = datafolder + '/' + json.graphs._ALL.nodes[dict_keys[i]].img;

        }

        $.getJSON('http://10.0.2.15:80/Flask/dataconvert', {
            "mykey": JSON.stringify(mydata)
        }, function (data) {
            console.log(data);
            var padding = {left: 30, right: 30, top: 20, bottom: 20};
            var iter_size = Object.keys(json.graphs).length - 1;
            var dict_keys = Object.keys(json.graphs._ALL.nodes);
            var dataset = [];

            for (var i = 0; i < dict_keys.length; i++) {

                dataset[i] = {};
                for (var j = 1; j <= iter_size; j++) {
                    dataset[i]["iter_" + (json.graphs._ALL.step) * j]
                        = [eval("json.graphs.iter" + (json.graphs._ALL.step) * j + ".nodes[dict_keys[i]].coord.tSNE[0]"), eval("json.graphs.iter" + (json.graphs._ALL.step) * j + ".nodes[dict_keys[i]].coord.tSNE[1]")]
                }
                dataset[i]['name'] = json.graphs._ALL.nodes[dict_keys[i]].name;
                dataset[i]["img"] = "data:image/png;base64," + data.result['img' + i];

            }


            console.log(dataset);
            console.log([json.graphs._ALL.extreme[0], json.graphs._ALL.extreme[2]]);
            console.log([json.graphs._ALL.extreme[1], json.graphs._ALL.extreme[3]]);

            /*define the measuring scale of axis*/
            //to keep the same scale of axis x and axis y
            /* Height/Width = (axis_max_Y - axis_min_Y) / (axis_max_X - axis_min_X)
             axis_max_X / axis_min_X = max_X / min_X */


            var xScale = d3.scaleLinear()
                .domain([(json.graphs._ALL.extreme[3] - json.graphs._ALL.extreme[1]) / (json.graphs._ALL.extreme[2] / json.graphs._ALL.extreme[0] - 1) * ((window.innerWidth - 160) - padding.left - padding.right - 20 - 20) / (window.innerHeight - padding.top - padding.bottom - 20 - 20),
                    (json.graphs._ALL.extreme[3] - json.graphs._ALL.extreme[1]) / (json.graphs._ALL.extreme[2] / json.graphs._ALL.extreme[0] - 1) * ((window.innerWidth - 160) - padding.left - padding.right - 20 - 20) / (window.innerHeight - padding.top - padding.bottom - 20 - 20) * (json.graphs._ALL.extreme[2] / json.graphs._ALL.extreme[0])])

                .range([0 + 20, (window.innerWidth - 160) - padding.left - padding.right - 20]);

            var yScale = d3.scaleLinear()
                .domain([json.graphs._ALL.extreme[1], json.graphs._ALL.extreme[3]])
                .range([window.innerHeight - padding.top - padding.bottom - 20, 0 + 20]);

            //define axis x
            var xAxis = d3.axisBottom(xScale);

            //define axis y
            var yAxis = d3.axisLeft(yScale);

            //add axis x
            extend_group.append("g")
                .attr("class", "axis")
                .attr("transform", "translate(" + (padding.left) + "," + (window.innerHeight - padding.bottom - 10 - (window.innerHeight - padding.top - padding.bottom - yScale(0))) + ")")
                .call(xAxis);

            //add axis y
            extend_group.append("g")
                .attr("class", "axis")
                .attr("transform", "translate(" + (padding.left + xScale(0)) + "," + (padding.top - 10) + ")")
                .call(yAxis);

            //create a frame of explanatory note
            var tooltip = d3.select("body")
                .append("div")
                .attr("class", "tooltip")
                .style("opacity", 0.0);

            //create the objects of images, define their attributes, input the links of images and realize the display of frame with mouse move
            var images = extend_group.selectAll("image")
                .data(dataset);

            var images_move = images.enter()
                .append("svg:image")
                .attr("transform", "translate(" + (padding.left) + ", " + (padding.top - 10) + ")")
                .attr("x", function (d, i) {
                    return xScale(eval("d.iter_" + json.graphs._ALL.step * 1 + "[0]")) - image_width / 2;
                })
                .attr("y", function (d, i) {
                    return yScale(eval("d.iter_" + json.graphs._ALL.step * 1 + "[1]")) - image_height / 2;
                })
                .attr("width", image_width)
                .attr("height", image_height)
                .attr("xlink:href", function (d, i) {
                    return d.img;
                })

                .on("mouseover", function (d) {
                    tooltip.html(" &nbsp name: &nbsp " + d.name + "<br />" + " &nbsp tSNE-x: " + eval("d.iter_" + json.graphs._ALL.step * 1 + "[0]") + "&nbsp" + "<br />" + " &nbsp tSNE-y: " + eval("d.iter_" + json.graphs._ALL.step * 1 + "[1]") + "&nbsp")
                        .style("left", (d3.event.pageX) + "px")
                        .style("top", (d3.event.pageY + 20) + "px")
                        .style("opacity", 0.8);
                })
                .on("mousemove", function (d) {
                    tooltip.style("left", (d3.event.pageX) + "px")
                        .style("top", (d3.event.pageY + 20) + "px");
                })
                .on("mouseout", function (d) {
                    tooltip.style("opacity", 0.0);
                });

            //ctreat a container viewbox for adding buttons
            var container = d3.select("body").append("div").attr("id", "container");
            var objTo = document.getElementById('container');

            //define and execute the function for creating the buttons for each step added in the container viewbox
            function create_button() {
                for (let k = 0; k < iter_size; k++) {
                    var bt = document.createElement("input");
                    bt.type = "button";
                    bt.id = "iter_" + json.graphs._ALL.step * (k + 1);
                    bt.value = "iter" + json.graphs._ALL.step * (k + 1);
                    bt.style = "font-size:12px;width:68px";
                    bt.onclick = a[k];
                    objTo.appendChild(bt);

                }
            }


            //define for each button the translation of images
            var time_step = 650;
            var a = [];
            for (let q = 0; q < iter_size; q++) {
                a[q] = function () {

                    $(".tooltip").opacity = 0.0;

                    images
                        .merge(images_move)
                        .on("mouseover", function (d) {
                            tooltip.html(" &nbsp name: &nbsp " + d.name + "<br />" + " &nbsp tSNE-x: " + eval("d.iter_" + json.graphs._ALL.step * (q + 1) + "[0]") + "&nbsp" + "<br />" + " &nbsp tSNE-y: " + eval("d.iter_" + json.graphs._ALL.step * (q + 1) + "[1]") + "&nbsp")
                                .style("left", (d3.event.pageX) + "px")
                                .style("top", (d3.event.pageY + 20) + "px")
                                .style("opacity", 0.8);
                        })
                        .on("mousemove", function (d) {
                            tooltip.style("left", (d3.event.pageX) + "px")
                                .style("top", (d3.event.pageY + 20) + "px");
                        })
                        .on("mouseout", function (d) {
                            tooltip.style("opacity", 0.0);
                        });

                    images
                        .merge(images_move)
                        .transition()
                        .duration(time_step)
                        .ease(d3.easeLinear)
                        .attr("x", function (d) {
                            return xScale(eval("d.iter_" + json.graphs._ALL.step * (q + 1) + "[0]")) - image_width / 2;
                        })
                        .attr("y", function (d) {
                            return yScale(eval("d.iter_" + json.graphs._ALL.step * (q + 1) + "[1]")) - image_height / 2;
                        });

                };

            }

            create_button();

        })
    };

    fr.readAsText(files.item(0));

};





//define the function of zoom
function zoomed(){
    d3.select(this).attr(
        "transform",'translate(' + d3.event.transform.x + ',' + d3.event.transform.y + ') scale(' + d3.event.transform.k + ')');
}